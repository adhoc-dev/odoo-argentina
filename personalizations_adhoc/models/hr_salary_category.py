from odoo import models, fields, api, tools


class HrSalaryCategory(models.Model):
    _name = 'hr.salary_category'
    _description = 'hr.salary_category'
    _order = 'name'

    name = fields.Char(required=True)
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one('res.currency', required=True)
    job_seniority_ids = fields.One2many('hr.job.seniority', 'salary_category_id', 'Job/Seniorities')

    @api.depends('amount', 'currency_id')
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s (%s)' % (
                rec.name,
                tools.format_amount(self.env, rec.amount, rec.currency_id, rec.env.lang),)))
        return result
