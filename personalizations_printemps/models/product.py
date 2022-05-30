from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_history = fields.One2many('price.history', 'product_template_id')

    def write(self, vals):
        if 'list_price' in vals or 'standard_price' in vals:
            self.env['price.history'].create({
                'product_template_id': self.id,
                'list_price': vals['list_price'] if 'list_price' in vals else self.list_price,
                'standard_price': vals['standard_price'] if 'standard_price' in vals else self.standard_price,
            })
        return super().write(vals)
