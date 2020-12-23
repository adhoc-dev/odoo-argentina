from odoo import models, fields


class XAccountOverdueType(models.Model):
    _name = 'x_account_overdue_type'
    _description = 'Tipos de mora'

    name = fields.Char(string="Causa de Mora")

