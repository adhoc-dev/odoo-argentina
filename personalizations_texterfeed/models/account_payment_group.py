from odoo import api, models, fields


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    x_comercial_id = fields.Many2one('res.users', string="Comercial Asignado", related="partner_id.user_id", store=True)
