from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    x_label = fields.Many2many(string="Etiquetas", comodel_name="crm.lead.tag", relation="x_account_invoice_crm_lead_tag_rel", column1="account_invoice_id", column2="crm_lead_tag_id")
