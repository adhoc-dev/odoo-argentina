from odoo import models, fields
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_pricelist_id = fields.Many2one(string="Tarifa", comodel_name="product.pricelist", on_delete="set null")
    x_usage = fields.Selection(string="Usage", related="location_id.usage", copy=False)
    x_seguimiento = fields.Text(string="Nº de seg. Correo argentino")

    def write(self, vals):
        if 'sale_id' in vals and vals.get('sale_id'):
            self.message_subscribe([self.env['sale.order'].browse(vals.get('sale_id')).user_id.partner_id.id], force=False)
        if 'x_seguimiento' in vals and vals.get('x_seguimiento'):
            self.message_post_with_template(94)
        return super().write(vals)


    def create_invoice_from_picking(self):
        def _prepare_invoice_line(pack_operation):
            account = pack_operation.product_id.property_account_income_id or pack_operation.product_id.categ_id.property_account_income_categ_id
            if not account:
                raise UserError(
                    ('Please define income account for this product:"%s" (id:%d) - or for its category: "%s".') %
                    (pack_operation.product_id.name,
                    pack_operation.product_id.id,
                    pack_operation.product_id.categ_id.name))

            fpos = self.partner_id.property_account_position_id
            if fpos:
                account = fpos.map_account(account)
            tmp_line = invoice_line_obj.new({'product_id': pack_operation.product_id.id})
            tmp_line._onchange_product_id()
            return {
                'name': tmp_line.name,
                'account_id': account.id,
                'product_id': pack_operation.product_id.id,
                'product_uom_id': tmp_line.product_uom_id.id,
                'quantity': pack_operation.qty_done,
                'price_unit': tmp_line.price_unit,
                'tax_ids': [(6, 0, pack_operation.product_id.taxes_id.filtered(lambda x: x.company_id == self.company_id).ids)]
            }
        self.ensure_one()
        journal = self.env['account.move'].with_context(default_type='out_refund')._get_default_journal()
        invoice_line_obj = self.env['account.move.line']
        invoice_obj = self.env['account.move']
        if self.sale_id or self.picking_type_code != 'incoming' or self.location_id.usage != 'customer' or self.state != 'done':
                raise UserError("No puede generar factura para este picking")
        invoices = []
        invoice_vals = {
                'invoice_origin': self.name,
                'type': 'out_refund',
                'partner_id': self.partner_id.id,
                'journal_id': journal.id,
                'currency_id': self.x_pricelist_id.currency_id.id,
                'narration': self.note,
                'company_id': self.company_id.id,
                'picking_ids': [(4, self.id)],
                'invoice_line_ids':[(0, None, _prepare_invoice_line(line)) for line in self.move_line_ids],
        }
        invoice = invoice_obj.create(invoice_vals)
        invoices.append(invoice.id)
        wiz = self.env['account.invoice.prices_update.wizard'].with_context(active_id=invoices).create({'pricelist_id': self.x_pricelist_id.id})
        wiz.update_prices()
        actions = self.env.ref('account.action_move_out_refund_type')
        action_read = actions.read()[0]
        action_read['domain'] = [('id', 'in', invoices)]
        return action_read
