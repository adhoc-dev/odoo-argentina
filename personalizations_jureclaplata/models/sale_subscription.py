from odoo import models, fields, api


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    student_id = fields.Many2one('res.partner', string='Alumno', domain="[('parent_id', '=', partner_id), ('partner_type', '=', 'student')]")
    curso_actual = fields.Many2one(comodel_name='academic.group', string='Curso Actual',
                                   compute="_compute_curso_actual")

    @api.depends('student_id')
    def _compute_curso_actual(self):
        for rec in self:
            if (not rec.student_id):
                rec.curso_actual = False
            else:
                rec.curso_actual = rec.student_id.curso_actual

