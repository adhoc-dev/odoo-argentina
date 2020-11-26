from odoo import api, models
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('name')
    def _check_product_uniq(self):
        # Agregamos Discount en filtered ya que el modulo sale_coupon crea productos con el mismo nombre para los descuento
        for rec in self.filtered(lambda x: x.name.find("discount") == -1):
            nbr_product = self.env['product.template'].search_count([('name', '=', rec.name)])
            if nbr_product > 1:
                raise ValidationError(
                    "No puede haber 2 productos con el mismo nombre, Eliga otro nombre")

