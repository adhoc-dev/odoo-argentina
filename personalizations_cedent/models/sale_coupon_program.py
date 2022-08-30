from odoo import api, models, fields, _
from odoo.tools.safe_eval import safe_eval


class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    max_stock_quantity = fields.Integer(string="Max Quantity", default=0, help="Si es 0 no hay límite de stock")
    stock_available = fields.Integer(string="Available Stock on Promotion", compute="_compute_stock_available")
    show_max_stock = fields.Boolean(compute="_compute_show_max_stock", default=False)

    def _check_promo_code(self, order, coupon_code):
        if not self._check_available_stock(order):
            domain = safe_eval(self.rule_products_domain)
            product_id = self.env['product.product'].search(domain)
            return {'error': _('There is not enough stock for the product %s only %s left in promotion. Please select up to that quantity.') % (product_id.name, self.stock_available)}
        return super()._check_promo_code(order, coupon_code)

    @api.depends('order_count', 'max_stock_quantity')
    def _compute_stock_available(self):
        for program in self:
            # Obtener ventas con el cupon aplicado
            sale_orders = self.env['sale.order.line'].search([('product_id', '=', program.discount_line_product_id.id), ('state', '!=', 'cancel')]).mapped('order_id')
            # De dichas ventas sumamos la cantidad de producto en promo vendido
            domain = safe_eval(program.rule_products_domain)
            product_ids = self.env['product.product'].search(domain).ids
            sold_quantity = sum(self.env['sale.order.line'].search([
                ('order_id', 'in', sale_orders.ids),
                ('product_id', 'in', product_ids)
            ]).mapped('product_uom_qty'))
            program.stock_available = program.max_stock_quantity - sold_quantity

    def _check_available_stock(self, order):
        domain = safe_eval(self.rule_products_domain)
        product_ids = self.env['product.product'].search(domain).ids
        product_qty = sum([line.product_uom_qty for line in order.order_line.filtered(lambda line: line.product_id.id in product_ids)])
        return product_qty <= self.stock_available and self.max_stock_quantity != 0

    # Chequear si el dominio de las reglas cambió para deshabilitar el stock máximo si la promoción incluye > 1 producto
    @api.depends('rule_products_domain')
    def _compute_show_max_stock(self):
        for program in self:
            domain = safe_eval(program.rule_products_domain)
            product_ids_qty = program.env['product.product'].search_count(domain)
            if product_ids_qty == 1:
                program.show_max_stock = True
            else:
                program.max_stock_quantity = 0
                program.show_max_stock = False
