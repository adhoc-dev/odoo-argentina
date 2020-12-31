from odoo import models, fields


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    x_studio_field_NfgZy = fields.Many2many(string="Etiquetas analíticas", comodel_name="account.analytic.tag",
                                            relation="x_account_analytic_tag_hr_expense_rel", column1="hr_expense_id",
                                            column2="account_analytic_tag_id", on_delete="cascade", copy=False)
