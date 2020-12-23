from odoo import models, fields


class XNoVacancySpecificationMotive(models.Model):
    _name = 'x_no_vacancy_specification_motive'
    _description = 'Especificación Motivo No Vacante'

    x_name = fields.Char(string="Name", copy=False)
    x_motive_no_vacancy = fields.Selection(string="Motivo", selection=[('d', 'Diagnóstico'),('pd', 'Posible Diagnóstico'),('se', 'Situación Económica')])
