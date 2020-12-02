from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    x_fecha_segundo_venc = fields.Date(string="Fecha segundo vencimiento", compute="_compute_x_fecha_segundo_venc", help="Es la fecha del segundo vencimiento de la factura", readonly=True, copy=False, store=True)
    x_invoice_nd_id = fields.Many2one(string="ND relacionada", comodel_name="account.invoice", on_delete="set null", readonly=True, copy=False)
    x_monto_cargo = fields.Monetary(string="Importe con recargo", compute="_compute_x_monto_cargo", readonly=True, copy=False, store=True)
    x_state_invoice = fields.Selection(string="Estado de vencimiento de factura", selection=[('vencida', 'Vencida'),('vencida_sin_nd', 'Vencida sin ND emitida'),('no_vencida', 'No vencida')], compute="_compute_x_state_invoice", readonly=True, copy=False, store=True)

    @api.depends('date_due','date_invoice')
    def _compute_x_fecha_segundo_venc(self):
        for rec in self:
          if rec.date_due:
            date = datetime.datetime.strptime(rec.date_due, "%Y-%m-%d") + dateutil.relativedelta.relativedelta(days=rec.company_id.x_rango_fecha_recargo)
            rec['x_fecha_segundo_venc'] = datetime.datetime.strftime(date, "%Y-%m-%d")
          else:
            rec['x_fecha_segundo_venc'] = False

    @api.depends('sale_order_ids','amount_total')
    def _compute_x_monto_cargo(self):
        for rec in self.filtered('sale_order_ids'):
          rec['x_monto_cargo'] = rec.amount_total * (1 + (rec.sale_order_ids[0].pricelist_id.x_porcentaje_cargo_extra)/ 100)

    @api.depends('date_due','x_invoice_nd_id','state')
    def _compute_x_state_invoice(self):
        for rec in self:
          x_state_invoice = 'no_vencida'
          if rec.state != 'open':
            rec['x_state_invoice'] = x_state_invoice
            continue
          if rec.date_due < datetime.datetime.today().strftime("%Y-%m-%d"):
            x_state_invoice = 'vencida'
          if x_state_invoice == 'vencida' and  not rec.x_invoice_nd_id:
            x_state_invoice = 'vencida_sin_nd'
          rec['x_state_invoice'] = x_state_invoice
