from odoo import api, models, fields


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    analytic_account_id = fields.Many2one(compute='_compute_analytic_id', store=True, readonly=False)
    analytic_tag_ids = fields.Many2many(compute='_compute_tag_ids', store=True, readonly=False)

    @api.onchange('product_id')
    def _compute_analytic_id(self):
        for rec in self:
            default_analytic_account = rec.env['account.analytic.default'].sudo().account_get(
                product_id=rec.product_id.id,
                user_id=rec.env.uid,
                company_id=rec.company_id.id,
            )
            rec.analytic_account_id = default_analytic_account.analytic_id

    @api.onchange('product_id')
    def _compute_tag_ids(self):
        for rec in self:
            default_analytic_account = rec.env['account.analytic.default'].sudo().account_get(
                product_id=rec.product_id.id,
                user_id=rec.env.uid,
                company_id=rec.company_id.id,
            )
            rec.analytic_tag_ids = default_analytic_account.analytic_tag_ids
