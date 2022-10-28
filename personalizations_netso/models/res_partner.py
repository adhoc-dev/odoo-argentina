from odoo import models, fields
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_invoicing_company_id = fields.Many2one('res.company', string="Compañia de Facturacion de Proveedor", required=False)
    average_due_days = fields.Float("Promedio", readonly=True)

    def ir_cron_update_avg_payment_days(self):
        self.search([]).action_compute_average_due_days()

    def action_compute_average_due_days(self):
        today = fields.Date.context_today(self)
        show_average_info = self.env.context.get('show_average_info')
        msg = "Facturas:\n"

        received_third_check = self.env.ref("account_check.account_payment_method_received_third_check")
        init_date = self.env['ir.config_parameter'].sudo().get_param('p13n_netso.average_due_init_date', '2022-09-21')
        from_date = fields.Date.to_date(init_date)
        for partner in self:
            # Buscar todas las facturas que han sido publicadas
            invoices = partner.invoice_ids.filtered(lambda x: x.state == 'posted' and x.invoice_date_due and x.invoice_date >= from_date)
            average_due_days = []
            for inv in invoices:
                payment_days = []
                for payment_group in inv.payment_group_ids:
                    for payment in payment_group.payment_ids:
                        payment_date = payment.payment_date if payment.payment_method_id != received_third_check else payment.check_payment_date
                        payment_days.append((payment_date - inv.invoice_date_due).days)

                payment_days = sorted(payment_days)
                # Si la factura esta vencida y nohay pagos
                if inv.invoice_date_due < today and not inv.invoice_payment_state != 'paid' and not payment_days:
                    average_due_days.append((today - inv.invoice_date_due).days)
                else:
                    average_due_days.append(max(payment_days, default=0))

                if show_average_info:
                    msg += "* (%s) %s Venc. %s - %s / %s - Pagos %s Final %s\n" % (
                        inv.id, inv.name,
                        inv.invoice_date_due,
                        inv.state, inv.invoice_payment_state,
                        payment_days, average_due_days[-1])

            res = sum(average_due_days) / (len(average_due_days) or 1)
            msg += " patner %s %s promedio (%s) %s res %s\n" % (partner.id, partner.name, len(average_due_days), average_due_days, res)
            partner.average_due_days = res
            if show_average_info:
                raise UserError(msg)
