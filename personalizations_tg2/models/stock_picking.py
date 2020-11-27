from odoo import api, models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_account_analytic_id = fields.Many2one(string="Cuenta Analítica", comodel_name="account.analytic.account", on_delete="set null")
    x_analytic_tag_ids = fields.Many2many(string="Etiquetas Analíticas", comodel_name="account.analytic.tag", relation="x_account_analytic_tag_stock_picking_rel", column1="stock_picking_id", column2="account_analytic_tag_id")


    @api.onchange('x_analytic_tag_ids')
    def onchange_x_analytic_tag_ids(self):
        for rec in self.filtered('x_analytic_tag_ids'):
            rec.move_lines.update({'analytic_tag_ids': rec.x_analytic_tag_ids})

    @api.onchange('x_account_analytic_id')
    def onchange_x_account_analytic_id(self):
        for rec in self.filtered('x_account_analytic_id'):
            rec.move_lines.update({'analytic_account_id': rec.x_account_analytic_id})
