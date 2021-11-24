from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_subscription_data(self, template):
        """ Add the tags from the order lines to the values to create the subscription. """
        values = super()._prepare_subscription_data(template)
        tags = []
        for line in self.order_line.filtered(lambda l: l.product_id.subscription_template_id == template and l.product_id.recurring_invoice):
            tags += line.analytic_tag_ids.ids
        values['tag_ids'] = [(6, 0, tags)]
        return values
