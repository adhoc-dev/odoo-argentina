from odoo import models, fields


class StockLocation(models.Model):
    _inherit = 'stock.location'

    partner_id = fields.Many2one("res.partner")
