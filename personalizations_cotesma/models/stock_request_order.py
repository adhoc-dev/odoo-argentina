from odoo import models, fields


class StockRequest(models.Model):
    _inherit = 'stock.request.order'

    user_tag_allow_ids = fields.Many2many('product.template.tag', compute="_compute_tag_allow_ids")

    
    def _compute_tag_allow_ids(self):
        for rec in self:
            rec.user_tag_allow_ids = self.env.user.tag_ids

