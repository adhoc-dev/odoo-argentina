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

    def get_base_url(self):
        self.ensure_one()
        if self._context.get('website_domain'):
            return self._context.get('website_domain')
        else:
            return super().get_base_url()


class PaymentLinkWizard(models.TransientModel):
    _inherit = 'payment.link.wizard'

    def _generate_link(self):
        # Hacemos esto para agregar una clave de contexto y en el metodo get_base_url tomar el dominio de la compañia (ya que cada colegio tiene su dominio)
        # y así evitar que todas tenga como url en el link de pago https:www.activelearning.com.ar/
        website = self.company_id and self.env['website'].search(
            [('company_id', '=', self.company_id.id), ('domain', '!=', False)], limit=1)
        if website:
            self = self.with_context(website_domain=website.get_base_url())
        super(PaymentLinkWizard, self)._generate_link()
