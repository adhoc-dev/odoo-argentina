# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, api
from odoo.tools import config


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(PurchaseOrderLine, self).create(vals_list)
        for line in lines:
            ov = self.env["sale.order"].search([('name', '=', line.order_id.origin)])
            if ov:
                ov_lines = ov.order_line.filtered(lambda x:x.product_id == line.product_id)
                for ov_line in ov_lines:
                    line.name = ov_line.name
                    line.price_unit = ov_line.purchase_price
        return lines
