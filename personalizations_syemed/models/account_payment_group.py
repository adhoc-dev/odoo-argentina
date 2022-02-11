from odoo import models, fields


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    # Hay otro campo en otro modulo de personalizacion que tiene mismo string y
    # lanza warning en el runbot. Agredamos un espacio extra en el string intentado
    # ver si podemos skipear ese warning
    x_commercial_id = fields.Many2one(related="partner_id.user_id", string="Comercial Asignado ", store=True)
