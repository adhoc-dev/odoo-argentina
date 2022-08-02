from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    # Esta herencia es para cuando se llama a la acción "action_send_multiple_rfq_mail" poder modificar el estado de las
    # PO a enviado. Para esto seguimos la misma lógica que el módulo de purchase order, la diferencia es que en este
    # caso el composition_mode de la acción es de tipo "mass_mail" en vez de "comment" por lo cual Odoo termina llamando
    # al método send_mail en vez de message_post.
    def send_mail(self, **kwargs):
        res = super(MailComposeMessage, self.sudo()).send_mail(**kwargs)
        if self.env.context.get('mark_rfq_sent'):
            self.env['purchase.order'].search([('id', 'in', self._context.get('active_ids'))]).write({'state': 'sent'})
        return res
