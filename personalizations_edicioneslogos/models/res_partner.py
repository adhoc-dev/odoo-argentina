from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_colegio = fields.Text(string="Colegio", help="Institución correspondiente al partner.")
    x_project_ids = fields.One2many(string="Proyectos", comodel_name="x_partner_project", inverse_name="x_partner_id")

    @api.onchange('user_id')
    def update_tags(self):
        old_user = self._origin.user_id
        if old_user != self.user_id and self.user_id.id == 59 and self.property_product_pricelist.id != 33:
            self.category_id = [(4, 11, 0)]
