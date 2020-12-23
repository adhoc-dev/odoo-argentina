##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models



class AcademicGroup(models.Model):
    _inherit = 'academic.group'
    _order = "company_id asc, year desc, division_id asc, level_id asc"

    def next_year(self):
        #Busco si el proximo nivel está dentro de los niveles del plan de estudio, si no está entonces el curso egresa
        for rec in self:
            if rec.level_id in rec.study_plan_level_ids and \
              rec.study_plan_level_ids.ids.index(rec.level_id.id) + 1 < len(rec.study_plan_level_ids):
                next_level = rec.study_plan_level_ids[rec.study_plan_level_ids.ids.index(rec.level_id.id) + 1]
                next_group = rec.env['academic.group'].search([
                    ('year','=',rec.year+1),('company_id','=',rec.company_id.id),
                    ('level_id','=',next_level.id),('division_id','=',rec.division_id.id)], limit=1)
                if not next_group:
                    next_group = rec.env['academic.group'].create({
                        'year': rec.year+1,
                        'division_id': rec.division_id.id,
                        'level_id': next_level.id,
                        'company_id': rec.company_id.id
                    })
                if next_group:
                    next_group.update({
                        'student_ids': [(4, x.id) for x in rec.student_ids.filtered('x_matricula')]
                    })
