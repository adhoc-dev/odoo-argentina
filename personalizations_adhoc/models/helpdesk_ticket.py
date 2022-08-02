from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    adhoc_product_ids = fields.Many2many('adhoc.product')
