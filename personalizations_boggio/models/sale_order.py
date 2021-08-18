from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_monto_USD = fields.Float(string="Monto Presupuesto en USD", help="Se graba el monto del presupuesto en dolares IVA incluido", compute='_compute_x_monto_USD', readonly=True, store=True, copy=False)
    x_info_cc = fields.Char(string="Info CC", readonly=True, copy=False)
    total_overdue = fields.Monetary(related="partner_id.total_overdue")

    @api.depends('state', 'currency_id','amount_total')
    def _compute_x_monto_USD(self):
        for rec in self.filtered(lambda s: s.state == 'draft'):
            USD_currency = self.env.ref('base.USD')
            rec.x_monto_USD = rec.currency_id._convert(rec.amount_total, USD_currency, rec.company_id, fields.Date.today())

    def open_action_followup(self):
        self.ensure_one()
        return {
            'name': _("Overdue Payments for %s") % self.partner_id.display_name,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [[self.env.ref('account_followup.customer_statements_form_view').id, 'form']],
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
        }

    def get_data_products(self):
        list_product=[]
        for line in self.mapped('order_line'):
            list_product.append((line.product_id, line.product_uom_qty))
        return list_product
