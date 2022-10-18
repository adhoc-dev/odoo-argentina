from odoo import models, fields, api, _
from odoo.exceptions import UserError
from ast import literal_eval


class StockRequest(models.Model):
    _inherit = 'stock.request.order'

    user_tag_allow_ids = fields.Many2many('product.template.tag', compute="_compute_tag_allow_ids")
    warehouse_code = fields.Char(related='warehouse_id.code')
    observations = fields.Text(string='Observaciones')


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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self.filtered("location_id.partner_id"):
            rec.picking_ids.write({"partner_id": rec.location_id.partner_id.id})
        return res

    def add_products_to_stock_request(self):
        """ In order to filter the products of the partner the "product supplier
        search" module need to be installed
        """
        self.ensure_one()
        action = self.env.ref('product.product_normal_action_sell')
        if action:
            context = literal_eval(action.context)
            context.pop('search_default_filter_to_sell', None)
            context.update(dict(
                search_default_filter_to_purchase=True,
                stock_request_products=True,
                company_id=self.company_id.id,
            ))
            action_read = action.sudo().read()[0]
            action_read.update(dict(
                context=context,
                name=_('Stock Request Products'),
                display_name=_('Stock Request Products'),
                domain=[('tag_ids', 'in', self.env.user.tag_ids.ids)],
            ))
        return action_read

    def add_products(self, product, qty):
        self.ensure_one()
        vals = {
            'company_id': self.company_id.id,
            'expected_date': self.expected_date,
            'location_id': self.location_id.id,
            'order_id': self.id,
            'picking_policy': self.picking_policy,
            'procurement_group_id': self.procurement_group_id.id,
            'product_id': product.id,
            'product_uom_id': product.uom_po_id.id,
            'product_uom_qty': qty,
            'route_id': self.route_id.id,
            'warehouse_id': self.warehouse_id.id,
        }
        self.env['stock.request'].create(vals)
