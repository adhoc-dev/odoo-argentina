from odoo import models, fields


class AccountPaymentGroup(models.Model):

    _inherit = 'account.payment.group'

    fecha_comprobante = fields.Date(string='Fecha del Comprobante')
    nro_comprobante = fields.Char(string='Nro de Comprobante')
    nro_cuota = fields.Char(string='Nro de Cuota', compute='_compute_payment_group_vals')
    mes = fields.Char(string='Mes', compute='_compute_payment_group_vals')

    def _compute_payment_group_vals(self):
        for payment in self:
            invoice = payment.matched_move_line_ids.move_id
            order = invoice.invoice_line_ids.mapped('sale_line_ids').order_id
            subscription = invoice.invoice_line_ids.subscription_id
            if len(invoice) == 1 and (order or subscription):
                if order:
                    payment.nro_cuota = '1'
                    payment.mes = invoice.invoice_date.month
                elif subscription:
                    payment.nro_cuota = payment._get_invoice_position(subscription.id, invoice.id)
                    if payment.nro_cuota == '13':
                        payment.mes = "Certificación"
                    else:
                        payment.mes = invoice.invoice_date.month
            else:
                payment.nro_cuota = None
                payment.mes = None

    def _get_invoice_position(self, subscription_id, invoice_id):
        ''' Returns the position of an invoice between the invoices related to a subscription sorted by invoice date '''
        invoices = self.env['account.move'].search([('invoice_line_ids.subscription_id', '=', subscription_id)])
        for i, invoice in enumerate(invoices.sorted(lambda i: (i.invoice_date, i.id))):
            if invoice.id == invoice_id:
                return i + 1
