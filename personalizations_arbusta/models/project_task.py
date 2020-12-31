from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    x_studio_field_J1l99 = fields.Char(string="URL de Calendar", copy=False)
    x_studio_field_sFveY = fields.Selection(string="Tipo de evento",
                                            selection=[('desayunar', 'desayunar'), ('merendar', 'merendar')],
                                            copy=False)
    x_studio_field_2WN1e = fields.Float(string="GDR Factor", copy=False)
    x_studio_field_dbSFl = fields.Selection(string="GDR Probabilidad",
                                            selection=[('Poco probable que ocurra', 'Poco probable que ocurra'),
                                                       ('Algo probable que ocurra', 'Algo probable que ocurra'),
                                                       ('Probable que ocurra', 'Probable que ocurra'),
                                                       ('Es muy probable que ocurra', 'Es muy probable que ocurra')],
                                            copy=False)
    x_studio_field_YGJ8m = fields.Selection(string="GDR Ocurrencias previas",
                                            selection=[('Nunca se ha producido', 'Nunca se ha producido'),
                                                       ('No se ha producido en los últimos 10 años',
                                                        'No se ha producido en los últimos 10 años'),
                                                       ('Se ha producido en los últimos 10 años',
                                                        'Se ha producido en los últimos 10 años'),
                                                       ('Se ha producido en los últimos 5 años',
                                                        'Se ha producido en los últimos 5 años'),
                                                       ('Se ha producido en el último año',
                                                        'Se ha producido en el último año')],
                                            copy=False)
    x_studio_field_v7s4v = fields.Selection(string="GDR Impacto en la EN",
                                            selection=[('No hay / No Aplica', 'No hay / No Aplica'),
                                                       ('Menor', 'Menor'), ('Moderado', 'Moderado'), ('Alto', 'Alto'),
                                                       ('Muy alto', 'Muy alto')], copy=False)
    x_studio_field_ZvKIG = fields.Selection(string="GDR Impacto cumplimiento OyM (Dirección)",
                                            selection=[('No hay / No Aplica', 'No hay / No Aplica'),
                                                       ('Menor', 'Menor'), ('Moderado', 'Moderado'),
                                                       ('Alto', 'Alto'), ('Muy alto', 'Muy alto')], copy=False)
    x_studio_field_GzL31 = fields.Selection(string="GDR Impacto OPS / Prod / Cliente",
                                            selection=[('No hay / No Aplica', 'No hay / No Aplica'),
                                                       ('Menor', 'Menor'), ('Moderado', 'Moderado'),
                                                       ('Alto', 'Alto'), ('Muy alto', 'Muy alto')], copy=False)
    x_studio_field_wcedN = fields.Float(string="GDO Factor", copy=False)
    x_studio_field_ppIPV = fields.Many2one(string="Tarea", comodel_name="project.task",
                                           on_delete="set null", copy=False)
    x_studio_field_HeGMm = fields.Integer(string="New Número entero", readonly=True, copy=False)
    x_studio_field_F2W07 = fields.Selection(string="GDO Probabilidad",
                                            selection=[('Poco probable que ocurra', 'Poco probable que ocurra'),
                                                       ('Algo probable que ocurra', 'Algo probable que ocurra'),
                                                       ('Probable que ocurra', 'Probable que ocurra'),
                                                       ('Es muy probable que ocurra', 'Es muy probable que ocurra')],
                                            copy=False)
    x_studio_field_kEg9m = fields.Selection(string="GDO Ocurrencias previas",
                                            selection=[('Nunca se ha producido', 'Nunca se ha producido'),
                                                       ('No se ha producido en los últimos 10 años',
                                                        'No se ha producido en los últimos 10 años'),
                                                       ('Se ha producido en los últimos 10 años',
                                                        'Se ha producido en los últimos 10 años'),
                                                       ('Se ha producido en los últimos 5 años',
                                                        'Se ha producido en los últimos 5 años'),
                                                       ('Se ha producido en el último año',
                                                        'Se ha producido en el último año')], copy=False)
    x_studio_field_ojMh8 = fields.Selection(string="GDO Potencial nuevos negocios",
                                            selection=[('No hay / No Aplica', 'No hay / No Aplica'),
                                                       ('Menor', 'Menor'), ('Moderado', 'Moderado'), ('Alto', 'Alto'),
                                                       ('Muy alto', 'Muy alto')], copy=False)
    x_studio_field_ZErzf = fields.Selection(string="GDO Potencial para expandir",
                                            selection=[('No hay / No Aplica', 'No hay / No Aplica'),
                                                       ('Menor', 'Menor'), ('Moderado', 'Moderado'), ('Alto', 'Alto'),
                                                       ('Muy alto', 'Muy alto')], copy=False)
    x_studio_field_hBfe8 = fields.Selection(string="GDO Potencial mejora cump. legales",
                                            selection=[('No hay / No Aplica', 'No hay / No Aplica'),
                                                       ('Menor', 'Menor'), ('Moderado', 'Moderado'),
                                                       ('Alto', 'Alto'), ('Muy alto', 'Muy alto')], copy=False)
    x_studio_field_7xvsf = fields.Selection(string="GDO Potencial mejora SGC",
                                            selection=[('No hay / No Aplica', 'No hay / No Aplica'),
                                                       ('Menor', 'Menor'), ('Moderado', 'Moderado'),
                                                       ('Alto', 'Alto'), ('Muy alto', 'Muy alto')], copy=False)
    x_studio_field_3ndQr = fields.Selection(string="GDO Potencial mejora reputación",
                                            selection=[('No impacta / NA', 'No impacta / NA'),
                                                       ('Impacto mínimo', 'Impacto mínimo'),
                                                       ('Impacto moderado', 'Impacto moderado'),
                                                       ('Buen impacto', 'Buen impacto'),
                                                       ('Gran impacto', 'Gran impacto')], copy=False)
    x_studio_field_ixkkT = fields.Selection(string="GDO Costo potencial",
                                            selection=[('> $500.000', '> $500.000'), ('> $100.000', '> $100.000'),
                                                       ('< $100.000', '< $100.000'), ('< $10.000', '< $10.000'),
                                                       ('$0 ó N/A', '$0 ó N/A')], copy=False)
