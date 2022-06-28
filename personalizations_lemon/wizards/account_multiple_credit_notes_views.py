from odoo import fields, models, api


class AccountSetDate(models.TransientModel):
    _name = 'account.create.multiple.credit.notes'
    _description = 'Set Invoice Date'

    @api.model
    def get_moves(self):
        moves = self.env['account.move'].browse(
            self._context.get('active_ids', False))
        return moves

    invoice_date = fields.Date(string="Fecha", required=True, default=fields.Date.today())
    move_ids = fields.Many2many(
        'account.move',
        default=get_moves
    )

    def confirm(self):
        date = self.invoice_date
        for inv in self.move_ids:
            refund_wizard = self.env['account.move.reversal'].with_context(
                active_ids=[inv.id], active_model='account.move').create({
                    'refund_method': 'refund',
                    'move_id': inv.id,
                    'date': date})
            refund_wizard._onchange_move_id()
            res = refund_wizard.reverse_moves()
            refund = self.env['account.move'].browse(res['res_id'])
            refund.write({'pay_now_journal_id': inv.pay_now_journal_id.id})
        return {'type': 'ir.actions.act_window_close'}
