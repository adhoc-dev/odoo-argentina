from odoo import models
from odoo.exceptions import UserError


class AccountMove(models.Model):

    _inherit = 'account.move'

    def validate_and_send(self):
        if self._context.get('active_model') == 'account.move':
            domain = [('id', 'in', self._context.get('active_ids', []))]
        else:
            raise UserError(_("Missing 'active_model' in context."))

        moves = self.env['account.move'].search(domain).filtered('line_ids')
        moves_to_post = moves.filtered(lambda m: m.state == 'draft')
        moves_to_post.post()

        for move in moves:
            vals_list = self.env['payment.link.wizard'].default_get([])
            payment = self.env['payment.link.wizard'].create(vals_list)
            move.access_url = payment.link
            template_id = self.env.ref(
                'personalizations_winwineducation.payment_link').id
            move.message_post_with_template(template_id)
        return {'type': 'ir.actions.act_window_close'}
