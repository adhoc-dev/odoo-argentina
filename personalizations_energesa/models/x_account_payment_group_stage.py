from odoo import models, fields


class XAccountPaymentGroupStage(models.Model):
    _name = 'x_account.payment.group_stage'
    _description = 'Grupo de Pago etapas'
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", copy=False)
