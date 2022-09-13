from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        if self.is_purchase_document():
            self.sudo().with_context(only_type_product=True).update_prices_with_supplier_cost()
        return super().action_post()

    def get_product_lines_to_update(self):
        lines = super().get_product_lines_to_update()
        if self.env.context.get('only_type_product'):
            lines = lines.filtered(lambda x: x.product_id.type == 'product')
        return lines
