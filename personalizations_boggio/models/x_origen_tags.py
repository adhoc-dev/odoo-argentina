from odoo import models, fields


class XOrigenTags(models.Model):
    _name = 'x_origen_tags'
    _description = 'origen no conformidad'

    x_name = fields.Char(string="Nombre", required=True)
