from odoo import models, fields


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    x_studio_agendar_presupuesto = fields.Date(string="Agendar Presupuesto", copy=False)
    x_studio_costo_materiales = fields.Float(string="Costo Materiales Presupuestado", track_visibility='onchange', copy=False)
    x_studio_costo_mano_de_obra = fields.Float(string="Costo Mano de Obra Presupuestado", track_visibility='onchange', copy=False)
    x_studio_adjuntar_presupuesto = fields.Binary(string="Adjuntar Presupuesto", copy=False)
    x_studio_field_72E6j_filename = fields.Char(string="Filename for x_studio_field_72E6j", copy=False)
    x_studio_presupuesto_filename = fields.Char(string="Filename for x_studio_presupuesto", copy=False)
    x_studio_adjuntar_presupuesto_filename = fields.Char(string="Filename for x_studio_adjuntar_presupuesto", copy=False)
    x_studio_costo_materiales_final = fields.Float(string="Costo Materiales Final", copy=False)
    x_studio_costo_mano_de_obra_final = fields.Float(string="Costo Mano de Obra Final", copy=False)
    x_studio_reportado_por = fields.Char(string="Reportado Por", copy=False)
    x_studio_email = fields.Char(string="email", copy=False)
