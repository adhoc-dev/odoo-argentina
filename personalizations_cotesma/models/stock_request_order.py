from odoo import models, fields, api
from odoo.exceptions import UserError


class StockRequest(models.Model):
    _inherit = 'stock.request.order'

    user_tag_allow_ids = fields.Many2many('product.template.tag', compute="_compute_tag_allow_ids")
    warehouse_code = fields.Char(related='warehouse_id.code')

    
    @api.depends('warehouse_id')
    @api.depends_context('uid')
    def _compute_tag_allow_ids(self):
        for rec in self:
            rec.user_tag_allow_ids = self.env.user.tag_ids

    @api.model
    def _create_from_product_multiselect(self, products):
        if products:
            product_without_access = products.filtered(lambda p: p.tag_ids not in self.env.user.tag_ids)
            if product_without_access:
                raise UserError('Estos productos: "%s" no tienen permisos para generar Pedido de existencias.' % ' - '.join(product_without_access.mapped('name')))
        return super()._create_from_product_multiselect(products)

