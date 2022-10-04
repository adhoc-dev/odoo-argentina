from odoo import fields, models


class AccountPaymentGroupInvoiceWizard(models.TransientModel):

    _inherit = "account.payment.group.invoice.wizard"

    student_id = fields.Many2one(
        'res.partner',
        string='Alumno',
        domain="[('parent_id', '=', partner_id), ('partner_type', '=', 'student')]",
        required=True,
    )

    partner_id = fields.Many2one(related="payment_group_id.partner_id")

    def get_invoice_vals(self):
        res = super().get_invoice_vals()
        res.update({'student_id': self.student_id.id})
        return res
