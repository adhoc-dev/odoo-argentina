from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_studio_field_708EL = fields.Many2one(string="Cuenta Analítica ", comodel_name="account.analytic.account", on_delete="set null", copy=False)
