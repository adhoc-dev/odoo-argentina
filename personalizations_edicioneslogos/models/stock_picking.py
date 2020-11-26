from odoo import api, models, fields
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_pricelist_id = fields.Many2one(string="Tarifa", comodel_name="product.pricelist", on_delete="set null")
    x_usage = fields.Selection(string="Usage", related="location_id.usage", readonly=True, copy=False)
    x_seguimiento = fields.Text(string="Nº de seg. Correo argentino")

    @api.multi
    def write(self, vals):
        if 'sale_id' in vals and vals.get('sale_id'):
            self.message_subscribe([self.env['sale.order'].browse(vals.get('sale_id')).user_id.partner_id.id], force=False)
        if 'x_seguimiento' in vals and vals.get('x_seguimiento'):
            self.message_post_with_template(94)
        return super(StockPicking, self).write(vals)


    def create_invoice_from_picking(self):
        self.ensure_one()
        journal_id = self.env['account.invoice'].default_get(['journal_id'])['journal_id']
        invoice_line_obj = self.env['account.invoice.line']
        invoice_obj = self.env['account.invoice']
        if self.sale_id or self.picking_type_code != 'incoming' or self.location_id.usage != 'customer' or self.state != 'done':
                raise Warning("No puede generar factura para este picking")
        invoices = []
        invoice_vals = {
                'origin': self.name,
                'type': 'out_refund',
                'account_id': self.partner_id.property_account_receivable_id.id,
                'partner_id': self.partner_id.id,
                'journal_id': journal_id,
                'currency_id': self.x_pricelist_id.currency_id.id,
                'comment': self.note,
                'company_id': self.company_id.id,
                'pricelist_id': self.x_pricelist_id,
                'picking_ids': [(4, self.id)]
        }
        invoice = invoice_obj.create(invoice_vals)
        invoices.append(invoice.id)
        for pack_operation in self.move_line_ids:
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
                tmp_line = invoice_line_obj.new({'product_id': pack_operation.product_id.id, 'invoice_id': invoice.id})
                tmp_line._onchange_product_id()
                invoice_line_vals = {
                    'name': tmp_line.name,
                    'account_id': account.id,
                    'product_id': pack_operation.product_id.id,
                    'uom_id': tmp_line.uom_id.id,
                    'quantity': pack_operation.qty_done,
                    'price_unit': tmp_line.price_unit,
                    'invoice_id':tmp_line.invoice_id.id,
                    'invoice_line_tax_ids': [(6, 0, tmp_line.invoice_line_tax_ids.ids)]
                }
                inv_line = invoice_line_obj.create(invoice_line_vals)
        actions = self.env.ref('account.action_invoice_tree1')
        action_read = actions.read()[0]
        action_read['domain'] = [('id', 'in', invoices)]
        return action_read
