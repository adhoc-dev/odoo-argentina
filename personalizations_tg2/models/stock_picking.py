from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_account_analytic_id = fields.Many2one(string="Cuenta Analítica", comodel_name="account.analytic.account", on_delete="set null")
    x_analytic_tag_ids = fields.Many2many(string="Etiquetas Analíticas", comodel_name="account.analytic.tag", relation="x_account_analytic_tag_stock_picking_rel", column1="stock_picking_id", column2="account_analytic_tag_id")
