from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    x_studio_field_Aq37T = fields.Selection(string="Unidad",
                                            selection=[('Global', 'Global'),
                                                       ('BD1', 'BD1'), ('BD2', 'BD2'),
                                                       ('BT1', 'BT1'), ('BT2', 'BT2'),
                                                       ('MD1', 'MD1'), ('MT1', 'MT1'),
                                                       ('MOD1', 'MOD1'), ('MOT1', 'MOT1'),
                                                       ('RD1', 'RD1'), ('RT1', 'RT1')],
                                            copy=False)
    x_studio_field_D7BUq = fields.Many2one(string="Service Owner", comodel_name="hr.employee",
                                           on_delete="set null", copy=False)
    x_studio_field_b1glF = fields.Integer(string="Horas teóricas", copy=False)
    x_studio_field_8MFbu = fields.Selection(string="Tribu",
                                            selection=[('Data Services', 'Data Services'),
                                                       ('Development', 'Development'),
                                                       ('DIS', 'Digital Interaction Services'),
                                                       ('Machine Learning Training', 'Machine Learning Training'),
                                                       ('QA & Software Testing', 'QA & Software Testing'),
                                                       ('Círculo Capacity', 'Círculo Capacity'),
                                                       ('Círculo Capital Humano', 'Círculo Capital Humano'),
                                                       ('Círculo Delivery', 'Círculo Delivery'),
                                                       ('Círculo Finanzas', 'Círculo Finanzas'),
                                                       ('Círculo Grow', 'Círculo Grow')], copy=False)
    x_studio_field_QI5H4 = fields.Selection(string="Industria",
                                            selection=[('Aeronáutica', 'Aeronáutica'),
                                                       ('Agrobusiness', 'Agrobusiness'), ('Banca', 'Banca'),
                                                       ('Beauty', 'Beauty'), ('Cryptomonedas', 'Cryptomonedas'),
                                                       ('E-commerce & marketplace', 'E-commerce & marketplace'),
                                                       ('Educación', 'Educación'),
                                                       ('Electrónica', 'Electrónica'),
                                                       ('Entretenimiento', 'Entretenimiento'),
                                                       ('Fintech', 'Fintech'), ('Gobierno', 'Gobierno'),
                                                       ('Marketplace', 'Marketplace'), ('Oil & Gas', 'Oil & Gas'),
                                                       ('ONG', 'ONG'), ('Otra', 'Otra'), ('Paperless', 'Paperless'),
                                                       ('Recursos Humanos', 'Recursos Humanos'), ('Salud', 'Salud'),
                                                       ('Seguros', 'Seguros'), ('Tecnología', 'Tecnología'),
                                                       ('N/A', 'N/A')], copy=False)
    x_studio_field_PkoH6 = fields.Many2many(string="Subservicio", comodel_name="crm.lead.tag",
                                            relation="x_crm_lead_tag_project_project_rel",
                                            column1="project_project_id", column2="crm_lead_tag_id",
                                            on_delete="cascade")
    x_studio_field_hPPw1 = fields.Html(string="New Html", copy=False)
    x_studio_field_6Vp7N = fields.Char(string="Carpeta Drive", copy=False)
    x_studio_field_E3Ha4 = fields.Char(string="Archivo Kick Off", copy=False)
    x_studio_field_eTFPK = fields.Many2one(string="Equipo",
                                           related="x_studio_field_D7BUq.department_id",
                                           on_delete="set null", readonly=True, copy=False, store=True)
    x_studio_field_OJHzP = fields.Selection(string="Complejidad",
                                            selection=[('Baja', 'Baja'), ('Media', 'Media'),
                                                       ('Alta', 'Alta')], copy=False)
    x_studio_field_d19Se = fields.Many2many(string="Skills requeridos", comodel_name="hr.skill",
                                            relation="x_hr_skill_project_project_rel", column1="project_project_id",
                                            column2="hr_skill_id", on_delete="cascade", copy=False)
    x_studio_field_9w4KH = fields.Integer(string="Tareas", copy=False)
    x_studio_field_Lys9g = fields.Integer(string="Lógica del negocio", copy=False)
    x_studio_field_SKjuT = fields.Integer(string="SLA - Métricas", copy=False)
    x_studio_field_o2hcY = fields.Integer(string="Herramientas", copy=False)
    description = fields.Html()
