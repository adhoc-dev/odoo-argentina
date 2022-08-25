from odoo import models, api


class SaleSubscriptionLine(models.Model):

    _inherit = "sale.subscription.line"

    @api.onchange('product_id', 'quantity')
    def onchange_product_quantity(self):
        res = super(SaleSubscriptionLine, self).onchange_product_quantity()
        for line in self:
            line.discount = False
            line._onchange_discount()
        return res
