from odoo import models, fields


class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    managed_product_ids = fields.One2many('adhoc.product', 'product_manager_id')
    owned_product_ids = fields.One2many('adhoc.product', 'product_owner_id')
    experteese_product_ids = fields.Many2many('adhoc.product', relation="adhoc_product_expert_rel")
