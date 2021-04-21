from odoo import models, fields


class XTipoinsta(models.Model):
    _name = 'x_tipoinsta'
    _description = 'Tipo Instalación'

    x_name = fields.Char(string="Name", required=True, copy=False)
