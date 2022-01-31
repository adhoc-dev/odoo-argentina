from odoo import api, models, fields


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    name = fields.Text(string='Description', required=True)


    @api.onchange('product_id')
    def _onchange_product_id(self):
       super()._onchange_product_id()
       if self.product_id:
           self.name = self.product_id.display_name


    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
        vals = super()._prepare_purchase_order_line(name, product_qty=product_qty, price_unit=price_unit, taxes_ids=taxes_ids)
        if self.purchase_request_lines and self.name:
            vals["name"] = self.name
        return vals
