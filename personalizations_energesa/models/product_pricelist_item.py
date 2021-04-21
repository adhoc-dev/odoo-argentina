from odoo import models, fields


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    x_mark_up = fields.Float(string="Mark up", compute="_compute_x_mark_up", readonly=True, copy=False, store=True)
    x_product_lst_price = fields.Float(string="Precio de lista + IVA", compute="_compute_x_product_lst_price", readonly=True, copy=False, store=True)
    x_b2b_price = fields.Float(string="Precio B2B", compute="_compute_x_b2b_price", readonly=True, copy=False, store=True)

    def _compute_x_mark_up(self):
      for rec in self:
        rec['x_mark_up'] = (rec.x_product_lst_price / rec.x_b2b_price) - 1 if rec.x_b2b_price != 0 else 0

    def _compute_x_product_lst_price(self):
        for rec in self:
          rec['x_product_lst_price'] = rec.product_tmpl_id.lst_price

    def _compute_x_b2b_price(self):
        for rec in self:
          rec['x_b2b_price'] = 	rec.x_product_lst_price * (1 - rec.percent_price /100)
