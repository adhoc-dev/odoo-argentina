from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_product_brand_id = fields.Many2one(string="Brand", related="product_id.product_tmpl_id.product_brand_id", help="Brand", on_delete="set null", readonly=True, copy=False)
    x_so_create_uid = fields.Many2one(string="Usuario Creador OV", related="sale_id.create_uid", on_delete="set null", readonly=True, copy=False)
    x_user_id = fields.Many2one(string="Preparador asignado", comodel_name="res.users", help="Usuario asignado por el jefe de logística, o responsable de deposito en cuestión, para que prepare el pedido.", on_delete="set null")
    x_write_uid2 = fields.Many2one(string="Preparador real", comodel_name="res.users", help="Usuario real que preparo el pedido", on_delete="set null")
    x_razon_devolucion = fields.Many2one(string="Razon de la devolucion", comodel_name="x_devolucion_tags.devolucion_tags", on_delete="set null", copy=False)
    x_studio_field_T8yfU = fields.Char(string="Tipo de venta", related="sale_id.type_id.name", readonly=True, translate=True, copy=False)
    x_plazo_pago = fields.Char(string="Plazo de Pago", related="sale_id.payment_term_id.display_name", readonly=True, copy=False)
    x_rpa_link = fields.Char(string="RPA Link Remito Firmado", help="Enlace del remito firmado subido por RPA", copy=False)
