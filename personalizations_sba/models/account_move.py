from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
import dateutil


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_fecha_segundo_venc = fields.Date(string="Fecha segundo vencimiento", compute="_compute_x_fecha_segundo_venc", help="Es la fecha del segundo vencimiento de la factura", readonly=True, copy=False, store=True)
    x_invoice_nd_id = fields.Many2one(string="ND relacionada", comodel_name="account.move", on_delete="set null", readonly=True, copy=False)
    x_monto_cargo = fields.Monetary(string="Importe con recargo", compute="_compute_x_monto_cargo", readonly=True, copy=False, store=True)
    x_state_invoice = fields.Selection(string="Estado de vencimiento de factura", selection=[('vencida', 'Vencida'),('vencida_sin_nd', 'Vencida sin ND emitida'),('no_vencida', 'No vencida')], compute="_compute_x_state_invoice", readonly=True, copy=False, store=True)

    @api.depends('date_due','date_invoice')
    def _compute_x_fecha_segundo_venc(self):
        for rec in self:
          if rec.date_due:
            date = datetime.strptime(rec.date_due, "%Y-%m-%d") + dateutil.relativedelta.relativedelta(days=rec.company_id.x_rango_fecha_recargo)
            rec.x_fecha_segundo_venc = datetime.strftime(date, "%Y-%m-%d")
          else:
            rec.x_fecha_segundo_venc = False

    @api.depends('sale_order_ids', 'amount_total')
    def _compute_x_monto_cargo(self):
        for rec in self.filtered('sale_order_ids'):
            rec.x_monto_cargo = rec.amount_total * (1 + (rec.sale_order_ids[0].pricelist_id.x_porcentaje_cargo_extra) / 100)

    @api.depends('date_due', 'x_invoice_nd_id', 'state')
    def _compute_x_state_invoice(self):
        for rec in self:
          x_state_invoice = 'no_vencida'
          if rec.state != 'open':
            rec.x_state_invoice = x_state_invoice
            continue
          if rec.date_due < fields.Date.today():
            x_state_invoice = 'vencida'
          if x_state_invoice == 'vencida' and not rec.x_invoice_nd_id:
            x_state_invoice = 'vencida_sin_nd'
          rec.x_state_invoice = x_state_invoice

    def create_debt_invoice(self):
        def prepare_interest_invoice(partner, amount, journal):
            comment = "Recargo por mora de la factura {}".format(self.document_number)
            account_id = self.account_id.id or partner.property_account_receivable_id.id

            invoice_vals = {
                'type': 'out_invoice',
                'partner_id': partner.id,
                'journal_id': journal.id,
                'narration': comment,
                'invoice_origin': self.document_number,
                'currency_id': self.company_id.currency_id.id,
                'invoice_payment_term_id': partner.property_payment_term_id.id or False,
                'fiscal_position_id': partner.property_account_position_id.id,
                'invoice_date': fields.Date.today(),
                'company_id': self.company_id.id,
                'invoice_user_id': partner.user_id.id or False
            }
            return invoice_vals

        def prepare_interest_invoice_line(invoice, partner, amount):
            company = self.company_id
            try:
              product = self.env['product.product'].browse(PRODUCT_ID)
            except Exception:
              raise UserError("No tienen configurado el producto")
            line_values = {}
            line_data = self.env['account.move.line'].with_context(
                force_company=company.id).new(dict(
                    product_id=PRODUCT_ID,
                    quantity=1.0,
                    move_id=invoice.id,
                    partner_id=partner.id,
                ))
            line_data._onchange_product_id()

            if not line_data.account_id:
                raise UserError(
                    'El producto {} no esta correctamente configurado, falta la cuenta contable.'.format(product.name))

            line_data['price_unit'] = amount
            line_data['name'] = line_data.product_id.name + '.\n' + invoice.comment


            for field in line_data._cache:
              line_values[field] = line_data[field]
            values = line_data._convert_to_write(line_values)
            return values

        def create_invoice():
            partner = self.partner_id
            amount = self.x_monto_cargo - self.amount_total
            journal = self.journal_id
            invoice_vals = prepare_interest_invoice(partner, amount, journal)
            invoice = self.with_context(internal_type='debit_note').create(invoice_vals)

            self.env['account.move.line'].create(prepare_interest_invoice_line(invoice, partner, amount))
            invoice.compute_taxes()
            invoice.message_post(body="Factura de recargo por mora creada de la factura {}".format(self.document_number))
            return invoice
        self.ensure_one()
        PRODUCT_ID = int(self.env['ir.config_parameter'].sudo().get_param('product.nd_mora'))
        invoice = create_invoice()
        self.x_invoice_nd_id = invoice
        actions = self.env.ref('account.action_invoice_tree1')
        action_read = actions.read()[0]
        res = self.env.ref('account.invoice_form', False)
        action_read['views'] = [(res and res.id or False, 'form')]
        action_read['res_id'] = invoice.id
        return action_read
