##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from . import models
from . import wizard
from . import demo
from odoo.addons.l10n_ar_withholding.models.account_payment import AccountPayment
from odoo.tools.sql import column_exists, table_exists
import logging

_logger = logging.getLogger(__name__)


def monkey_patch_synchronize_to_moves():
    def _synchronize_to_moves(self, changed_fields):
        # Neutralize l10n_ar_withholding's _synchronize_to_moves override, which manually unlinks
        # the withholding lines on every sync ("synchronization mechanism is not implemented yet").
        # Since l10n_ar_tax now keeps withholding lines as display_type='product', the standard
        # sync handles them correctly, so we skip that manual-unlink override and call super directly.
        return super(AccountPayment, self)._synchronize_to_moves(changed_fields)

    AccountPayment._synchronize_to_moves = _synchronize_to_moves


def _l10n_ar_tax_pre_init(env):
    """Create the new account.payment columns before the ORM does.

    `l10n_ar_fiscal_position_id` and `withholdable_advanced_amount` are stored computed fields,
    so on install Odoo creates their column and queues a recompute for every existing payment.
    On databases with a large payment history that sweep takes longer than the worker time limit
    and the install dies half way through.

    Creating the columns here makes Field.update_db see them as already existing and skip the
    recompute. Historical payments keep exactly the value the compute would give them: no fiscal
    position (it is only set on draft supplier payments of argentinian companies) and the current
    unreconciled amount as the advance, filled in a single statement.
    """
    if not table_exists(env.cr, "account_payment"):
        return
    env.cr.execute(
        """
        ALTER TABLE account_payment
            ADD COLUMN IF NOT EXISTS l10n_ar_fiscal_position_id integer,
            ADD COLUMN IF NOT EXISTS withholdable_advanced_amount numeric
        """
    )
    if column_exists(env.cr, "account_payment", "unreconciled_amount"):
        env.cr.execute("UPDATE account_payment SET withholdable_advanced_amount = unreconciled_amount")


def _l10n_ar_update_taxes(env):
    """Al instalar este módulo, en caso de que existan compañías responsable inscripto argentinas y con plan de cuentas
    ajustamos ciertos datos de los impuestos
    TODO la mayoria de esto deberia implementarse en odoo standard
    """

    # si tiene instalado chart ri o exento le actualizamos impuestos
    companies = env["res.company"].search([("chart_template", "in", ("ar_base", "ar_ri", "ar_ex"))])
    for company in companies:
        env["account.chart.template"]._add_wh_taxes(company)

    # Dejamos registro en los logs de las compañías en las cuales se estableció el código de impuesto
    if companies:
        _logger.info(
            "Se agregaron los códigos de impuestos correspondientes para retenciones de ganancias aplicadas y retenciones de iva aplicadas y las etiquetas de impuestos para compañías %s."
            % ", ".join(companies.mapped("name"))
        )
