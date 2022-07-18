from odoo import models, fields
from odoo.exceptions import UserError
from odooly import Client
from odoo.tools.safe_eval import safe_eval
import re
import datetime
import logging

_logger = logging.getLogger(__name__)


class Location(models.Model):
    _inherit = 'stock.location'

    external_stock_source = fields.Selection([
        ('odoo_database', 'Odoo Database'),
        ('manual_source', 'Manual Source')], string='External Stock Source')
    odoo_hostname = fields.Char("Hostname")
    odoo_db_name = fields.Char("Database Name")
    odoo_user = fields.Char(
        string="Username",
        help="""El usuario que se utilizará para conectar con la base de datos remota.
                Tener en cuenta que para poder obtener información de las ubicaciones listadas en el campo
                'External Locations' este usuario debe tener tildadas las compañías correspondientes""")
    odoo_password = fields.Char("Password")
    external_location_ids = fields.Char("External Locations", default="[]", help="""
        Lista de ubicaciones de la base de datos remota. Sincronizamos stock de las ubicaciones listadas e hijas de las mismas.
        """)
    last_sync = fields.Datetime('Last Sync Date')
    is_public = fields.Boolean(
        string="Publicar stock en la red",
        help="Permitir que las distintas bases de la red vean el stock de esta ubicación.")

    def _get_odoo_client(self):
        self.ensure_one()
        try:
            return Client(
                # Use JSONRPC to prevent error when server responds with None
                self.odoo_hostname.strip("/") + "/jsonrpc",
                db=self.odoo_db_name,
                user=self.odoo_user,
                password=self.odoo_password,
            )
        except Exception as e:
            raise UserError("Unable to Connect to remote database %s. Error: %s" % (self.odoo_db_name, e))

    def _cron_sync_location_stock(self):
        ''' Cron to synchronize stock of locations, we priorice locations that have never run the synchronization
            or with the oldest sync date.
        '''
        location = self.env['stock.location'].search([('external_stock_source', '=', 'odoo_database'), ('last_sync', '=', False)], limit=1)
        if not location:
            location = self.env['stock.location'].search([('external_stock_source', '=', 'odoo_database')], order='last_sync asc', limit=1)
        if location:
            location.sync_location_stock()

    def sync_location_stock(self):
        self.ensure_one()

        # Connect with external database
        remote_db = self._get_odoo_client()

        # Get products domain
        location_ids = safe_eval(self.external_location_ids)
        domain = [('location_id', 'child_of', location_ids)]
        domain += self._get_product_domain(remote_db)

        # Get quants from remote db
        quants = remote_db.env['stock.quant'].read_group(
            domain,
            fields=['product_id', 'quantity', 'reserved_quantity', 'lot_id'],
            groupby=['product_id', 'lot_id'],
            lazy=False)
        _logger.info('Updating %s products from database %s' % (len(quants), self.odoo_db_name))

        # Process quants information:
        # - Get the product default_code
        # - Map the lot_id to the lot_name
        quants_vals = {}
        for quant in quants:
            # If quantity is 0 or negative, we don't create the quant.
            if quant['quantity'] <= 0:
                continue
            # Try to get the default code from the product display name
            try:
                # TODO: imp getting default_code (query, controller in ext db, adding related in quants in ext db)
                match = re.match(r'^\[([^\[\]]*)\]', quant['product_id'][1])
                default_code = match.group(1)
            except Exception:
                _logger.debug('We could not get the default code of the product: %s', quant['product_id'][1])
                continue

            if default_code not in quants_vals:
                quants_vals[default_code] = []

            quants_vals[default_code].append({
                'quantity': quant['quantity'],
                'reserved_quantity': quant['reserved_quantity'],
                'location_id': self.id,
                'lot_name': quant['lot_id'][1] if quant['lot_id'] else False,
            })

        # Get local ids related to product's default_code
        products_default_codes = list(quants_vals.keys())
        local_product_vals = self.env['product.product'].search_read(
            [('default_code', 'in', products_default_codes)],
            ['default_code', 'id']
        )
        local_product_vals = {vals['default_code']: vals['id'] for vals in local_product_vals}

        # Remove outdated quants
        product_ids = list(local_product_vals.values())
        self.env['stock.quant'].search([('product_id', 'in', product_ids), ('location_id', '=', self.id)]).sudo().unlink()

        # Create new quants
        quant_vals_list = []
        for default_code, local_id in local_product_vals.items():
            product_quants = quants_vals[default_code]
            for quant in product_quants:
                quant['product_id'] = local_id
            quant_vals_list += product_quants
        self.env['stock.quant'].sudo().create(quant_vals_list)

        # Update last synchronization date
        self.last_sync = datetime.datetime.now()

    def _get_product_domain(self, remote_db):
        # If this is not the first synchronization,
        # update only the products that has stock move lines created after the sync date
        if self.last_sync:
            location_ids = safe_eval(self.external_location_ids)
            domain = [
                ('write_date', '>=', fields.Date.to_string(self.last_sync)),
                '|', ('location_id', 'child_of', location_ids), ('location_dest_id', 'in', location_ids)]
            products = remote_db.env['stock.move.line'].read_group(domain, ['product_id'], ['product_id'])
            product_ids = [product['product_id'][0] for product in products]
            return [('product_id', 'in', product_ids)]
        return []
