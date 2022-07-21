from odoo import models, fields, api

class AdhocProduct(models.Model):
    _name = 'adhoc.product'
    _description = 'Adhoc Products'
    _rec_name = "product_full_name"

    product_name = fields.Char(required=True)
    parent_id = fields.Many2one('adhoc.product')
    product_full_name = fields.Char(compute='_compute_product_full_name', store=True)
    product_manager_id = fields.Many2one('hr.employee')
    product_owner_id = fields.Many2one('hr.employee')
    product_expert_ids = fields.Many2many('hr.employee', relation="adhoc_product_expert_rel")
    technical_team_id = fields.Many2one('hr.department')

    @api.depends('product_name', 'technical_team_id')
    def _compute_product_full_name(self):
        product_full_name = '%s (%s)' %(self.product_name, self.technical_team_id)
        return product_full_name
