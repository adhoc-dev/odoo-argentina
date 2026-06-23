from odoo import api, fields, models
from odoo.tools import formatLang


class AccountMove(models.Model):
    """Heredamos todos los metodos que de alguna manera llamen a tax.compute_all y les pasamos la fecha"""

    _inherit = "account.move"

    perceptions_fiscal_positon = fields.Boolean(
        compute="_compute_perceptions_fiscal_position",
    )

    def _compute_perceptions_fiscal_position(self):
        """
        Compute if the fiscal position has perceptions.
        """
        for move in self:
            move.perceptions_fiscal_positon = bool(
                move.fiscal_position_id.l10n_ar_tax_ids.filtered(lambda x: x.tax_type == "perception")
            )

    def _get_tax_factor(self):
        self.ensure_one()
        tax_factor = self.amount_total and (self.amount_untaxed / self.amount_total) or 1.0
        doc_letter = self.l10n_latam_document_type_id.l10n_ar_letter
        # if we receive B invoices, then we take out 21 of vat
        # this use of case if when company is except on vat for eg.
        if tax_factor == 1.0 and doc_letter == "B":
            tax_factor = 1.0 / 1.21
        return tax_factor

    def write(self, vals):
        res = super().write(vals)
        # Si el invoice_date cambia, recomputamos las percepciones.
        # En Odoo 18+, cuando el guardado viene de un formulario (UI), los 'tax_ids' de las líneas
        # suelen estar presentes en los 'vals' (dentro de 'invoice_line_ids').
        # Si el usuario editó las líneas, no queremos re-ejecutar nuestra lógica de refresco automático.
        if "invoice_date" in vals and "invoice_line_ids" not in vals:
            self._l10n_ar_recompute_fiscal_position_taxes()
        return res

    @api.onchange("invoice_date", "commercial_partner_id")
    def _l10n_ar_recompute_fiscal_position_taxes(self):
        """Recalculamos las percepciones si cambiamos la fecha de la orden de venta o el commercial partner.
        IMPORTANTE: este metodo solo esta pensado para cambiar alicuota de MISMA fiscal position (por cambio en fecha o partner) pero no para cambiar los impuestos.
        Para ello nos basamos en los impuestos de la posicion fiscal, buscamos si hay impuestos existentes para los tax groups involucrados y los
        reemplazamos por los nuevos impuestos.
        NO lo hacemos para el cambio de fiscal_position_id porque el onchange de fiscal_position_id implementado en sale_ux ya recomputa todos los taxes
        """
        for move in self.filtered(
            lambda x: x.is_sale_document(include_receipts=True) and x.perceptions_fiscal_positon and x.state == "draft"
        ):
            fp_tax_groups = move.fiscal_position_id.l10n_ar_tax_ids.filtered(
                lambda x: x.tax_type == "perception"
            ).mapped("default_tax_id.tax_group_id")
            new_taxes = move.fiscal_position_id._l10n_ar_add_taxes(
                move.partner_id, move.company_id, move.date, "perception"
            )
            # Solo queremos que se recomputen los impuestos en facturas de cliente/proveedor
            for line in move.filtered(lambda x: not x.reversed_entry_id).invoice_line_ids:
                to_unlink = line.tax_ids.filtered(lambda x: x.tax_group_id in fp_tax_groups)
                if to_unlink._origin != new_taxes:
                    line.tax_ids = (line.tax_ids - to_unlink) | new_taxes

    def copy(self, default=None):
        """Re computamos las percepciones al duplicar una factura porque puede ser que la factura venga de otro periodo
        o por alguna razón las percepciones hayan cambiado
        """
        recs = super().copy(default=default)
        recs._l10n_ar_recompute_fiscal_position_taxes()
        return recs

    # -------------------------------------------------------------------------
    # Régimen de Transparencia Fiscal (Ley 27.743) — Percepciones de IIBB
    # -------------------------------------------------------------------------
    # Reutilizamos el cuadro de transparencia fiscal nacional ya existente en
    # l10n_ar (`_l10n_ar_get_invoice_custom_tax_summary_for_report`, que arma las
    # líneas de IVA Contenido / Otros Impuestos Nacionales) y le agregamos, a
    # continuación, una línea por cada percepción de Ingresos Brutos discriminada
    # por jurisdicción, según las resoluciones provinciales de transparencia
    # fiscal a consumidor final (ATER 128/2026 ER, AGIP 169/2026 CABA,
    # ARECH 468/2026 Chubut). La leyenda se deriva de la jurisdicción del impuesto
    # y se puede ajustar por provincia desde `_L10N_AR_IIBB_TRANSPARENCY_LEGENDS`.

    # Leyendas exactas exigidas por la norma de cada provincia.
    # Clave: código de provincia (res.country.state.code).
    # Valor: (leyenda, mostrar_alicuota).
    _L10N_AR_IIBB_TRANSPARENCY_LEGENDS = {
        "C": ("ALÍCUOTA ISIB CABA", True),                 # AGIP 169/2026 (texto exacto exigido)
        "U": ("VALOR APROXIMADO DEL ISIB CHUBUT", False),  # ARECH 468/2026 (solo importe)
    }

    def _l10n_ar_iibb_transparency_legend(self, tax):
        """Devuelve (leyenda, mostrar_alicuota) para la línea de IIBB de la
        jurisdicción del impuesto. Por defecto usa el nombre de la provincia y
        muestra la alícuota; las provincias con texto legal exacto se
        sobreescriben en `_L10N_AR_IIBB_TRANSPARENCY_LEGENDS`."""
        self.ensure_one()
        state = tax.l10n_ar_state_id
        return self._L10N_AR_IIBB_TRANSPARENCY_LEGENDS.get(
            state.code,
            (state.name or tax.tax_group_id.name, True),
        )

    def _l10n_ar_get_invoice_custom_tax_summary_for_report(self):
        """Extiende el cuadro de Transparencia Fiscal agregando una línea por cada
        percepción de Ingresos Brutos (tributo ARCA 07), a continuación del IVA.
        La alícuota se toma del impuesto configurado (`tax.amount`), igual que la
        localización deriva la alícuota de las percepciones."""
        results = super()._l10n_ar_get_invoice_custom_tax_summary_for_report()
        # Mismo alcance que el régimen nacional: solo Facturas B (códigos 6/7/8).
        if self.l10n_latam_document_type_id.code not in ("6", "7", "8"):
            return results

        base_lines, _tax_lines = self._get_rounded_base_and_tax_lines()
        AccountTax = self.env["account.tax"]

        def grouping_function(_base_line, tax_data):
            if not tax_data:
                return None
            tax = tax_data["tax"]
            if tax.tax_group_id.l10n_ar_tribute_afip_code != "07":
                return None
            return {"tax_id": tax.id}

        base_lines_aggregated_values = AccountTax._aggregate_base_lines_tax_details(base_lines, grouping_function)
        values_per_grouping_key = AccountTax._aggregate_base_lines_aggregated_values(base_lines_aggregated_values)
        for grouping_key, values in values_per_grouping_key.items():
            if not grouping_key:
                continue
            tax = AccountTax.browse(grouping_key["tax_id"])
            legend, show_aliquot = self._l10n_ar_iibb_transparency_legend(tax)
            if show_aliquot:
                name = "%s %s%%" % (legend, formatLang(self.env, tax.amount))
            else:
                name = legend
            results.append({
                "name": name,
                "tax_amount_currency": values["tax_amount_currency"],
                "formatted_tax_amount_currency": formatLang(self.env, values["tax_amount_currency"]),
            })
        return results
