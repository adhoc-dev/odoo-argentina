from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_task_stage = fields.Many2one(string="Etapa de las Tareas", comodel_name="project.task.type", compute="_compute_x_task_stage", on_delete="set null", track_visibility="onchange", readonly=True, copy=False)
    x_invoice_residual_amount = fields.Float(string="Saldo Factura", compute="_compute_x_invoice_residual_amount", readonly=True, copy=False, store=True)
    x_invoice_total_amount = fields.Float(string="Facturado", compute="_compute_x_invoice_total_amount", readonly=True, copy=False, store=True)
    x_sale_amount = fields.Float(string="Saldo Venta", compute="_compute_x_sale_amount", readonly=True, copy=False, store=True)
    x_studio_field_fUR9d = fields.Selection(string="USO ADMIN", selection=[['A COBRAR', 'A COBRAR'], ['CANJE', 'CANJE'], ['AJUSTE', 'AJUSTE'], ['INCOBRABLE', 'INCOBRABLE']], copy=False)
    x_studio_field_xjUhp = fields.Text(string="Ingresar las notas comenzando con la fecha", copy=False)
    x_studio_field_VU2in = fields.Many2one(string="Cliente Final", comodel_name="res.partner", on_delete="set null", copy=False)
    x_studio_field_N9ZS1 = fields.Date(string="Fecha Estimada de Cobro", copy=False)
    x_partner_shipping_street = fields.Char(string="Partner Shipping Street", related="partner_shipping_id.street", readonly=True, copy=False, store=True)
    x_partner_shipping_street2 = fields.Char(string="Partner Shipping Street2", related="partner_shipping_id.street2", readonly=True, copy=False, store=True)
    x_partner_shipping_city = fields.Char(string="Partner Shipping City", related="partner_shipping_id.city", readonly=True, copy=False, store=True)
    x_partner_shipping_state = fields.Char(string="Partner Shipping State", related="partner_shipping_id.state_id.name", help="Administrative divisions of a country. E.g. Fed. State, Departement, Canton", readonly=True, copy=False, store=True)
    x_partner_shipping_zip = fields.Char(string="Partner Shipping ZIP", related="partner_shipping_id.zip", readonly=True, copy=False, store=True)
    x_partner_shipping_id_name = fields.Char(string="Nombre Contacto Entrega", related="partner_shipping_id.name", readonly=True, copy=False, store=True)
    x_partner_shipping_id_phone = fields.Char(string="Teléfono Entrega", related="partner_shipping_id.phone", readonly=True, copy=False, store=True)
    x_partner_shipping_id_mobile = fields.Char(string="Celular Entrega", related="partner_shipping_id.mobile", readonly=True, copy=False, store=True)
    x_partner_shipping_id_email = fields.Char(string="Email Entrega", related="partner_shipping_id.email", readonly=True, copy=False, store=True)
    x_verificado = fields.Boolean(string="Verificado", copy=False)
    x_partner_invoice_id_street = fields.Char(string="Calle Facturación", related="partner_invoice_id.street", readonly=True, copy=False, store=True)
    x_partner_invoice_id_city = fields.Char(string="Ciudad Facturación", related="partner_invoice_id.city", readonly=True, copy=False, store=True)
    x_partner_invoice_id_state_id_name = fields.Char(string="Provincia Facturación", related="partner_invoice_id.state_id.name", help="Administrative divisions of a country. E.g. Fed. State, Departement, Canton", readonly=True, copy=False, store=True)
    x_partner_invoice_id_zip = fields.Char(string="CP Facturación", related="partner_invoice_id.zip", readonly=True, copy=False, store=True)
    x_partner_invoice_id_name = fields.Char(string="Nombre Contacto Facturación", related="partner_invoice_id.name", readonly=True, copy=False, store=True)
    x_partner_invoice_id_phone = fields.Char(string="Teléfono Facturación", related="partner_invoice_id.phone", readonly=True, copy=False, store=True)
    x_partner_invoice_id_mobile = fields.Char(string="Celular Facturación", related="partner_invoice_id.mobile", readonly=True, copy=False, store=True)
    x_partner_invoice_id_email = fields.Char(string="Mail Facturación", related="partner_invoice_id.email", readonly=True, copy=False, store=True)
    x_partner_invoice_id_street2 = fields.Char(string="Barrio Facturación", related="partner_invoice_id.street2", readonly=True, copy=False, store=True)
    x_partner_invoice_id_vat = fields.Char(string="N° Identificación Principal", related="partner_invoice_id.vat", readonly=True, copy=False, store=True)
    x_partner_invoice_id_id_numbers_category_id_display_name = fields.Char(string="Tipo Identificación Principal", related="partner_invoice_id.id_numbers.category_id.display_name", readonly=True, copy=False, store=True)
    x_partner_invoice_id_afip_responsability_type_id_display_name = fields.Char(string="Tipo AFIP", related="partner_invoice_id.l10n_ar_afip_responsibility_type_id.display_name", readonly=True, copy=False, store=True)
    x_total_replenishment_cost = fields.Monetary(string="Costo Total", compute="_compute_x_total_replenishment_cost", readonly=True, copy=False, store=True)
    x_margin2 = fields.Float(string="Margin2", compute="_compute_x_margin2", track_visibility="always", readonly=True, copy=False, store=True)

    @api.depends('tasks_ids.stage_id')
    def _compute_x_task_stage(self):
        for rec in self:
          for ts in rec.tasks_ids:
            if not ts.parent_id:
              rec['x_task_stage'] = ts.stage_id

    @api.depends('invoice_ids','invoice_status')
    def _compute_x_invoice_residual_amount(self):
        for rec in self.filtered('invoice_ids'):
                total = 0
                for inv in rec.invoice_ids:
                    if inv.currency_id != rec.pricelist_id.currency_id:
                        total += inv.currency_id.compute(inv.residual, rec.pricelist_id.currency_id)
                    else:
                        total += inv.residual
                rec['x_invoice_residual_amount'] = total

    @api.depends('invoice_ids','invoice_status')
    def _compute_x_invoice_total_amount(self):
        for rec in self.filtered('invoice_ids'):
                total = 0
                for inv in rec.invoice_ids:
                    if inv.currency_id != rec.pricelist_id.currency_id:
                        total += inv.currency_id.compute(inv.amount_total,
                    rec.pricelist_id.currency_id)
                    else:
                        total += inv.amount_total
                rec['x_invoice_total_amount'] = total

    @api.depends('invoice_ids','amount_total','invoice_status')
    def _compute_x_sale_amount(self):
        for rec in self:
                total = 0
                if rec.invoice_ids:
                    for inv in rec.invoice_ids:
                        if inv.currency_id != rec.pricelist_id.currency_id:
                            total += inv.currency_id.compute(inv.amount_total,
                        rec.pricelist_id.currency_id)
                        else:
                            total += inv.amount_total
                    x_sale_amount =  rec.amount_total - total
                else:
                    x_sale_amount = rec.amount_total
                rec['x_sale_amount'] = x_sale_amount

    @api.depends('order_line','margin','state')
    def _compute_x_total_replenishment_cost(self):
        for rec in self:
                total = 0
                for line in rec.order_line:
                    total += line.product_uom_qty * line.purchase_price
        rec['x_total_replenishment_cost'] = total

    @api.depends('margin','amount_untaxed','state')
    def _compute_x_margin2(self):
        for rec in self:
          if rec.amount_untaxed != 0:
            rec['x_margin2'] = (rec.margin / rec.amount_untaxed) * 100
          else:
            rec['x_margin2'] = -100
