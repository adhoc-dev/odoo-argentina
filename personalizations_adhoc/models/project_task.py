from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    adhoc_product_ids = fields.Many2many('adhoc.product')
