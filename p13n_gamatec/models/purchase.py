# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, api
from odoo.tools import config


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(PurchaseOrderLine, self).create(vals_list)
        if lines.order_id:
            ov_name = lines.order_id.origin
            if ov_name:
                ov = self.env["sale.order"].search([('name','=',ov_name)])
                if ov:
                    custom_line = ov.order_line.filtered(lambda x:x.product_id == lines.product_id)
                    if custom_line:
                        try:
                            lines.name = custom_line.name
                            lines.price_unit = custom_line.purchase_price
                        except:
                            pass
        return lines
