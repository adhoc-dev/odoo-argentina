from odoo import models, fields, api


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    x_seller_id = fields.Many2one(string="Main Seller	", related="product_id.product_tmpl_id.main_seller_id", help="Vendor of this product	", on_delete="set null", readonly=True, copy=False)
    x_supplier_code = fields.Char(string="Supplier Code	", related="product_id.product_tmpl_id.supplier_code", help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.", readonly=True, translate=True, copy=False)
    x_qty_available = fields.Float(string="Stock en Mano	", related="product_id.qty_available", help="Current quantity of products."
"In a context with a single Stock Location, this includes goods stored at this Location, or any of its children."
"In a context with a single Warehouse, this includes goods stored in the Stock Location of this Warehouse, or any of its children."
"stored in the Stock Location of the Warehouse of this Shop, or any of its children."
"Otherwise, this includes goods stored in any Stock Location with 'internal' type.", readonly=True, copy=False)
    x_brand = fields.Char(string="Marca", related="product_id.product_brand_id.name", readonly=True)
    x_virtual_available = fields.Float(string="Cantidad prevista", related="product_id.virtual_available", help="Cantidad prevista (calculada como cantidad a mano - saliente + entrante)"
"En un contexto de una sola ubicación de existencias, esto incluye los bienes almacenados en esta ubicación, o cualquiera de sus hijas."
"En un contexto de un solo almacén, esto incluye los bienes almacenados en la ubicación de existencias de ese almacén, o cualquiera de sus hijas."
"En cualquier otro caso, esto incluye los bienes almacenados en cualquier ubicación de existencias de tipo 'Interna'.", readonly=True, copy=False)
    x_abc_sales_combined = fields.Char(string="ABC Ventas combinadas	", related="product_id.product_tmpl_id.abc_sales_combined", readonly=True, copy=False)
    x_red_security = fields.Integer(string="Rojo Seguridad", help="Rojo seguridad", readonly=True, copy=False)
    x_tor = fields.Integer(string="TOR: Tope de Rojo", readonly=True, copy=False)
    x_stddev_lead_days = fields.Float(string="Desvio Estandar Dias", readonly=True, copy=False)
    x_toy = fields.Float(string="TOY: Tope de Amarillo", readonly=True, copy=False)
    x_tog = fields.Float(string="TOG: Tope de Verde", readonly=True, copy=False)
    x_frec_compra = fields.Integer(string="Frecuencia Compra", help="Frecuencia de compra", readonly=True, copy=False)
    x_origen_compra = fields.Char(string="Origen Compra", help="P: proveedor"
"I: interno (Sucursales)", readonly=True, copy=False)
    x_color_stock = fields.Char(string="Color de Stock", readonly=True, copy=False)
    x_date_act = fields.Date(string="Fecha Actualizacion Estadistica", help="Fecha de actualizacion de datos de tiempos de entrega, estc", readonly=True, copy=False)
    x_estrategia = fields.Integer(string="Estrategia", help="0: no definido, 1: stock manual,  2: stock automático (frec compra  en proveedor y tiempos de filtrado?proveedor? ) 4. Stock min manual y máximo automático")
    x_aux = fields.Char(string="aux", readonly=True, copy=False)
    x_rotacion = fields.Float(string="ROTACION IR", compute="_compute_x_rotacion", readonly=True, copy=False)
    x_rotacion_warehouse = fields.Float(string="ROTACION IR local", compute="_compute_x_rotacion_warehouse", readonly=True, copy=False)

    @api.depends('rotation','product_id')
    def _compute_x_rotacion(self):
        for record in self:
            record['x_rotacion'] = (record.product_id.virtual_available>0.0 and record.rotation*12.0/record.product_id.virtual_available or 6.66)

    @api.depends('rotation','product_id','warehouse_id')
    def _compute_x_rotacion_warehouse(self):
        for record in self:
            record['x_rotacion_warehouse'] = (record.product_id.with_context(warehouse=record.warehouse_id.id).virtual_available>0.0 and record.warehouse_rotation*12.0/record.product_id.with_context(warehouse=record.warehouse_id.id).virtual_available or 6.66)
