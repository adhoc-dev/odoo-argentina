from odoo import models, fields


class ResPartnerIndustry(models.Model):
    _inherit = 'res.partner.industry'

    x_objetivos = fields.Boolean(string="Objetivo")
