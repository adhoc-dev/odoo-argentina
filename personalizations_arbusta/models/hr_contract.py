from odoo import models, fields


class HrContract(models.Model):
    _inherit = 'hr.contract'

    x_studio_field_TiE3d = fields.Selection(string="Oficina", related="employee_id.x_studio_field_HkwZE",
                                            readonly=True, copy=False, store=True)
    x_studio_field_iEtK8 = fields.Many2one(string="Etapa", comodel_name="helpdesk.stage",
                                           on_delete="set null", copy=False)
    x_studio_field_FKfYe = fields.Text(string="Comentarios", copy=False)
    x_studio_field_GSsUn = fields.Selection(string="PIL Tipo",
                                            selection=[('Común', 'Común'), ('Empalme', 'Empalme')], copy=False)
    x_studio_field_mGr59 = fields.Monetary(string="PIL Monto", copy=False)
    x_studio_field_eIfqe = fields.Selection(string="PEJ Tipo",
                                            selection=[('PEL', 'Primera Experiencia Laboral (PEL)'),
                                                       ('TPJ', 'Trabajo Protegido Joven (TPJ)')],
                                            copy=False)
    x_studio_field_VJN0Z = fields.Char(string="Responsable", related="employee_id.parent_id.name",
                                       readonly=True, tracking=True, copy=False, store=True)
