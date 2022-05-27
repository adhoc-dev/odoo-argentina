from openupgradelib import openupgrade
import logging
_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    # Lo hacemos asi porque el registro moneda tiene la opcion de noupdate
    # queremos que esta siga estando pero solo modificar este valor en
    # especifico
    _logger.info('We change ARS displayname to show in the invoice report')
    env.ref('base.ARS').currency_unit_label = 'Pesos'
