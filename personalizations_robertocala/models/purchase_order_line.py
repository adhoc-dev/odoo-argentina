from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_replenishment_base_cost_on_currency = fields.Float(string="Costo base de reposición en Moneda", related="product_id.replenishment_base_cost_on_currency", help="Base price to compute the customer price. Sometimes called the catalog price.", readonly=True, copy=False)
