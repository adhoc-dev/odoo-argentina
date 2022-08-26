from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    adhoc_product_id = fields.Many2one('adhoc.product')
