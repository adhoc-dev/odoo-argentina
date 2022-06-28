from odoo import models, fields


class XSeguimientos(models.Model):
    _name = 'x_seguimientos'
    _description = 'Seguimientos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", copy=False)
    x_studio_field_TTmDr = fields.Many2one(string="Colaborador/a", comodel_name="hr.employee", on_delete="set null",
                                           copy=False)
    x_studio_field_2bqg4 = fields.Char(string="Equipo", related="x_studio_field_TTmDr.department_id.name",
                                       readonly=True, copy=False, store=True)
    x_studio_field_f0rK8 = fields.Char(string="Responsable", related="x_studio_field_TTmDr.parent_id.name",
                                       readonly=True, tracking=100, copy=False, store=True)
    x_studio_field_nZW1U = fields.Selection(string="Tipo de Conversación",
                                            selection=[('PAL', 'Plan de acompañamiento laboral'),
                                                       ('Casos puntuales', 'Casos puntuales'),
                                                       ('Otras conversaciones', 'Otras conversaciones')],
                                            tracking=100, copy=False)
    x_studio_field_2Ct4K = fields.Char(string="Link PAL", copy=False, tracking=100)
    x_studio_field_HIWV1 = fields.Date(string="Inicio PAL", copy=False, tracking=100)
    x_studio_field_qDZi1 = fields.Date(string="Fin PAL", copy=False, tracking=100)
    x_studio_field_5UmOW = fields.Date(string="Fecha", copy=False)
    x_studio_field_vzUZ2 = fields.Html(string="Descripción", copy=False)
    x_stage_id = fields.Many2one(string="Etapa", comodel_name="x_seguimientos_stage", on_delete="set null", copy=False)
    x_studio_field_ALnNA = fields.Char(string="Correo Responsable",
                                       related="x_studio_field_TTmDr.parent_id.work_email",
                                       readonly=True, copy=False, store=True)
    x_studio_field_q3WdL = fields.Selection(string="Pipeline status bar",
                                            selection=[('status1', 'Plan iniciado'), ('status2', 'Plan en curso'),
                                                       ('status3', 'Plan finalizado')], tracking=50, copy=False)
    x_studio_field_spRXL = fields.Many2one(string="Empleadom", comodel_name="hr.employee",
                                           on_delete="set null", copy=False)
    x_studio_field_9EuDY = fields.Html(string="Confidencial", copy=False)
    x_studio_instancia_del_proceso = fields.Selection(string="Instancia del Proceso",
                                                      selection=[('Charla inicial con líder',
                                                                  'Charla inicial con líder'),
                                                                 ('Llamadodeatencion',
                                                                  'Llamado de atención - Apercibimiento oral'),
                                                                 ('Apercibimiento escrito', 'Apercibimiento escrito'),
                                                                 ('Suspensión de días', 'Suspensión de días')],
                                                      copy=False)
    x_studio_instancia_del_pal = fields.Selection(string="Instancia del PAL",
                                                  selection=[('Charla inicial', 'Charla inicial'),
                                                             ('Primera devolución', 'Primera devolución'),
                                                             ('Segunda devolución', 'Segunda devolución'),
                                                             ('Tercera devolución', 'Tercera devolución'),
                                                             ('Cuarta devolución', 'Cuarta devolución'),
                                                             ('Definición del líder', 'Definición del líder'),
                                                             ('Reunión de cierre del plan',
                                                              'Reunión de cierre del plan')],
                                                  copy=False, tracking=100)
