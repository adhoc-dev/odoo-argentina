from odoo import models, fields


class PaymentToken(models.Model):
    _inherit = 'payment.token'

    x_tc_card_type = fields.Selection(string="Tipo de Tarjeta", selection=[('debit', 'Debito'), ('credit', 'Credito')])
