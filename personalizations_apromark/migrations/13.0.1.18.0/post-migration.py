from openupgradelib import openupgrade
import logging
_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info('Se establecen los collector_id en account.payment.group')
    for payment in env['account.payment.group'].search([]):
        payment.collector_id = payment.create_uid
