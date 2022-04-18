from odoo import models, fields


class HrJob(models.Model):
    _inherit = 'hr.job'

    seniority_ids = fields.One2many('hr.job.seniority', 'job_id', 'Seniorities')
