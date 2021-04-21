from odoo import models, fields


class XInstaladores(models.Model):
    _name = 'x_instaladores'
    _description = 'Instaladores'

    x_name = fields.Char(string="Name", required=True, copy=False)
