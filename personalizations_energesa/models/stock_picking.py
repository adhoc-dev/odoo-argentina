from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_studio_field_cbfA4 = fields.Many2one(string="OV Vinculada", related="group_id.sale_id", on_delete="set null", readonly=True, copy=False, store=True)
    x_plantilla = fields.Boolean(string="Es plantilla estándar", copy=False)
    x_sale_order_team_id = fields.Many2one(string="Canal de ventas", related="sale_id.team_id", on_delete="set null", readonly=True, copy=False, store=True)
    x_total_standard_price = fields.Float(string="Costo Total", compute="_compute_x_total_standard_price", track_visibility="always", readonly=True, copy=False, store=True)

    @api.depends('move_lines','__last_update','state')
    def _compute_x_total_standard_price(self):
        for rec in self:
            total = 0
            for line in rec.move_lines:
                total += line.quantity_done * line.x_standard_price
            rec['x_total_standard_price'] = total
