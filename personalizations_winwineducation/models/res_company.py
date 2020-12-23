from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    x_prueba_imagen = fields.Html(string="prueba")
