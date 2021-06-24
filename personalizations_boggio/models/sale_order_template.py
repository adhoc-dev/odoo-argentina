from odoo import models, fields


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    pdf_footer = fields.Html(string="Footer")
