from odoo import models, fields


class AdhocModuleModule(models.Model):
    _inherit = 'adhoc.module.module'

    adhoc_product_id = fields.Many2one(related='module_id.adhoc_product_id', store=True)
    product_category_id = fields.Many2one('adhoc.product', related='adhoc_product_id.product_category_id', store=True)

    def _get_adhoc_category_field(self):
        """ en vez de identificar los modules version con la adhoc category lo hacemos con el product category
        luego modificamos también las vistas para que se vea este dato. Al sincronizar hacia el cliente
        lo seguimos llamando adhoc category
        TODO ver tal vez de renombrar también en el cliente y llamarlo product category?
        """
        return 'product_category_id'
