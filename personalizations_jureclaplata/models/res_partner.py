from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    curso_actual = fields.Many2one(comodel_name='academic.group', string='Curso Actual',
                                   compute="_compute_curso_actual", store=True)

    @api.depends('student_group_ids')
    def _compute_curso_actual(self):
        for rec in self.filtered('student_group_ids'):
           rec.curso_actual = rec.student_group_ids.sorted('year', reverse=True)[0]
