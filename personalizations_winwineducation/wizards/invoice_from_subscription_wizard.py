from odoo import models, fields
from odoo.exceptions import UserError


class InvoiceFromSubscriptionWizard(models.TransientModel):
    _name = 'invoice.create_from_subscription.wizard'
    _description = 'Crear Factura desde Suscripción'

    def _domain_company(self):
        company = self.env.company
        return ['|', ('company_id', '=', False), ('company_id', '=', company.id)]

    product_ids = fields.Many2many('product.product', string='Product', domain=_domain_company)

    def create_from_subscription(self):
        def prepare_invoice_line(invoice, partner, product):
            company = invoice.company_id

            line_values = {}
            line_data = self.env['account.move.line'].with_context(force_company=company.id).new(dict(
                product_id=product,
                quantity=1.0,
                move_id=invoice.id,
                partner_id=partner.id,
            ))
            line_data._onchange_product_id()
            line_data._onchange_balance()
            if not line_data.account_id:
                raise UserError(
                    'El producto {} no esta correctamente configurado, falta la cuenta contable.'.format(product.name))
            for field in line_data._cache:
                line_values[field] = line_data[field]
            line_values['subscription_id'] = subscription.id
            values = line_data._convert_to_write(line_values)
            return values

        def prepare_invoice_data():
            values = subscription._prepare_invoice_data()
            reference = subscription.partner_id.name + ' - ' + subscription.name + ' - ' + 'Reserva de vacante'
            values['ref'] = reference
            values['narration'] = ''
            values['invoice_origin'] = subscription.display_name
            return values

        sale_subscriptions = self.env['sale.subscription'].browse(self._context.get('active_ids', []))

        if not self.product_ids:
            raise UserError(_('Debe haber al menos un producto'))

        invoice_line_obj = self.env['account.move.line']
        invoice_obj = self.env['account.move']
        invoices = []

        for subscription in sale_subscriptions:
            invoice_vals = prepare_invoice_data()
            invoice = invoice_obj.create(invoice_vals)
            for product in self.product_ids:
                invoice.invoice_line_ids += invoice_line_obj.new(prepare_invoice_line(invoice, invoice.partner_id, product))
            invoice._recompute_dynamic_lines()
            invoice._onchange_invoice_line_ids()
            invoices.append(invoice.id)

        action = self.env["ir.actions.actions"]._for_xml_id('account.action_move_out_invoice_type')
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices)]
        elif len(invoices) == 1:
            action['views'] = [(self.env.ref(
                'account.view_move_form').id, 'form')]
            action['res_id'] = invoices[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
