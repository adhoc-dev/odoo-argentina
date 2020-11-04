from odoo import fields, models


class CreditCard(models.Model):
    _name = 'res.partner.credit_card'
    _description = 'Tarjeta de Crédito'

    name = fields.Char(string='Tipo')
