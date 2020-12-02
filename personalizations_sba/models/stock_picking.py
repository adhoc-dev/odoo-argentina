from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_studio_field_oowCd = fields.Char(string="Destinatario", copy=False)
