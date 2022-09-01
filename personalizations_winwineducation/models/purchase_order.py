from odoo import models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def get_access_action(self, access_uid=None):
        """ Para las ordenes de compra devolvemos {} para evitar enviar botón de link al registro cuando se envían
            presupuestos u ordenes de compra.
        """
        return {}
