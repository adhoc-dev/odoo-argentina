from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.invoice_lines')
    def _get_invoiced(self):
        # llamado a super para que se compute con facturas vinculadas
        super()._get_invoiced()

        for rec in self:
            # agregamos facturas vinculadas por campo origin
            other_invoices = self.env['account.move'].search(
                [('invoice_origin', 'like', rec.name),
                 ('move_type', 'in', ('out_invoice', 'out_refund'))])

            if other_invoices:
                total_invoices = rec.invoice_ids | other_invoices
                rec.invoice_ids |= total_invoices
                rec.invoice_count = len(total_invoices)
