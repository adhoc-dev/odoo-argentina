from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    vendor_ids = fields.Many2many('res.partner', string="Vendors", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.onchange('vendor_id')
    def _onchange_vendors(self):
        # TODO: ver
        res = super()._onchange_vendor()
        return

    def action_in_progress(self):
        self.ensure_one()
        if not all(obj.line_ids for obj in self):
            raise UserError(_("You cannot confirm agreement '%s' because there is no product line.") % self.name)
        if self.type_id.quantity_copy == 'none' and self.vendor_ids:
            for requisition_line in self.line_ids:
                if requisition_line.price_unit <= 0.0:
                    raise UserError(_('You cannot confirm the blanket order without price.'))
                if requisition_line.product_qty <= 0.0:
                    raise UserError(_('You cannot confirm the blanket order without quantity.'))
                requisition_line.create_supplier_info()
            self.write({'state': 'ongoing'})
        else:
            super().action_in_progress()
        # Set the sequence number regarding the requisition type
        if self.name == 'New':
            if self.is_quantity_copy != 'none':
                self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.purchase.tender')
            else:
                self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.blanket.order')

    def purchase_requisition_to_multiple_so(self):
        self.ensure_one()
        if not self.vendor_ids:
            action = self.env.ref('purchase_requisition.action_purchase_requisition_to_so').read()[0]
            return action
        else:
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


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    @api.model
    def create(self, vals):
        res = super(PurchaseRequisitionLine, self).create(vals)
        if res.requisition_id.state not in ['draft', 'cancel', 'done'] and res.requisition_id.is_quantity_copy == 'none':
            for vendor in res.requisition_id.vendor_ids:
                supplier_infos = self.env['product.supplierinfo'].search([
                    ('product_id', '=', vals.get('product_id')),
                    ('name', '=', vendor.id),
                ])
                if not any([s.purchase_requisition_id for s in supplier_infos]):
                    res.create_supplier_info()
            if vals['price_unit'] <= 0.0:
                raise UserError(_('You cannot confirm the blanket order without price.'))
        return res

    def create_supplier_info(self):
        purchase_requisition = self.requisition_id
        if purchase_requisition.type_id.quantity_copy == 'none' and purchase_requisition.vendor_ids:
            # create a supplier_info only in case of blanket order
            for vendor in purchase_requisition.vendor_ids:
                self.env['product.supplierinfo'].create({
                    'name': vendor.id,
                    'product_id': self.product_id.id,
                    'product_tmpl_id': self.product_id.product_tmpl_id.id,
                    'price': self.price_unit,
                    'currency_id': self.requisition_id.currency_id.id,
                    'purchase_requisition_line_id': self.id,
                })
        else:
            super().create_supplier_info()
