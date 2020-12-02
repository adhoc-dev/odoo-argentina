from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self.filered(lambda x: not x.partner_id.sale_type):
            type_id = env['ir.default'].sudo().get('sale.order', 'type_id', company_id=rec.company_id.id, user_id=self.env.user.id)
            if type_id:
                rec.type_id = type_id
