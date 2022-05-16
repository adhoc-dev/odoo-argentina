from odoo import models
from odoo.exceptions import UserError


class OrderpointUpdateMaxMinFromSuggestedWizard(models.TransientModel):
    _name = 'orderpoint.update_maxmin_from_suggested.wizard'
    _description = 'Actualizar máximo y mínimo desde cantidades sugeridas'

    def confirm(self):
        self.ensure_one()
        active_ids = self._context.get('active_ids')
        active_model = self._context.get('active_model')
        if active_model != 'stock.warehouse.orderpoint':
            raise UserError(_(
                'Esta acción debe ser llamada desde las reglas de abastecimiento'))
        return self.env[active_model].browse(
            active_ids)._update_from_suggested()
