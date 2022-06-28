from odoo import models, fields


class XTipoinsta(models.Model):
    _name = 'x_tipoinsta'
    _description = 'Tipo Instalación'
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", required=True, copy=False)
