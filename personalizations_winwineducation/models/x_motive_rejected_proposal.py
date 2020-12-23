from odoo import models, fields


class XMotiveRejectedProposal(models.Model):
    _name = 'x_motive_rejected_proposal'
    _description = 'Motivos Rechazo Propuesta Laboral'

    x_name = fields.Char(string="Motivo", required=True, copy=False)
