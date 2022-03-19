from odoo import models, fields, api, _
from lxml import etree
import json


class ProductProduct(models.Model):
    _inherit = "product.product"

    qty_request = fields.Float(
        string='Quantity to Request',
        compute='_compute_qty_request',
        help="Technical field. Used to compute the quantity of products",
    )

    @api.depends_context('active_id')
    def _compute_qty_request(self):
        stock_request_order_id = self._context.get('active_id', False)
        if not stock_request_order_id:
            self.qty_request = 0
            return

        stock_request_lines = self.env['stock.request.order'].browse(stock_request_order_id).stock_request_ids

        for rec in self:
            lines = stock_request_lines.filtered(lambda x: x.product_id == rec)
            value = sum([line.product_uom_id._compute_quantity(line.product_uom_qty, rec.uom_po_id) for line in lines])
            rec.qty_request = value

    def _set_qty_request(self, qty):
        self.ensure_one()
        stock_request_id = self._context.get('active_id', False)
        if stock_request_id:
            lines = self.env['stock.request'].search([
                ('order_id', '=', stock_request_id),
                ('product_id', '=', self.id)])
            if lines:
                (lines - lines[0]).unlink()
                lines[0].product_uom_qty = qty
            else:
                self.env['stock.request.order'].browse(stock_request_id).add_products(self, qty)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        stock_request_products = self._context.get('stock_request_products')
        if stock_request_products and view_type == 'tree':
            doc = etree.XML(res['arch'])

            # replace uom_id to uom_po_id field
            node = doc.xpath("//field[@name='uom_id']")[0]
            replacement_xml = "<field name='uom_po_id'/>"
            uom_po_id_node = etree.fromstring(replacement_xml)
            node.getparent().replace(node, uom_po_id_node)
            res['fields'].update(self.fields_get(['uom_ids']))

            # make all fields not editable
            for node in doc.xpath("//field"):
                node.set('readonly', '1')
                modifiers = json.loads(node.get("modifiers") or "{}")
                modifiers['readonly'] = True
                node.set("modifiers", json.dumps(modifiers))

            # add qty field
            placeholder = doc.xpath("//field[@name='default_code']")[0]
            placeholder.addprevious(
                etree.Element('field', {
                    'name': 'qty_request',
                    'readonly': '0',
                }))
            res['fields'].update(self.fields_get(['qty_request']))

            # add button tu open form
            placeholder = doc.xpath("//tree")[0]
            placeholder.append(
                etree.Element('button', {
                    'name': 'action_product_form',
                    'type': 'object',
                    'icon': 'fa-external-link',
                    'string': _('Open Product Form View'),
                }))

            # make tree view editable
            for node in doc.xpath("/tree"):
                node.set('edit', 'true')
                node.set('create', 'false')
                node.set('editable', 'top')
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    def write(self, vals):
        if self._context.get('stock_request_products') and 'qty_request' in vals:
            for rec in self:
                rec._set_qty_request(vals['qty_request'])
            return True
        return super().write(vals)
