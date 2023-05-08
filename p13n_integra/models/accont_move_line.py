from odoo import models, fields


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    payment_method_id = fields.Many2one(related="move_id.payment_id.payment_method_line_id", string="Método de Pago")
