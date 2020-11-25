from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_colegio = fields.Text(string="Colegio", help="Institución correspondiente al partner.")
    x_product_pricelist = fields.Many2one(string="Precio de lista", related="property_product_pricelist", help="This pricelist will be used, instead of the default one, for sales to the current partner", on_delete="set null", readonly=True, store=True)
    x_project_ids = fields.One2many(string="Proyectos", comodel_name="x_partner_project", inverse_name="x_partner_id")
