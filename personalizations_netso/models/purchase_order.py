from odoo import api, models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    invoicing_company_id = fields.Many2one('res.company', string="Compañia de Facturacion", required=False)

    @api.onchange('partner_id')
    def _onchange_partner_supplier(self):
        for rec in self.filtered('partner_id'):
            rec.invoicing_company_id = rec.partner_id.supplier_invoicing_company_id
