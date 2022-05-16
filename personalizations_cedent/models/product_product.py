from odoo import models, fields
from odoo.tools.float_utils import float_is_zero
import statistics


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_rotation(self, location=False, compute_stdev=False):
        self.ensure_one()
        # stock "A mano"
        stock_now = self.with_context(location=location.id if location else None).qty_available
        if not float_is_zero(stock_now, precision_rounding=self.uom_id.rounding):
            return super().get_product_rotation(location, compute_stdev)

        move_domain = [('product_id', '=', self.id), ('state', '=', 'done'), ('picking_code', '!=', 'internal')]
        if location:
            move_domain += ['|',
                ('location_id', 'child_of', location.id), ('location_dest_id', 'child_of', location.id)
            ]
        last_move = self.env['stock.move'].search(move_domain, order="date desc", limit=1)

        if last_move:
            last_day_stock = last_move.date.date()
            from_date = fields.Datetime.subtract(last_day_stock, days=120)

            base_domain = [
                ('date', '>=', from_date),
                ('state', '=', 'done'),
                ('product_id', '=', self.id),
            ]
            base_domain_send = base_domain + [
                ('location_dest_id.usage', '=', 'customer')]
            base_domain_return = base_domain + [
                ('location_id.usage', '=', 'customer')]

            if location:
                base_domain_send += [('location_id', 'child_of', location.id)]
                base_domain_return += [
                    ('location_dest_id', 'child_of', location.id)]

            quantities = self.env['stock.move'].search(base_domain_send).mapped(
                'product_qty') + self.env['stock.move'].search(
                    base_domain_return).mapped(lambda x: -x.product_qty)
            rotation = sum(quantities) / 4.0
            if compute_stdev:
                stdev = len(quantities) > 1 and statistics.stdev(quantities) or 0.0
        else:
            rotation = stdev = 0.0
        if compute_stdev:
            return rotation, stdev
        return rotation
