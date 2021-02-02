from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_label = fields.Many2many(string="Etiquetas", comodel_name="crm.lead.tag", relation="x_account_move_crm_lead_tag_rel", column1="account_move_id", column2="crm_lead_tag_id")
