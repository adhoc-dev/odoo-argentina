from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    x_ajuste_lista = fields.Float(string="Ajuste de Lista", help="ajuste de lista para calculo automatico de descuento por volumen", copy=False)
    x_desc_max = fields.Float(string="Descuento maximo a Mayorista", help="Descuento que tiene la lista hasta mayorista", copy=False)
    x_venta_min = fields.Float(string="Venta Minima lista cc", help="Venta minima para lista de cuenta corriente", copy=False)
    x_venta_max = fields.Float(string="Venta Maxima lista cc", help="Venta Maxima para lista en cuenta corriente", copy=False)
