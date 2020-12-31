from odoo import models, fields


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    x_studio_field_a96Q7 = fields.Monetary(string="Facturación esperada", tracking=100, copy=False)
    x_studio_field_fRhqO = fields.Integer(string="Horas totales", tracking=100, copy=False)
    x_studio_field_t74nz = fields.Char(string="Sector Cliente", related="partner_id.industry_id.name",
                                       readonly=True, translate=True, copy=False, store=True)
    x_studio_field_AMCA4 = fields.Date(string="Renegociar rate", tracking=100, copy=False)
    x_studio_field_kkleC = fields.Date(string="Kickoff", copy=False)
    x_studio_field_LQKkN = fields.Char(string="SO del proyecto",
                                       related="analytic_account_id.project_ids.x_studio_field_D7BUq.display_name",
                                       readonly=True, copy=False, store=True)
