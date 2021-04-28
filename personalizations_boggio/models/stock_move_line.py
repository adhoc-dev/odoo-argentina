from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    x_supplier_code = fields.Char(string="Supplier Code", related="product_id.product_tmpl_id.supplier_code", help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.	", readonly=True, copy=False)
    x_product_brand_id = fields.Many2one(string="Marca", related="product_id.product_tmpl_id.product_brand_id", help="	Select a brand for this product", on_delete="set null", readonly=True, copy=False)
    x_internal_code = fields.Char(string="Internal Code", related="product_id.product_tmpl_id.internal_code", readonly=True)
