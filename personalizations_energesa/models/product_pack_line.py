from odoo import models, fields, api


class ProductPackLine(models.Model):
    _inherit = 'product.pack.line'

    x_product_template_standard_price = fields.Float(string="Costo contable", related="product_id.standard_price_copy", help="Cost used for stock valuation in standard price and as a first price to set in average/fifo. Also used as a base price for pricelists. Expressed in the default unit of measure of the product. ", readonly=True, copy=False, store=True)
    x_subtotal = fields.Float(string="Costo Total", compute="_compute_x_subtotal", track_visibility="always", readonly=True, copy=False, store=True)

    @api.depends('quantity','x_product_template_standard_price')
    def _compute_x_subtotal(self):
        for rec in self:
          rec['x_subtotal'] = rec.quantity * rec.x_product_template_standard_price
