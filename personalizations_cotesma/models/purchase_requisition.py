from odoo import models, fields, _
from odoo.exceptions import UserError


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    vendor_ids = fields.Many2many('res.partner', string="Vendors", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    priority = fields.Selection([('0', 'Normal'),('1', 'Urgente')], string="Prioridad")

    def action_in_progress(self):
        self.ensure_one()
        if not self.vendor_ids or self.type_id.quantity_copy == 'none':
            return super().action_in_progress()

        if not all(obj.line_ids for obj in self):
            raise UserError(_("You cannot confirm agreement '%s' because there is no product line.") % self.name)

        self.write({'state': 'in_progress'})
        if self.name == 'New' and self.is_quantity_copy != 'none':
            self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.purchase.tender')

        po_ids = []
        for vendor in self.vendor_ids:
            po = self.env['purchase.order'].create({
                'requisition_id': self.id,
                'partner_id': vendor.id,
            })
            po._onchange_requisition_id()
            po_ids.append(po.id)
        return {
            'name': _("Request for Quotation"),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', po_ids)],
        }

    def view_purchase_order_lines(self):
        self.ensure_one()
        action = self.env.ref('purchase_ux.action_purchase_line_tree').read()[0]
        action['domain'] = [('order_id', '=', self.purchase_ids.ids)]
        action['context'] = {'search_default_groupby_product': 1}
        return action
