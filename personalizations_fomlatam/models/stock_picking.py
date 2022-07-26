from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    date_etd = fields.Date(string='ETD (Estimated time of departure)')
    date_eta = fields.Date(string='ETA (Estimated time of arrival)')
    purchase_partner_ref = fields.Char(related='purchase_id.partner_ref', string="Referencia de proveedor")
