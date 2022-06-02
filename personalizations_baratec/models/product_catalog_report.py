#############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class ProductCatalogReport(models.Model):
    _inherit = 'product.product_catalog_report'

    mode = fields.Selection([('1', 'Sin color'), ('2', 'Con color')], string='Modo catálogo')
    tax = fields.Boolean(string='Mostrar impuesto?')
    note_catalog = fields.Text(string='Aclaraciones catálogo')

    def get_products(self, category_ids):
        categories = category_ids.mapped('id')
        order = self.products_order if self.products_order else ''
        if not self.include_sub_categories:
            domain = [('categ_id.id', 'in', categories)]
        else:
            domain = [('categ_id.id', 'child_of', categories)]
        if self.only_with_stock:
            domain.append(('qty_available', '>', 0))

        products = self.env[self.product_type].search(
            domain, order=order)
        return products

    def get_price(self, product, pricelist):
        product_obj = self.env[self.product_type].with_context(pricelist=pricelist.id, whole_pack_price=True)
        sale_uom = self.env['product.template'].fields_get(
            ['sale_uom_ids'])
        if sale_uom and product.sale_uom_ids:
            product_obj = product_obj.with_context(
                uom=product.sale_uom_ids[0].uom_id.id)
        prod = product_obj.browse([product.id])
        if self.taxes_included:
            taxes = float()
            price = float()
            for tax in prod.taxes_id.mapped('amount'):
                taxes += tax
            price += (prod.price + prod.price*taxes/100)
        else:
            price = prod.price
        return price

    def get_discount(self,prod,price):
        if self.taxes_included:
            taxes = float()
            for tax in prod.taxes_id.mapped('amount'):
                taxes += tax
            price = 100*price/(100+taxes)
        if prod.list_price:
            discount = (prod.list_price - price)*100/prod.list_price
            return round(discount)
        return 0

    def get_category_name(self, name):
        if 'Todos / Se puede vender /' in name:
            return name[26:]
        return name

    def generate_report(self):
        return self.env.ref('personalizations_baratec.action_report_catalog').report_action(self)
