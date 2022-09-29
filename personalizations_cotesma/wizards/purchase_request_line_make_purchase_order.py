from odoo import api, models

class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    @api.model
    def _prepare_item(self, line):
        res = super()._prepare_item(line)
        res['keep_description'] = True
        return res

    def make_purchase_order(self):
        res = super().make_purchase_order()
        active_model = self.env.context.get("active_model")
        if active_model == "purchase.request":
            request_ids = self.env.context.get("active_ids")
            if len(request_ids) == 1:
                request = self.env["purchase.request"].browse(request_ids)
                self.env['purchase.order'].search(res['domain']).priority = request.priority
        return res
