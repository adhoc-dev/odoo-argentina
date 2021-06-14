##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        super()._onchange_quantity()
        if not self.product_id:
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(
            self.product_id.replenishment_cost, self.product_id.supplier_taxes_id,
            self.taxes_id, self.company_id) if self.product_id.replenishment_cost else 0.0

    # Acá compara la moneda de la orden con la moneda del producto
        if price_unit and self.\
                order_id.currency_id and self.product_id.\
                currency_id != self.order_id.currency_id:
            price_unit = self.product_id.currency_id._convert(
                price_unit, self.order_id.currency_id,
                self.order_id.company_id,
                self.order_id.date_order or fields.Date.today())
    # # Compara si hay uom y si esa uom es distinta a la del producto
        if self.product_uom and self.product_id.\
                uom_id != self.product_uom:
            price_unit = self.product_id.uom_id._compute_price(
                price_unit, self.product_uom)
        self.price_unit = price_unit
