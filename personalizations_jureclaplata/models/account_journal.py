from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # TODO borrar o agregar campos necesarios
    direct_debit_format = fields.Selection(selection_add=[
        ('pago_mis_cuentas', 'Pago Mis Cuentas')
    ])
