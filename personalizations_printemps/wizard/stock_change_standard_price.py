from odoo import models

class StockChangeStandardPrice(models.TransientModel):
    _inherit = "stock.change.standard.price"

    def change_price(self):
        res = super().change_price()
        if self._context['active_model'] == 'product.template':
            rec = self.env['product.template'].browse(self._context['active_id'])
            rec.env['price.history'].create({
                    'product_template_id': rec.id,
                    'list_price': rec.list_price,
                    'standard_price': rec.standard_price,
                })
        return res
