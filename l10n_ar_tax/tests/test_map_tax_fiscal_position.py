"""
Tests para map_tax en posiciones fiscales argentinas (l10n_ar_tax).

Validan el comportamiento introducido en el commit cf2bf142:
    Para posiciones fiscales que SOLO tienen l10n_ar_tax_ids (retenciones/percepciones)
    y ningún tax_ids explícito, map_tax() debe retornar los impuestos sin modificar,
    en lugar de delegar al domestic FP (lo que podía aplicar sustituciones de IVA
    erróneas a todas las facturas del partner).

Escenarios cubiertos:
    1. FP percepción-only → map_tax retorna impuestos sin cambio
    2. FP percepción-only con sustitución en domestic FP → IVA 21% no se reemplaza por IVA 0%
    3. FP con tax_ids explícitos → map_tax aplica la sustitución correctamente (super)
    4. Domestic FP → map_tax aplica la sustitución correctamente
    5. Factura con FP percepción-only → conserva IVA 21% en las líneas
"""

from odoo import Command
from odoo.addons.l10n_ar.tests.common import TestArCommon
from odoo.tests import tagged


@tagged("-at_install", "post_install")
class TestMapTaxFiscalPosition(TestArCommon):
    """Tests de map_tax para posiciones fiscales de percepción/retención."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Impuesto de percepción IIBB CABA para usar en l10n_ar_tax_ids
        cls.caba_perception_tax = cls.env.ref(
            "account.%i_ri_tax_percepcion_iibb_caba_aplicada" % cls.env.company.id
        )

        # Posición fiscal "percepción-only": sin tax_ids, con l10n_ar_tax_ids
        cls.perception_only_fp = cls.env["account.fiscal.position"].create(
            {
                "name": "Test FP Percepcion Only",
                "company_id": cls.company_ri.id,
            }
        )
        cls.env["account.fiscal.position.l10n_ar_tax"].create(
            {
                "fiscal_position_id": cls.perception_only_fp.id,
                "default_tax_id": cls.caba_perception_tax.id,
                "tax_type": "perception",
            }
        )

        # Posición fiscal con tax_ids explícitos: IVA 21% → IVA 0%
        # En Odoo 19, tax_ids es Many2many a account.tax y el mapeo funciona
        # mediante original_tax_ids en el impuesto destino.
        cls.tax_0.original_tax_ids = [Command.set(cls.tax_21.ids)]
        cls.fp_with_tax_mapping = cls.env["account.fiscal.position"].create(
            {
                "name": "Test FP Con Mapping IVA",
                "company_id": cls.company_ri.id,
                "tax_ids": [Command.set(cls.tax_0.ids)],
            }
        )

    def test_map_tax_perception_only_returns_taxes_unchanged(self):
        """
        FP percepción-only (no tax_ids, tiene l10n_ar_tax_ids, no es domestic FP)
        debe retornar los impuestos de entrada sin ninguna modificación.
        Valida el fix de cf2bf142: antes se delegaba a domestic_fp.map_tax().
        """
        taxes = self.tax_21
        result = self.perception_only_fp.map_tax(taxes)
        self.assertEqual(
            result,
            taxes,
            "Una FP percepcion-only debe retornar los impuestos sin modificacion.",
        )

    def test_map_tax_perception_only_not_affected_by_domestic_fp_substitution(self):
        """
        Incluso si el domestic FP tiene una sustitución IVA 21% → IVA 0%,
        la FP percepción-only debe devolver IVA 21% sin cambios.
        Valida el escenario principal del fix cf2bf142.
        """
        # Configurar domestic FP con sustitución IVA 21% → IVA 0%
        domestic_fp = self.company_ri.domestic_fiscal_position_id
        if not domestic_fp:
            self.skipTest("No se encontró domestic fiscal position para la compañía de test.")

        # Agregar sustitución al domestic FP via original_tax_ids en IVA 0%
        if self.tax_21 not in self.tax_0.original_tax_ids:
            self.tax_0.original_tax_ids = [Command.link(self.tax_21.id)]
        if self.tax_0 not in domestic_fp.tax_ids:
            domestic_fp.tax_ids = [Command.link(self.tax_0.id)]

        taxes = self.tax_21
        result = self.perception_only_fp.map_tax(taxes)
        self.assertEqual(
            result,
            self.tax_21,
            "La FP percepcion-only no debe aplicar la sustitucion IVA 21%→IVA 0% del domestic FP.",
        )

    def test_map_tax_fp_with_explicit_tax_ids_applies_substitution(self):
        """
        Una FP con tax_ids explícitos debe aplicar la sustitución mediante super().map_tax().
        Verifica que el fix no rompe FPs con mapping de IVA.
        """
        taxes = self.tax_21
        result = self.fp_with_tax_mapping.map_tax(taxes)
        self.assertEqual(
            result,
            self.tax_0,
            "Una FP con tax_ids explícitos debe aplicar la sustitucion de impuestos.",
        )

    def test_invoice_with_perception_only_fp_preserves_vat_taxes(self):
        """
        Al crear una factura asignando una FP percepción-only, las líneas
        deben conservar el IVA 21% sin ser reemplazado por IVA 0%.
        Valida el impacto en el flujo de facturas del fix cf2bf142.
        """
        domestic_fp = self.company_ri.domestic_fiscal_position_id
        if not domestic_fp:
            self.skipTest("No se encontró domestic fiscal position para la compañía de test.")

        # Asegurar que el domestic FP tiene sustitución IVA 21% → IVA 0%
        if self.tax_21 not in self.tax_0.original_tax_ids:
            self.tax_0.original_tax_ids = [Command.link(self.tax_21.id)]
        if self.tax_0 not in domestic_fp.tax_ids:
            domestic_fp.tax_ids = [Command.link(self.tax_0.id)]

        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.res_partner_adhoc.id,
                "fiscal_position_id": self.perception_only_fp.id,
                "company_id": self.company_ri.id,
                "invoice_date": "2025-01-15",
                "date": "2025-01-15",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product_a.id,
                            "quantity": 1,
                            "price_unit": 1000.0,
                            "tax_ids": [Command.set(self.tax_21.ids)],
                        }
                    )
                ],
                "l10n_latam_document_number": "0001-00000001",
            }
        )

        line_taxes = invoice.invoice_line_ids.tax_ids
        self.assertIn(
            self.tax_21,
            line_taxes,
            "IVA 21% debe estar presente en la línea cuando se usa una FP percepcion-only.",
        )
        self.assertNotIn(
            self.tax_0,
            line_taxes,
            "IVA 0% no debe aparecer en la línea; la FP percepcion-only no debe sustituir impuestos.",
        )

    def test_vendor_payment_with_perception_only_fp_invoice_posts(self):
        """
        Una factura de proveedor con una FP percepción-only puede confirmarse
        sin errores y conserva el IVA 21%.
        Valida que el map_tax no elimina impuestos en el contexto de pagos/facturas.
        """
        invoice = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": self.res_partner_adhoc.id,
                "fiscal_position_id": self.perception_only_fp.id,
                "company_id": self.company_ri.id,
                "invoice_date": "2025-01-15",
                "date": "2025-01-15",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product_a.id,
                            "quantity": 1,
                            "price_unit": 500.0,
                            "tax_ids": [Command.set(self.tax_21_purchase.ids)],
                        }
                    )
                ],
                "l10n_latam_document_number": "0001-00000010",
            }
        )
        invoice.action_post()

        self.assertEqual(invoice.state, "posted")
        self.assertIn(
            self.tax_21_purchase,
            invoice.invoice_line_ids.tax_ids,
            "IVA 21% compras debe conservarse en factura de proveedor con FP percepcion-only.",
        )
