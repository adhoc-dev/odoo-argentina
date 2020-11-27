from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_account_analytic_id = fields.Many2one(string="Cuenta Analítica", comodel_name="account.analytic.account", on_delete="set null")
    x_analytic_tag_ids = fields.Many2many(string="Etiquetas Analíticas", comodel_name="account.analytic.tag", relation="x_account_analytic_tag_purchase_order_rel", column1="purchase_order_id", column2="account_analytic_tag_id")
