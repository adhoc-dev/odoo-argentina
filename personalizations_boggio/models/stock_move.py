from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    x_product_brand_id = fields.Many2one(string="Brand", related="product_id.product_tmpl_id.product_brand_id", help="	Select a brand for this product	", on_delete="set null", readonly=True, copy=False)
    x_supplier_code = fields.Char(string="Supplier Code	", related="product_id.product_tmpl_id.supplier_code", help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.		", readonly=True, translate=True, copy=False)
    x_oc_create_uid = fields.Many2one(string="Usuario creado OC", related="purchase_id.create_uid", on_delete="set null", readonly=True, copy=False)
    x_so_create_uid = fields.Many2one(string="Usuario Creado OV", related="sale_id.create_uid", on_delete="set null", readonly=True, copy=False)
