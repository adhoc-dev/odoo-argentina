from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    curso_actual = fields.Many2one(comodel_name='academic.group', string='Curso Actual',
                                   compute="_compute_curso_actual", store=True)

    student_code = fields.Char('Student Code', copy=False)

    _sql_constraints = {
        ('student_code_uniq', 'unique(student_code)',
            'Student Code must be unique!')
    }

    @api.model
    def create(self, vals):
        if vals.get('partner_type') and vals.get('partner_type') == 'student' and not vals.get('student_code', False):
            vals['student_code'] = self.env['ir.sequence'].next_by_code('student.code')
        return super().create(vals)

    @api.depends('student_group_ids')
    def _compute_curso_actual(self):
        for rec in self.filtered('student_group_ids'):
            rec.curso_actual = rec.student_group_ids.sorted('year', reverse=True)[0]