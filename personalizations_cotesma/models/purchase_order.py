from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    priority = fields.Selection([('0', 'Normal'),('1', 'Urgente')], compute="_compute_priority",
                                string="Prioridad", store=True, readonly=False)

    @api.depends('requisition_id')
    def _compute_priority(self):
        for rec in self:
            if rec.requisition_id:
                rec.priority = rec.requisition_id.priority
