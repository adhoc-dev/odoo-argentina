from odoo import models, fields


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    x_studio_field_S1rgc = fields.Char(string="Procesador", copy=False)
    x_studio_field_IcWSQ = fields.Selection(string="SO",
                                            selection=[('Android', 'Android'), ('iOS', 'iOS'), ('Linux', 'Linux'),
                                                       ('Windows', 'Windows')], copy=False)
    x_studio_field_ryw64 = fields.Char(string="Versión", copy=False)
    x_studio_field_oL0Da = fields.Selection(string="RAM",
                                            selection=[('2GB', '2GB'), ('4GB', '4GB'), ('6GB', '6GB'), ('8GB', '8GB'),
                                                       ('12GB', '12GB'), ('16GB', '16GB')], copy=False)
    x_employee_ids = fields.Many2many(string="Empleados", comodel_name="hr.employee",
                                      relation="x_hr_employee_maintenance_equipment_rel",
                                      column1="maintenance_equipment_id", column2="hr_employee_id",
                                      on_delete="cascade")
    x_studio_field_Fma5o = fields.Char(string="MAC Adress", copy=False)
    bateria = fields.Char(string="Batería", copy=False)
    adaptador = fields.Char(string="Adaptador", copy=False)
    x_studio_field_zSGQr = fields.Boolean(string="Uso part-time", copy=False)
    x_studio_field_BGI1f = fields.Boolean(string="Seguro", copy=False)
    x_studio_field_X4XKN = fields.Selection(string="Valoración",
                                            selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                       ('5', '5')], copy=False)
    x_studio_field_L19xM = fields.Boolean(string="Leasing", copy=False)
    x_studio_field_KNn6W = fields.Selection(string="Almacenamiento",
                                            selection=[('HDD 250GB', 'HDD 250GB'), ('HDD 500GB', 'HDD 500GB'),
                                                       ('HDD 1TB', 'HDD 1TB'), ('SDD 120GB', 'SDD 120GB'),
                                                       ('SDD 240GB', 'SDD 240GB'), ('SDD 500GB', 'SDD 500GB')],
                                            copy=False)
    x_studio_field_TSV4A = fields.Boolean(string="Alquilado", copy=False)
    x_studio_field_LfHb2 = fields.Boolean(string="Service técnico", copy=False)
