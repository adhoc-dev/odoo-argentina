from odoo import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    x_supplier_code = fields.Char(string="Supplier Code", related="product_id.product_tmpl_id.supplier_code", help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.", readonly=True, translate=True, copy=False)
