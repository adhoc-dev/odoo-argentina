from odoo import models, fields, api


class AdhocProduct(models.Model):
    _name = 'adhoc.product'
    _description = 'Adhoc Products'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = 'complete_name'

    name = fields.Char('Nombre', index=True, required=True)
    complete_name = fields.Char('Nombre Completo', compute='_compute_complete_name', recursive=True, store=True)
    parent_id = fields.Many2one('adhoc.product', 'Producto Padre', index=True, ondelete='restrict')
    parent_path = fields.Char(index=True)
    product_manager_id = fields.Many2one('hr.employee')
    product_owner_id = fields.Many2one('hr.employee')
    product_expert_ids = fields.Many2many('hr.employee', relation="adhoc_product_expert_rel")
    technical_team_id = fields.Many2one('hr.department', string='Equipo Técnico')
    color = fields.Integer(string='Color')
    product_category_id = fields.Many2one('adhoc.product', compute='_compute_product_category', recursive=True, store=True)

    @api.depends('parent_id.product_category_id')
    def _compute_product_category(self):
        for rec in self:
            if rec.parent_id:
                rec.product_category_id = rec.parent_id.product_category_id
            else:
                rec.product_category_id = rec

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for rec in self:
            if rec.parent_id:
                rec.complete_name = '%s / %s' % (rec.parent_id.complete_name, rec.name)
            else:
                rec.complete_name = rec.name
