##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'


    def _compute_price_rule_get_items(self, products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids, categ_ids):
        """
        Modificamos este metodo para agregar a la query un and a la clausla WHERE para tener en cuenta el campo "brand_id y "manufacturer"
        """
        self.ensure_one()
        prod_templates = self.env['product.template'].browse(prod_tmpl_ids)
        prod_variants = self.env['product.product'].browse(prod_ids)
        brands = prod_templates.mapped('product_brand_id') or self.env['product.brand']
        manufactures = prod_variants.mapped('manufacturer') or self.env['res.partner']
        self.env['product.pricelist.item'].flush(['price', 'currency_id', 'company_id'])
        # Load all rules
        self.env.cr.execute(
            """
             SELECT
                item.id
            FROM
                product_pricelist_item AS item
            LEFT JOIN product_category AS categ ON item.categ_id = categ.id
            WHERE
                (item.product_tmpl_id IS NULL OR item.product_tmpl_id = any(%s))
                AND (item.product_id IS NULL OR item.product_id = any(%s))
                AND (item.categ_id IS NULL OR item.categ_id = any(%s))
                AND (item.brand_id IS NULL OR item.brand_id = any(%s))
                AND (item.manufacturer IS NULL OR item.manufacturer = any(%s))
                AND (item.pricelist_id = %s)
                AND (item.date_start IS NULL OR item.date_start<=%s)
                AND (item.date_end IS NULL OR item.date_end>=%s)
            ORDER BY
                item.applied_on, item.min_quantity desc, item.brand_id, item.manufacturer, categ.complete_name desc, item.id desc
            """,
            (prod_tmpl_ids, prod_ids, categ_ids, brands.ids, manufactures.ids, self.id, date, date))
        # NOTE: if you change `order by` on that query, make sure it matches
        # _order from model to avoid inconstencies and undeterministic issues.

        item_ids = [x[0] for x in self.env.cr.fetchall()]
        return self.env['product.pricelist.item'].browse(item_ids)
