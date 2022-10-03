from odoo import fields, models

class PurchaseRequestLine(models.Model):

    _inherit = "purchase.request.line"

    date_required = fields.Date(default=False)
    tag_id = fields.Many2one("product.template.tag", string="Etiqueta")
