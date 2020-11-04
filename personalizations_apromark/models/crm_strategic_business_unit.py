from odoo import fields, models


class StrategicBusinessUnit(models.Model):
    _name = 'crm.strategic_business_unit'
    _description = 'Unidad Estratégica de Negocio'

    name = fields.Char(string='Nombre')

