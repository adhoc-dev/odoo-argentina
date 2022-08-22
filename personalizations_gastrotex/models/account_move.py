from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_down_payment = fields.Boolean(string='Es Factura de Anticipo?')

    def _get_concept(self):
        self.ensure_one()
        return '1' if self.is_down_payment else super()._get_concept()

    @api.onchange('invoice_line_ids')
    def is_down_payment_on_change(self):
        down_payment_product = self.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id')
        if down_payment_product and len(self.invoice_line_ids) == 1 and self.invoice_line_ids.product_id.id == int(down_payment_product):
            self.is_down_payment = True
