from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    x_budget_line_ids = fields.One2many(string="Líneas de Presupuesto", comodel_name="account.analytic.line", inverse_name="account_id", domain=[('x_presupuestado', '=', True)])


    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """ We need to show all the childs when you search by the parent name"""
        analytic_ids = super(AccountAnalyticAccount, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
        analytics  = self.browse(analytic_ids).mapped('child_ids')
        if analytics:
            analytic_ids.extend(analytics.ids)
        return analytic_ids
