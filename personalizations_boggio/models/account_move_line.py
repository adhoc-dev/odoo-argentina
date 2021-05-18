from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_pricelist_id = fields.Many2one(string="Lista Precios de NV", related="move_id.x_pricelist_id", help="Lista de precios de Nota de venta", on_delete="set null", readonly=True, copy=False)
    x_supplier_code = fields.Char(string="Supplier Code", related="product_id.product_tmpl_id.supplier_code", help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.", readonly=True, translate=True, copy=False)
