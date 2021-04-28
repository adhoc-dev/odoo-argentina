from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_pricelist_id = fields.Many2one(string="Lista Precios de NV", related="invoice_id.x_pricelist_id", help="Lista de precios de Nota de venta", on_delete="set null", readonly=True, copy=False)
