from odoo import models, fields, api


class PurchaseSuggest(models.TransientModel):
    _inherit = 'purchase.suggest'

    x_product_code = fields.Char(string="Código Proveedor", related="product_id.seller_ids.product_code", help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.", readonly=True, copy=False)
    x_abc_sales_combined = fields.Char(string="ABC Ventas combinadas", related="product_id.product_tmpl_id.abc_sales_combined", readonly=True, copy=False)
    x_product_brand_id = fields.Many2one(string="Brand", related="product_id.product_tmpl_id.product_brand_id", help="Select a brand for this product", on_delete="set null", readonly=True, copy=False)
    x_user_id = fields.Many2one(string="Comercial", related="seller_id.user_id", help="The internal user that is in charge of communicating with this contact if any.", on_delete="set null", readonly=True)
    x_qty_available = fields.Float(string="Stock Boggio", related="product_id.qty_available", help="Stock de toda la empresa", readonly=True, copy=False)
    x_lead_days = fields.Integer(string="Tiempo de entrega", related="orderpoint_id.lead_days", help="Lead days", readonly=True, copy=False)
    x_marca = fields.Char(string="Marcas", related="product_id.product_tmpl_id.product_brand_id.name", readonly=True, copy=False)
    x_dias_stock_location = fields.Float(string="Dias Stock Ubica", compute="_compute_x_dias_stock_location", help="Stock Virtual / rotacion de la ubicacion", readonly=True, copy=False)
    x_unidad_empaque = fields.Char(string="U.E.", related="product_id.quantity_per_pack", readonly=True, copy=False)

    @api.depends('warehouse_rotation')
    def _compute_x_dias_stock_location(self):
        for record in self:
            record['x_dias_stock_location'] = (record.warehouse_rotation>0 and record.virtual_available/record.warehouse_rotation*30.0 or 999.9 )
