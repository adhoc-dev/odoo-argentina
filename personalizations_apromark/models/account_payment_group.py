from odoo import models, fields


class AccountPaymentGroup(models.Model):

    _inherit = 'account.payment.group'

    fecha_comprobante = fields.Date(string='Fecha del Comprobante')
    nro_comprobante = fields.Char(string='Nro de Comprobante')
    nro_cuota = fields.Char(string='Nro de Cuota', compute='_compute_payment_group_vals')
    mes = fields.Char(string='Mes', compute='_compute_payment_group_vals')
    collector_id = fields.Many2one('res.users',string='Cobrado por', copy=False,default=lambda self: self.env.user)
    payments_amount = fields.Monetary(store=True)

    def _compute_payment_group_vals(self):
        for payment in self:
            invoice = payment.matched_move_line_ids.move_id
            order = invoice.invoice_line_ids.mapped('sale_line_ids').order_id
            subscription = invoice.invoice_line_ids.subscription_id
            if len(invoice) == 1 and (order or subscription):
                if order:
                    payment.nro_cuota = subscription.cuota_inicial
                    payment.mes = invoice.invoice_date.month
                elif subscription:
                    # Get the invoices related to the subscription
                    invoices = self.env['account.move'].search(
                        [('invoice_line_ids.subscription_id', '=', subscription.id)])
                    # Set the position of the invoice in the subscription
                    payment.nro_cuota = invoices.sorted(lambda i: (i.invoice_date, i.id)).ids.index(invoice.id) + subscription.cuota_inicial
                    payment.mes = "Certificación" if payment.nro_cuota == '13' else invoice.invoice_date.month
            else:
                payment.nro_cuota = None
                payment.mes = None
