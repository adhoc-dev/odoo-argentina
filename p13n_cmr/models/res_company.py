from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    cbu_company = fields.Char()
