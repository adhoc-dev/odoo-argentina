from odoo import models, fields


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    date_start = fields.Date(required=True)
    purchase_type = fields.Selection([('bajo','Bajo'),('medio','Medio'), ('alto','Alto')])

    def button_approved(self):
        res = super().button_approved()
        self.ensure_one()
        template_id = self.env.ref(
            'personalizations_arbusta.purchase_request_mail_template').id
        self.message_post_with_template(template_id)
        return res
