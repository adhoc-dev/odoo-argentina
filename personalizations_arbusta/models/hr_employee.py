from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    job_id = fields.Many2one(tracking=100)

    x_studio_field_HkwZE = fields.Selection(string="Oficina", selection=[('Buenos Aires', 'BUE'), ('Medellín', 'MED'),
                                                                         ('Montevideo', 'MON'), ('Rosario', 'ROS')],
                                            copy=False)
    x_studio_field_Qma7r = fields.Selection(string="Unidad",
                                            selection=[('BD1', 'BD1'), ('BD2', 'BD2'), ('BT1', 'BT1'), ('BT2', 'BT2'),
                                                       ('MD1', 'MD1'), ('MT1', 'MT1'), ('MOD1', 'MOD1'),
                                                       ('MOT1', 'MOT1'), ('RD1', 'RD1'), ('RT1', 'RT1'),
                                                       ('Estructura', 'Estructura')],
                                            tracking=100, copy=False)
    x_studio_field_fZbCK = fields.Selection(string="Seniority",
                                            selection=[('N/A', 'N/A'),('Pre junior', 'Pre junior'), ('Junior', 'Junior'),
                                                       ('Semi Senior', 'Semi Senior'), ('Senior', 'Senior'),
                                                       ('Trainee', 'Trainee')], tracking=100, copy=False)
    employee_id_maintenance_equip_count = fields.Integer(string="Asignado al empleado count",
                                                                compute="_compute_employee_maintenance_equip_count",
                                                                readonly=True, copy=False)
    x_studio_field_cTb35 = fields.Selection(string="Modalidad",
                                            selection=[('Part-time', 'Part-time'), ('Full-time', 'Full-time')],
                                            tracking=100, copy=False)
    x_studio_field_ontRJ = fields.Selection(string="Situación extranj.",
                                            selection=[('Trámite en proceso', 'Trámite en proceso'),
                                                       ('Precaria', 'Precaria'), ('Temporaria', 'Temporaria'),
                                                       ('DNI Permanente', 'DNI Permanente')], copy=False)
    x_studio_field_r6BXX = fields.Char(string="Nombre OS", copy=False)
    x_studio_field_bdBsj = fields.Char(string="Plan Prepaga", copy=False)
    level_reached = fields.Selection(string="Nivel alcanzado",
                                     selection=[('Incompleto', 'Incompleto'),('En curso', 'En curso'), ('Graduado', 'Graduado')],
                                     copy=False)
    x_department_id = fields.Many2one(string="department_id", related="department_id",
                                      help="Solo se usa por el seguimiento", on_delete="set null", readonly=True)
    parent_id = fields.Many2one(domain="[]")
    coach_id = fields.Many2one(domain="[]")
    x_parent_id = fields.Many2one(string="parent_id", related="parent_id", help="Por seguimiento",
                                  on_delete="set null", readonly=True)
    x_coach_id = fields.Many2one(string="coach_id", related="coach_id", help="Por seguimiento",
                                 on_delete="set null", readonly=True)
    x_studio_field_t2GcX = fields.Char(string="Carrera", copy=False)
    x_maintenance_equipment_ids = fields.Many2many(string="Equipos",
                                                   comodel_name="maintenance.equipment",
                                                   relation="x_hr_employee_maintenance_equipment_rel",
                                                   column1="hr_employee_id", column2="maintenance_equipment_id",
                                                   on_delete="cascade")
    x_studio_field_HT2p1 = fields.Boolean(string="Certif. alumno", copy=False)
    x_studio_field_wmRd0 = fields.Integer(string="Adic. a cargo", copy=False)
    x_studio_field_BGD1N = fields.Many2one(string="Contact", comodel_name="res.partner",
                                           on_delete="set null", copy=False)
    x_studio_field_bysyH = fields.Selection(string="Área",
                                            selection=[('Calidad de Procesos', 'Calidad de Procesos'),
                                                       ('Capital Humano', 'Capital Humano'),
                                                       ('Comercial', 'Comercial'), ('Comunicación', 'Comunicación'),
                                                       ('Directorio', 'Directorio'),
                                                       ('Entrenamientos', 'Entrenamientos'), ('Finanzas', 'Finanzas'),
                                                       ('Operaciones', 'Operaciones'), ('Plataformas', 'Plataformas'),
                                                       ('Tecnología', 'Tecnología')], copy=False)
    x_studio_field_lhpTm = fields.Char(string="Legajo N°", copy=False)
    x_studio_field_wir9T = fields.Char(string="CUIL", related="user_id.vat",
                                       help="Identification Number for selected type", readonly=True,
                                       copy=False, store=True)
    x_studio_field_L0xnY = fields.Char(string="CBU", related="user_id.bank_ids.acc_number",
                                       help="Código Bancario Único Argentino", readonly=True, copy=False, store=True)
    x_studio_field_tyBkm = fields.Char(string="Nombre Prepaga", copy=False)
    employee_id_account_analytic_line_count = fields.Integer(string="Employee count",
                                                             compute="_compute_employee_account_analytic_line_count",
                                                             copy=False)
    x_studio_field_r67Xd = fields.Char(string="Movi N°", tracking=100, copy=False)
    x_studio_field_Ev7Dp = fields.Selection(string="Tribu",
                                            selection=[('Data Services', 'Data Services'),
                                                       ('Development', 'Development'),
                                                       ('Digital Interaction Services',
                                                        'Digital Interaction Services'),                                                       ('Machine Learning Training', 'Machine Learning Training'),
                                                       ('QA & Software Testing', 'QA & Software Testing'),
                                                       ('Staff', 'Staff')], copy=False)
    x_studio_field_2MSWR = fields.Selection(string="Chapter",
                                            selection=[('Automatización', 'Automatización'),
                                                       ('Comunicaciones', 'Comunicaciones'),
                                                       ('Mejora Contínua', 'Mejora Contínua'),
                                                       ('Técnico', 'Técnico')], copy=False, tracking=100)
    x_studio_field_SHzlD = fields.Boolean(string="Homeoffice", copy=False)
    x_studio_field_CsHEC = fields.Boolean(string="Disponibilidad FT", tracking=100, copy=False)
    x_studio_field_q5sPJ = fields.Boolean(string="Validación FT", tracking=100, copy=False)
    x_studio_field_ny2Ip = fields.Date(string="Fecha Baja", copy=False)
    x_studio_field_RiU1z = fields.Selection(string="Tipo de desvinculación",
                                            selection=[('No pasó período de prueba','No pasó período de prueba'), ('Finalización de contrato','Finalización de contrato'),('Despido', 'Despido'), ('Renuncia', 'Renuncia'),
                                                       ('Otro', 'Otro')], copy=False)
    x_studio_field_awy5r = fields.Char(string="Comentarios baja", copy=False)
    x_studio_field_RFrXP = fields.Selection(string="Causa baja",
                                            selection=[('Estudio','Estudio'),('Nuevo empleo', 'Nuevo empleo'),
                                                       ('Motivos Personales', 'Motivos personales')], copy=False)
    x_studio_field_1jaDd = fields.Selection(string="Motivo baja",
                                            selection=[
                                                       ('Mudanza', 'Mudanza'),
                                                       ('Relación con su líder', 'Relación con su líder'),
                                                       ('Mejora Salarial','Mejora Salarial'),
                                                       ('Posibilidades de desarrollo','Posibilidades de desarrollo'),
                                                       ('Clima laboral','Clima laboral'),
                                                       ('Cuidado del hogar','Cuidado del hogar'),
                                                       ('Otros','Otros')],
                                            copy=False)
    x_studio_field_VKdnN = fields.Integer(string="Modalidad horas", copy=False)
    x_studio_field_na3Vg = fields.Boolean(string="Requiere conectividad", copy=False)
    level_study = fields.Selection(string='Grado de Estudio',
                                   selection=[('es', 'Educación Superior'), ('em', 'Educación Media'),
                                              ('ep', 'Educación Primaria'), ('utu', 'UTU'),
                                              ('Secundaria','Secundaria'),('Terciaria','Terciaria'),
                                              ('Universitaria','Universitaria'),('Posgrado/Master','Posgrado/Master')])
    registry_date = fields.Date(string='Alta', tracking=100, copy=False)
    comunidad_arbustera = fields.Boolean(string='Comunidad Arbustera')

    def _compute_employee_maintenance_equip_count(self):
        results = self.env['maintenance.equipment'].read_group([('employee_id', 'in', self.ids)],
                                                               ['employee_id'], 'employee_id')
        dic = {}
        for x in results:
            dic[x['employee_id'][0]] = x['employee_id_count']
        for record in self:
            record['employee_id_maintenance_equip_count'] = dic.get(record.id, 0) +\
                len(record.x_maintenance_equipment_ids)

    def _compute_employee_account_analytic_line_count(self):
        results = self.env['account.analytic.line'].read_group([('employee_id', 'in', self.ids)],
                                                               ['employee_id'], 'employee_id')
        dic = {}
        for x in results:
            dic[x['employee_id'][0]] = x['employee_id_count']
        for record in self:
            record['employee_id_account_analytic_line_count'] = dic.get(record.id, 0)
