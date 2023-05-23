from odoo import  models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_plazo_cobro_esperado = fields.Integer(string="Plazo de cobro esperado (días)", store=True)
