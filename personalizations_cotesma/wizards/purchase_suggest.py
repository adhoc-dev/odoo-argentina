from odoo import models, fields, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError

class PurchaseSuggestPrCreate(models.TransientModel):
    _name = 'purchase.suggest.pr.create'
    _description = 'PurchaseSuggestPrCreate'

    only_update_if_same_user = fields.Boolean(
        default=True,
        string='Solo actualizar si mismo usuario',
        help='Solo se va a actualizar el PC si existe un PC generado '
        'por mi usuario, si no se va a generar uno nuevo.',
    )

    requisition_type_id = fields.Many2one(
       'purchase.requisition.type', default=lambda x:x.env['purchase.requisition']._get_type_id())

    def _prepare_purchase_requisition(self, company, pick_type):
        pr_vals = {
            'company_id': company.id,
            'picking_type_id': pick_type.id,
            'type_id': self.requisition_type_id.id,
        }
        return pr_vals

    def _prepare_purchase_requisition_line(
            self, product, uom, new_pr):
        vals = {
            'product_id': product.id,
            'requisition_id': new_pr.id,
            'product_uom_id': uom.id,
            'product_qty': 1.0,
            'name': product.name,
        }
        return vals

    def _location2pickingtype(self, company, location):
        spto = self.env['stock.picking.type']
        pick_type_dom = [
            ('code', '=', 'incoming'),
            ('warehouse_id.company_id', '=', company.id)]
        pick_types = spto.search(
            pick_type_dom + [(
                'default_location_dest_id',
                'child_of',
                location.location_id.id)])
        if not pick_types:
            pick_types = spto.search(pick_type_dom)
            if not pick_types:
                raise UserError(_(
                    "Make sure you have at least an incoming picking "
                    "type defined"))
        return pick_types[0]


    def _create_update_purchase_requisition(
            self, company, pr_lines, location):
        self = self.with_context(company_id=company.id)
        prl = self.env['purchase.requisition.line']
        pr = self.env['purchase.requisition']
        pick_type = self._location2pickingtype(company, location)
        domain = [
            ('company_id', '=', company.id),
            ('state', '=', 'draft'),
            ('picking_type_id', '=', pick_type.id),
        ]
        if self.only_update_if_same_user:
            domain += [('create_uid', '=', self.env.user.id)]

        existing_pos = pr.search(domain)
        if existing_pos:
            # update the first existing PO
            existing_pr = existing_pos[0]
            for product, qty_to_order, uom in pr_lines:
                existing_prlines = prl.search([
                    ('product_id', '=', product.id),
                    ('requisition_id', '=', existing_pr.id),
                ])
                if existing_prlines:
                    existing_prline = existing_prlines[0]
                    existing_prline.product_qty += uom._compute_quantity(
                        qty_to_order, existing_prline.product_uom_id)
                else:
                    prl_vals = self._prepare_purchase_requisition_line(
                        product, uom, existing_pr)
                    new_pr_line = prl.create(prl_vals)
                    new_pr_line.product_qty = qty_to_order
            existing_pr.message_post(
                body='Purchase requisition updated from purchase suggestions.')
            return existing_pr
        else:
            # create new PR
            pr_vals = self._prepare_purchase_requisition(company, pick_type)
            new_pr = pr.create(pr_vals)
            for product, qty_to_order, uom in pr_lines:
                prl_vals = self._prepare_purchase_requisition_line(
                    product, uom, new_pr)
                new_pr_line = prl.create(prl_vals)
                new_pr_line.product_qty = qty_to_order
            return new_pr

    def create_pr(self):
        self.ensure_one()
        pr_to_create = {}
        psuggest_ids = self.env.context.get('active_ids')
        location = False
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in self.env['purchase.suggest'].browse(psuggest_ids):
            if not location:
                location = line.location_id
            if float_is_zero(line.qty_to_order, precision_digits=precision):
                continue
            pr_to_create.setdefault(
                (line.company_id), []).append(
                (line.product_id, line.qty_to_order, line.uom_po_id))
        if not pr_to_create:
            raise UserError(_('No purchase requisition created or updated'))
        pr_ids = []
        for company, pr_lines in pr_to_create.items():
            assert location, 'No stock location'
            pr = self._create_update_purchase_requisition(
                company, pr_lines, location)
            pr_ids.append(pr.id)
        action = self.env["ir.actions.actions"]._for_xml_id('purchase_requisition.action_purchase_requisition')
        action['domain'] = [('id', 'in', pr_ids)]
        return action
