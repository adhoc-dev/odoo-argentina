from odoo import fields, models


class Location(models.Model):
    _name = 'crm.location'
    _description = 'Lugar'

    name = fields.Char(string='Nombre')
