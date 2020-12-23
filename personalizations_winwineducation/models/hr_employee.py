from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    x_studio_dni = fields.Char(string="D.N.I.", copy=False)
    x_studio_localidad = fields.Char(string="Localidad", copy=False)
    x_studio_cdigo_postal = fields.Char(string="Código postal", copy=False)
    x_studio_provincia = fields.Char(string="Provincia", copy=False)
    x_studio_tiene_hijos_con_discapacidad = fields.Boolean(string="¿Tiene hijos con discapacidad?", copy=False)
    x_studio_antigedad_docente = fields.Integer(string="Antigüedad docente", copy=False)
    x_studio_otras_instituciones_en_las_que_trabaja = fields.Char(string="Otras instituciones en las que trabaja", copy=False)
    x_studio_cantidad_de_horas_declaradas_titular = fields.Char(string="Cantidad de horas declaradas titular", copy=False)
    x_studio_tiene_obra_social_prepaga_o_servicio_de_emergencia = fields.Boolean(string="¿Tiene obra social, prepaga o servicio de emergencia?", copy=False)
    x_studio_nombre_y_plan_de_obra_social = fields.Char(string="Nombre y plan de Obra Social", copy=False)
    x_studio_domicilio_legal = fields.Char(string="Domicilio legal", copy=False)
    x_studio_fecha_de_ingreso = fields.Date(string="Fecha de ingreso", copy=False)
    x_studio_domicilio = fields.Char(string="Domicilio real", copy=False)
    x_studio_depto_lote_uf_etc = fields.Char(string="Depto., Lote., UF., etc.", copy=False)
    x_studio_email_personal = fields.Char(string="Email personal", copy=False)
    x_studio_horas_asignadas_en_nuestro_colegio = fields.Float(string="Horas asignadas en nuestro colegio", copy=False)
    x_studio_field_bbAIl = fields.Integer(string="New Número entero", copy=False)
    x_studio_mvil_personal = fields.Char(string="Móvil personal", copy=False)
    x_studio_cuil_1 = fields.Char(string="C.U.I.L.", copy=False)
    x_studio_field_7V8Ks = fields.Char(string="Número de socio", copy=False)
    x_studio_carrera_finalizada_1 = fields.Selection(string="Carrera finalizada", selection=[["Sí","Sí"],["No","No"]], copy=False)
    x_studio_field_EjHsb = fields.Selection(string="Estado", selection=[["activo","Activo"],["licencia","Licencia"],["baja","Baja"],["Suplente","Suplente"]], copy=False)
    x_studio_asignaturas = fields.Many2many(string="Asignaturas", comodel_name="academic.subject", relation="x_academic_subject_hr_employee_rel", column1="hr_employee_id", column2="academic_subject_id", copy=False)
