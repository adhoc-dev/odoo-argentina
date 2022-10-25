from datetime import date
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    curso_actual = fields.Many2one(comodel_name='academic.group', string='Curso Actual',
                                   compute="_compute_curso_actual", store=True)

    student_code = fields.Char('Student Code', copy=False, size=5)
    red_link_id_deuda = fields.Integer(
        'ID Deuda a Informar (Red Link)', default=1, company_dependent=True,
        help='Campo Tecnico: Numero Volumen usado de Red Link (por dia)')

    _sql_constraints = [
        ('student_code_uniq', 'unique(student_code, company_id)',
            'Student Code must be unique per company!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('partner_type') and vals.get('partner_type') == 'student' and not vals.get('student_code', False):
            vals['student_code'] = self.env['ir.sequence'].next_by_code('student.code')
        return super().create(vals)

    @api.depends('student_group_ids')
    def _compute_curso_actual(self):
        for rec in self.filtered('student_group_ids'):
            cursos = rec.student_group_ids.sorted(key=lambda r: r.year, reverse=True)
            cursos_filtrados = cursos.filtered(lambda r: r.year <= date.today().year)
            if cursos_filtrados:
                rec.curso_actual = cursos_filtrados[0]
            else:
                rec.curso_actual = cursos[0]
