
from odoo import api, models


class PurchaseRequestLineMakePurchaseRequisition(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.requisition"

    @api.model
    def _prepare_purchase_requisition_line(self, pr, item):
        vals = super()._prepare_purchase_requisition_line(pr, item)
        vals["name"] = item.name
        return vals


    @api.model
    def _get_requisition_line_search_domain(self, requisition, item):
        vals = super()._get_requisition_line_search_domain(requisition, item)
        if item.name:
            vals.append(("name", "=", item.name))
        return vals
