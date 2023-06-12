from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_fecha_cobro_esperado = fields.Date(string="Fecha esperada de cobro",
                                compute='_compute_fecha_cobro_esperado',
                                store=True, readonly=False)


    @api.depends('partner_id')
    def _compute_fecha_cobro_esperado(self):
        date = fields.Date.today()
        for rec in self:
            if rec.partner_id.x_plazo_cobro_esperado:
                rec.x_fecha_cobro_esperado = date + relativedelta(days=rec.partner_id.x_plazo_cobro_esperado)
