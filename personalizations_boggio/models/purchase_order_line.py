from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_product_brand_id = fields.Many2one(string="Brand", related="product_id.product_tmpl_id.product_brand_id", help="Select a brand for this product", on_delete="set null", readonly=True, copy=False)
    x_location_id = fields.Many2one(string="Ubicación", related="product_id.location_id", on_delete="set null", readonly=True)
    x_qty_available = fields.Float(string="Stock en Mano", related="product_id.qty_available", help="Current quantity of products."
"In a context with a single Stock Location, this includes goods stored at this Location, or any of its children."
"In a context with a single Warehouse, this includes goods stored in the Stock Location of this Warehouse, or any of its children."
"stored in the Stock Location of the Warehouse of this Shop, or any of its children."
"Otherwise, this includes goods stored in any Stock Location with 'internal' type.", readonly=True, copy=False)
    x_virtual_available = fields.Float(string="Stock Virtual", related="product_id.virtual_available", help="Forecast quantity (computed as Quantity On Hand - Outgoing + Incoming)"
"In a context with a single Stock Location, this includes goods stored in this location, or any of its children."
"In a context with a single Warehouse, this includes goods stored in the Stock Location of this Warehouse, or any of its children."
"Otherwise, this includes goods stored in any Stock Location with 'internal' type.", readonly=True, copy=False)
    x_supplier_code = fields.Char(string="Supplier Code", related="product_id.product_tmpl_id.supplier_code", help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.", readonly=True, translate=True, copy=False)
