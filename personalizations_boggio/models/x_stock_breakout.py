from odoo import models, fields


class XStockBreakout(models.Model):
    _name = 'x_stock_breakout'
    _description = 'Roturas de Stock'
    _inherit = ['mail.thread']
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", copy=False)
    x_stock = fields.Float(string="Stock en la empresa")
    x_stock_central = fields.Float(string="Stock Central")
    x_stk_min = fields.Float(string="Stock Minimo Central", help="Stock min Rosario")
    x_stk_max = fields.Float(string="Stock Maximo Central")
    x_state = fields.Integer(string="Estado", help="0: sin analisis, 10: terminado y corredigo. 1: cancelado, 2: error de stock, 9: revisado sin correccion")
    x_product_id = fields.Many2one(string="Producto", comodel_name="product.product", on_delete="set null")
    x_reason = fields.Char(string="Motivo en Compras", help="Motivo del problema")
    x_product_brand_id = fields.Many2one(string="Marca", related="x_product_id.product_tmpl_id.product_brand_id", help="Select a brand for this product", on_delete="set null", readonly=True, copy=False, store=True)
    x_rotation = fields.Float(string="Rotacion", copy=False)
    x_rotation_central = fields.Float(string="Rotacion Central", copy=False)
    x_abc = fields.Char(string="ABC")
