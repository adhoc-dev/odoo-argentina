from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_pack_cost = fields.Monetary(string="Costo Pack", compute="_compute_x_pack_cost", readonly=True, copy=False, store=True)

    @api.depends('pack_line_ids','pack_line_ids.x_subtotal')
    def _compute_x_pack_cost(self):
        for rec in self.filtered('pack_line_ids'):
            total = 0
            for prod in rec.pack_line_ids:
                if prod.x_subtotal:
                    total += prod.x_subtotal
            rec['x_pack_cost'] = total
