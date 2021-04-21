from odoo import models, fields


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    x_stage_id = fields.Many2one(string="Etapa", comodel_name="x_account.payment.group_stage", on_delete="set null", copy=False)
