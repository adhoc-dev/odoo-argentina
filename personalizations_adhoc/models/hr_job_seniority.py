from odoo import models, fields, api


class HrJobSenioritySalaryCategory(models.Model):
    _name = 'hr.job.seniority'
    _description = 'Salary categories per Job and Seniority'
    _order = 'salary_category_id'

    job_id = fields.Many2one('hr.job', required=True)
    seniority_id = fields.Many2one('hr.seniority', required=True)
    description = fields.Text()
    salary_category_id = fields.Many2one('hr.salary_category', required=True)

    _sql_constraints = [
        ('unique_salary_category', 'unique (job_id, seniority_id)', 'There must be only one job / seniority relation')
    ]

    @api.depends('job_id', 'seniority_id')
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.job_id.name, rec.seniority_id.name)))
        return result
