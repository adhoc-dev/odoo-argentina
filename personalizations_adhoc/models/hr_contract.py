from odoo import models, fields, api
from odoo.exceptions import UserError


class HrContract(models.Model):

    _inherit = 'hr.contract'

    seniority_id = fields.Many2one('hr.seniority')
    wage = fields.Monetary(compute='_compute_wage', store=True, readonly=False)

    @api.depends('seniority_id', 'job_id.seniority_ids.salary_category_id.amount')
    def _compute_wage(self):
        for rec in self.filtered(lambda x: x.seniority_id and x.job_id and x.state in ['draft', 'open']):
            # TODO search
            job_seniority_salary_category = rec.env['hr.job.seniority'].search(
                [('seniority_id', '=', rec.seniority_id.id), ('job_id', '=', rec.job_id.id)], limit=1)
            if not job_seniority_salary_category:
                raise UserError('No encontramos una categoría de salario para el puesto %s y seniority %s' % (
                    rec.job_id.name, rec.seniority_id.name))
            rec.wage = job_seniority_salary_category.salary_category_id.currency_id._convert(
                job_seniority_salary_category.salary_category_id.amount, rec.currency_id,
                rec.company_id, fields.Date.today())
