from odoo import _, models, fields
from odoo.exceptions import UserError


class AccountMove(models.Model):

    _inherit = 'account.move'

    payment_link = fields.Char()

    def validate_and_send(self):
        if self._context.get('active_model') == 'account.move':
            domain = [('id', 'in', self._context.get('active_ids', []))]
        else:
            raise UserError(_("Missing 'active_model' in context."))

        moves = self.env['account.move'].search(domain).filtered('line_ids')
        moves_to_post = moves.filtered(lambda m: m.state == 'draft')
        moves_to_post._post()

        for move in moves.filtered(lambda m: m.state == 'posted'):
            vals_list = self.env['payment.link.wizard'].default_get([])
            payment = self.env['payment.link.wizard'].create(vals_list)
            move.payment_link = payment.link
            template_id = self.env.ref(
                'p13n_integra.email_template_payment_link').id
            move.message_post_with_template(template_id)
        return {'type': 'ir.actions.act_window_close'}
