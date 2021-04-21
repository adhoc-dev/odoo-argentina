from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_pr_group_id = fields.Many2one(string="Grupo de abastecimeinto", related="order_id.group_id", on_delete="set null", readonly=True, copy=False, store=True)
