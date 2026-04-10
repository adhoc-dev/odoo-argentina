##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _complete_values_from_session(self, session, values):
        """
        Sobrescribimos para asegurar que la fiscal position se calcule correctamente
        según el partner, no solo usando la fiscal position por defecto.
        """
        values = super()._complete_values_from_session(session, values)

        # Si hay un partner, obtenemos su fiscal position
        if values.get('partner_id'):
            partner = self.env['res.partner'].browse(values['partner_id'])
            if partner.exists():
                # Primero verificar si el partner tiene una fiscal position manual
                fiscal_position = partner.property_account_position_id

                # Si no tiene manual, buscar la automática
                if not fiscal_position:
                    fiscal_position = self.env['account.fiscal.position'].with_company(
                        values.get('company_id') or session.config_id.company_id.id
                    )._get_fiscal_position(partner)

                if fiscal_position:
                    values['fiscal_position_id'] = fiscal_position.id

        return values

    @api.model
    def _get_invoice_lines_values(self, line_values, pos_order_line):
        """
        Sobrescribimos para NO pasar tax_ids explícitamente cuando hay percepciones.
        Esto permite que account.move.line._get_computed_taxes() se ejecute y agregue
        las percepciones automáticamente.
        """
        result = super()._get_invoice_lines_values(line_values, pos_order_line)

        # Si la orden tiene posición fiscal con percepciones, NO pasamos los tax_ids
        # para permitir que el sistema los compute automáticamente
        if (pos_order_line.order_id.fiscal_position_id and
                pos_order_line.order_id.fiscal_position_id.l10n_ar_tax_ids.filtered(
                    lambda x: x.tax_type == "perception"
                )):
            # En lugar de pasar tax_ids explícitamente, no los pasamos para que
            # _compute_tax_ids() se ejecute y llame a _get_computed_taxes()
            # que agregará las percepciones
            result.pop('tax_ids', None)

        return result
