from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
import dateutil


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_fecha_segundo_venc = fields.Date(string="Fecha segundo vencimiento", compute="_compute_x_fecha_segundo_venc", help="Es la fecha del segundo vencimiento de la factura", readonly=True, copy=False, store=True)
    x_invoice_nd_id = fields.Many2one(string="ND relacionada", comodel_name="account.move", on_delete="set null", readonly=True, copy=False)
    x_monto_cargo = fields.Monetary(string="Importe con recargo", compute="_compute_x_monto_cargo", readonly=True, copy=False)
    x_state_invoice = fields.Selection(
      string="Estado de vencimiento de factura",
      selection=[('vencida', 'Vencida'),('vencida_sin_nd', 'Vencida sin ND emitida'),('no_vencida', 'No vencida')],
      compute="_compute_x_state_invoice",
      search="_search_x_state_invoice",
      copy=False)

    @api.depends('invoice_date_due', 'invoice_date')
    def _compute_x_fecha_segundo_venc(self):
        for rec in self:
          if rec.invoice_date_due:
            date = rec.invoice_date_due + dateutil.relativedelta.relativedelta(days=rec.company_id.x_rango_fecha_recargo)
            rec.x_fecha_segundo_venc = datetime.strftime(date, "%Y-%m-%d")
          else:
            rec.x_fecha_segundo_venc = False

    @api.depends('sale_order_ids', 'amount_total')
    def _compute_x_monto_cargo(self):
        self.x_monto_cargo = 0.0
        for rec in self.filtered('sale_order_ids'):
            rec.x_monto_cargo = rec.amount_total * (1 + (rec.sale_order_ids[0].pricelist_id.x_porcentaje_cargo_extra) / 100)

    def _compute_x_state_invoice(self):
        # NOTE: We are not able to set this field as stored beause we need to compute the value daily so we need that the field
        # is auto updated everydate, actually every moment that the user try to show or search by this field.
        for rec in self:
          x_state_invoice = 'no_vencida'
          if rec.state != 'posted' or rec.invoice_payment_state == 'paid':
            rec.x_state_invoice = x_state_invoice
            continue
          if rec.invoice_date_due and rec.invoice_date_due < fields.Date.context_today(rec):
            x_state_invoice = 'vencida'
          if x_state_invoice == 'vencida' and not rec.x_invoice_nd_id:
            x_state_invoice = 'vencida_sin_nd'
          rec.x_state_invoice = x_state_invoice

    def _search_x_state_invoice(self, operator, value):
        """ Compute the search on the field 'x_state_invoice' """
        if isinstance(value, str):
            value = [value]
        value = [v for v in value if v in ['vencida', 'vencida_sin_nd', 'no_vencida']]
        if operator not in ('in', '=') or not value:
            return []
        invoice_state_data = self._query_x_state_invoice()
        return [('id', 'in', [d['id'] for d in invoice_state_data if d['x_state_invoice'] in value])]

    def _query_x_state_invoice(self):
        sql = """
            SELECT id,
                CASE WHEN (state != 'posted' OR invoice_payment_state = 'paid') THEN 'no_vencida'
                     WHEN (x_invoice_nd_id IS NULL) THEN 'vencida_sin_nd'
                     WHEN (x_invoice_nd_id IS NOT NULL) THEN 'vencida'
                     ELSE 'no_vencida'
                END AS x_state_invoice
            FROM account_move
              WHERE (invoice_date_due IS NOT NULL AND invoice_date_due < %(today)s)
          """
        params = {
            'today': fields.Date.context_today(self),
        }
        self.env['account.move'].flush()
        self.env.cr.execute(sql, params)
        result = self.env.cr.dictfetchall()
        return result

    def create_debt_invoice(self):
        def prepare_interest_invoice(partner):
            comment = "Recargo por mora de la factura {}".format(self.name)

            invoice_vals = {
                'narration': comment,
                'invoice_origin': self.name,
                'invoice_payment_term_id': partner.property_payment_term_id.id or False,
            }
            return invoice_vals

        def prepare_interest_invoice_line(invoice, partner, amount):
            company = self.company_id
            try:
              product = self.env['product.product'].browse(PRODUCT_ID)
            except Exception:
              raise UserError("No tienen configurado el producto")
            line_values = {}
            line_data = self.env['account.move.line'].with_context(
                force_company=company.id).new(dict(
                    product_id=PRODUCT_ID,
                    quantity=1.0,
                    move_id=invoice.id,
                    partner_id=partner.id,
                ))
            line_data._onchange_product_id()
            line_data._onchange_balance()

            if not line_data.account_id:
                raise UserError(
                    'El producto {} no esta correctamente configurado, falta la cuenta contable.'.format(product.name))

            line_data['price_unit'] = amount
            line_data['name'] = line_data.product_id.name + '.\n' + invoice.narration

            for field in line_data._cache:
              line_values[field] = line_data[field]
            values = line_data._convert_to_write(line_values)
            return values

        def create_invoice():
            partner = self.partner_id
            amount = self.x_monto_cargo - self.amount_total
            debit_note = self.env['account.debit.note'].with_context(active_model="account.move",active_ids=self.ids).create({
              'copy_lines': False,
            })
            action = debit_note.create_debit()
            invoice = self.env['account.move'].browse(action['res_id'])
            invoice.write(prepare_interest_invoice(partner))
            invoice.with_context(internal_type='debit_note').write({'invoice_line_ids': [(0,0,prepare_interest_invoice_line(invoice, partner, amount))]})
            invoice._recompute_dynamic_lines()
            invoice._onchange_invoice_line_ids()
            invoice.message_post(body="Factura de recargo por mora creada de la factura {}".format(self.l10n_latam_document_number))
            return invoice
        self.ensure_one()
        PRODUCT_ID = int(self.env['ir.config_parameter'].sudo().get_param('product.nd_mora'))
        invoice = create_invoice()
        self.x_invoice_nd_id = invoice
        action_read = self.env["ir.actions.actions"]._for_xml_id('account.action_move_out_invoice_type')
        res = self.env.ref('account.view_move_form', False)
        action_read['views'] = [(res and res.id or False, 'form')]
        action_read['res_id'] = invoice.id
        return action_read

    def action_post(self):
      if ((self.type == 'out_refund' or self.type == 'in_refund') and not self.env.user.has_group('personalizations_sba.group_validate_credit_note')):
          raise UserError("No tiene permiso para validar notas de crédito")
      return super().action_post()
