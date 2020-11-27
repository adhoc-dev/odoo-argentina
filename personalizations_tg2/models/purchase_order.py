from odoo import api, models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_account_analytic_id = fields.Many2one(string="Cuenta Analítica", comodel_name="account.analytic.account", on_delete="set null")
    x_analytic_tag_ids = fields.Many2many(string="Etiquetas Analíticas", comodel_name="account.analytic.tag", relation="x_account_analytic_tag_purchase_order_rel", column1="purchase_order_id", column2="account_analytic_tag_id")


    @api.onchange('x_analytic_tag_ids')
    def onchage_x_analytic_tag_ids(self):
        for rec in self.filtered('x_analytic_tag_ids'):
            rec.order_line.update({'analytic_tag_ids': rec.x_analytic_tag_ids})

    @api.onchange('x_account_analytic_id')
    def onchange_x_account_analytic_id(self):
        for rec in self.filtered('x_account_analytic_id'):
            rec.order_line.update({'account_analytic_id': rec.x_account_analytic_id})
