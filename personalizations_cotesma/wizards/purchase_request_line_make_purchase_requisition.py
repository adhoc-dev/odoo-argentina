
from odoo import api, models


class PurchaseRequestLineMakePurchaseRequisition(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.requisition"

    def make_purchase_requisition(self):
        res = super().make_purchase_requisition()
        active_model = self.env.context.get("active_model")
        if active_model == "purchase.request":
            request_ids = self.env.context.get("active_ids")
            if len(request_ids) == 1:
                request = self.env["purchase.request"].browse(request_ids)
                self.env['purchase.requisition'].search(eval(res['domain'])).priority = request.priority
        return res

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
