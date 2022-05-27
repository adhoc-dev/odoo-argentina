from odoo import models


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def amount_to_text(self, amount):
        """ Eliminar el nombre de la moneda pesos que esta esta en la cantidad en letras porque ya esta en el reporte
        personalizado impreso en otro lugar """
        res = super().amount_to_text(amount)
        res = res.replace(' ' + self.currency_unit_label, '')
        return res
