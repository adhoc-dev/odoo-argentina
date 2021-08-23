from odoo import models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if self.analytic_account_id:
            default['analytic_account_id'] = self.analytic_account_id.copy().id
        return super().copy(default)

    @api.onchange('name')
    def onchange_name_account_analytic_id(self):
        if self.analytic_account_id and self.analytic_account_id.name != self.name:
            self.analytic_account_id.name = self.name
