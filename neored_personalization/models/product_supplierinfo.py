from odoo import models, fields


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    product_code_2 = fields.Char('Código de Producto 2')
    # por defecto quieren compartir los precios de distintos proveedores. Esto ademas es importante
    # para que cuando se sincroniza de catalogo a cada distribuidor se creen bien sin compañia
    company_id = fields.Many2one(default=False)
