from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_sale_order_line_multiline_description_variants(self):
        if self.product_id.barcode:
            return '\n ISBN: ' + self.product_id.barcode
        return ''
