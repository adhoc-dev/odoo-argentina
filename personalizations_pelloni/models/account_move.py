from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _generate_payment_direct_debit(self):
        to_pay_moves = self.filtered(
        lambda x: x.direct_debit_mandate_id and x.invoice_payment_state == 'not_paid' and x.type == 'out_invoice')
        for rec in to_pay_moves:
            subscription = rec.invoice_line_ids.mapped('subscription_id')
            payment = rec.env['account.payment'].with_context(active_model=False, active_ids=False, create_from_expense=True).create({
                    # 'invoice_ids': [(4, rec.id, None)],
                    'journal_id': rec.direct_debit_mandate_id.journal_id.id,
                    'payment_method_id': rec.env.ref('account_direct_debit.payment_method_direct_debit').id,
                    'direct_debit_mandate_id': rec.direct_debit_mandate_id.id,
                    'amount': rec.amount_residual,
                    'currency_id': rec.currency_id.id,
                    'payment_type': 'inbound',
                    # TODO evaluar si no debería tomar primero payment_ref? que hace odoo en otros lugares
                    'communication': rec.name or rec.ref or subscription.name,
                    'partner_type': 'customer' if rec.type == 'out_invoice' else 'supplier',
                    'partner_id': rec.partner_id.commercial_partner_id.id,
                    'payment_date': rec.invoice_date_due or rec.invoice_date
                })
            payment.post()
            payment.write({'invoice_ids': [(4, rec.id, None)]})

            (payment.move_line_ids + rec.line_ids).filtered(
                lambda line: not line.reconciled and line.account_id == payment.destination_account_id and not (line.account_id == line.payment_id.writeoff_account_id and line.name == line.payment_id.writeoff_label)).reconcile()
