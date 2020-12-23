from odoo import api, models
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('name')
    def _check_product_uniq(self):
        if not self._context.get('default_program_type', False):
            for rec in self:
                nbr_product = self.env['product.template'].search_count([('name', '=', rec.name)])
                if nbr_product > 1:
                    raise ValidationError(
                        "No puede haber 2 productos con el mismo nombre, Eliga otro nombre")

