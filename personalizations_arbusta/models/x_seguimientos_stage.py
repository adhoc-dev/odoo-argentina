from odoo import models, fields


class XSeguimientosStage(models.Model):
    _name = 'x_seguimientos_stage'
    _description = 'Seguimientos etapas'

    x_name = fields.Char(string="Name", copy=False)
