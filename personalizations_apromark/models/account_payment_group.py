from odoo import models, fields


class AccountPaymentGroup(models.Model):

    _inherit = 'account.payment.group'

    fecha_comprobante = fields.Date(string='Fecha del Comprobante')
    nro_comprobante = fields.Char(string='Nro de Comprobante')
