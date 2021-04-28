from odoo import models, fields


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    x_studio_field_5L26y = fields.Char(string="Codigo proveedor", related="replenishment_cost_rule_id.product_ids.supplier_code", help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.", readonly=True, copy=False)
