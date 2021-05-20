from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_monto_USD = fields.Float(string="Monto Presupuesto en USD", help="Se graba el monto del presupuesto en dolares IVA incluido", compute='_compute_x_monto_USD', readonly=True, store=True, copy=False)
    x_info_cc = fields.Char(string="Info CC", readonly=True, copy=False)

    @api.depends('state', 'currency_id','amount_total')
    def _compute_x_monto_USD(self):
        for rec in self.filtered(lambda s: s.state == 'draft'):
            USD_currency = self.env.ref('base.USD')
            rec.x_monto_USD = rec.currency_id._convert(rec.amount_total, USD_currency, rec.company_id, fields.Date.today())
