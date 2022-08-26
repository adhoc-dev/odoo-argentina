from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    adhoc_product_id = fields.Many2one('adhoc.product')
