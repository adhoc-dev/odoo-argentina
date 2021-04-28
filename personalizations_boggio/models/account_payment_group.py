from odoo import models, fields


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    x_operate_with_checks = fields.Boolean(string="Opera con Cheques", related="partner_id.x_operate_with_checks", help="Si el campo esta activo quiere decir que el cliente puede operar con cheques en los recibos", readonly=True, copy=False)
    x_control = fields.Boolean(string="Control", help="Control de pago", readonly=True, copy=False)
