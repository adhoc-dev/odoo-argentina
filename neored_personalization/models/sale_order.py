from odoo import models, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def action_external_stock_wizard(self):
        self.ensure_one()
        rec = self.env['external.stock.wizard'].with_context(product_id=self.product_template_id.id).create({})
        return {
            'name': _('External Stock'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'external.stock.wizard',
            'view_type': 'form',
            'res_id': rec.id,
            'target': 'new',
        }
