from odoo import models, fields, api
from odoo.tools.float_utils import float_compare
import logging
_logger = logging.getLogger(__name__)


class Orderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    minimum_factor = fields.Float(string='Factor mínimo', default=0)
    maximum_factor = fields.Float(string='Factor máximo', default=0)

    product_qty_min_suggested = fields.Integer(compute='_compute_product_qty_suggested', string='Mínimo sugerido')
    product_qty_max_suggested = fields.Integer(compute='_compute_product_qty_suggested', string='Máximo sugerido')

    @api.depends('rotation', 'minimum_factor', 'maximum_factor')
    def _compute_product_qty_suggested(self):
        # solo calculamos los sugeridos si la rotación es mayor a 0.25 por pedido en personalización
        for rec in self:
            rotation = rec.product_id.get_product_rotation()
            if float_compare(rotation, 0.25, precision_digits=2) >= 0:
                rec.product_qty_min_suggested = int(rotation * rec.minimum_factor)
                rec.product_qty_max_suggested = int(rotation * rec.maximum_factor)
            else:
                rec.product_qty_min_suggested = rec.product_qty_max_suggested = 0

    @api.model
    def cron_update_from_suggested(self):
        _logger.info('Running update max and min from suggested cron')
        orderpoints = self.env['stock.warehouse.orderpoint'].search([])
        if orderpoints:
            orderpoints._update_from_suggested()

    def _update_from_suggested(self):
        for orderpoint in self:
            orderpoint.update({
                'product_min_qty': orderpoint.product_qty_min_suggested,
                'product_max_qty': orderpoint.product_qty_max_suggested,
            })
