# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http, fields
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class ShopifyController(http.Controller):

    @http.route(['/shopify/update'], type='json', methods=['GET'], auth='public')
    def update_shopify(self, **kwargs):
        context = {
            'pricelist': kwargs['pricelist'],
            'location': kwargs['location'],
            'taxes_included': True,
        }
        products = request.env['product.product'].sudo().with_context(context).search([('barcode', '!=', False)])
        res = []
        for product in products:
            res.append({
                'barcode': product.barcode,
                'qty_available': product.qty_available,
                'price': product.price,
                'tag': ', '.join(product.tag_ids.mapped('name')),
                'length': product.product_length,
                'height': product.product_height,
                'width': product.product_width,
                'weight': product.weight,
            })
        _logger.info('Shopify: updating %s products', len(res))
        return res


class OdooAPI(http.Controller):

    def error_response(self, msg, status=200):
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": status,
                "message": msg,
            }
        }

    # TODO WIP review if needed csrf=False
    @http.route('/api/<string:api_key>/<string:endpoint>', type="json", auth="public", methods=["GET", "POST"])
    def call_model_function(self, api_key, endpoint, **post):

        # Review valid API KEY
        ICP = http.request.env['ir.config_parameter'].sudo().get_param
        system_api_key = ICP('personalizations_sba.rest_api_key', '')
        if api_key != system_api_key:
            return self.error_response('Is not a valid API KEY', status=400)

        available_endpoints = ['get_new_contacts', 'update_contact', 'get_validated_invoices', 'create_contact']
        if endpoint not in available_endpoints:
            return self.error_response('Not valid endpoint', status=400)

        body = http.request.jsonrequest
        result = getattr(self, endpoint)(body)
        return result

    def get_new_contacts(self, args):
        """ Consultar la información de los contactos en Odoo, en este momento lee la info de los contactos en Odoo
        y devuelve todos los campos.

        Ejemplo del body a enviar al request:
             puede ser sin body
             con un body como este {"from_date": "2021-06-06 00:00:00"}
        """
        domain = []

        # If a given date then only return the partners updated/created after that date
        from_date = args.get('from_date')
        if from_date:
            from_date = fields.Datetime.from_string(from_date)
            domain += [('create_date', '>=', from_date)]
        read_fields = [
            'name', 'vat', 'l10n_ar_afip_responsibility_type_id', 'l10n_latam_identification_type_id',
            'mobile', 'phone', 'email',
            # 'contact_address_complete',
            'street', 'street2', 'state_id', 'country_id',
            'is_company', 'parent_id',

            # Nuevos campos solicitados via ticket 40583 el 22/12/2021
            'user_id', 'credit_limit', 'zip', 'city', 'commercial_partner_id',
            'create_uid', 'create_date', 'partner_state', 'x_studio_field_HZyaK',
            'x_studio_field_PCg5t', 'nbr_open_invoices', 'category_id',
        ]
        partners = http.request.env['res.partner'].sudo().search(domain).read(read_fields)
        return {'count': len(partners), 'partners': partners}

    def update_contact(self, args):
        """ Escribir y actualizar los datos de un contacto desde Sales Force
        Example: body {"values": {"ref": "hola prueba"}, "partner_id": 5}
        """
        partner_id = args.get('partner_id', False)
        values = args.get('values', {})
        if not partner_id or not values:
            return {'msg': 'Nothing was done, need to send partner_id and values keys in the body of the request'}
        return {
            'updated_id': partner_id,
            'write': http.request.env['res.partner'].sudo().browse(partner_id).write(values),
        }

    def create_contact(self, args):
        """ Crea un contacto con los valores dados en los argumentos. Si envian un campo no valido le mostramos mensaje
        de error del Odoo indicando el error.

        Example: body {"values": {"ref": "referencia contacto", "name": "nombre contacto"}, ... } """
        values = args.get('values', {})
        if not values:
            return {'msg': 'Nothing was done, need to send values keys in the body of the request'}

        status = 'SUCCESS'
        partner = False
        try:
            partner = http.request.env['res.partner'].sudo().create(values)
        except Exception as exp:
            status = 'ERROR: %s' % repr(exp)

        return {
            'partner_id': partner and partner.id,
            'status': status,
        }

    def get_validated_invoices(self, args):
        """ obtiene las factura validadas, devuelve:
        * id de cliente
        * id de factura
        * numero factura
        * el detalle de las lineas
        tanto del account.invoice y account.invoice.line.
        """
        domain = [('type', 'in', ['out_invoice', 'out_refund']), ('state', '=', 'posted')]

        # If a given date then only return the partners updated/created after that date
        from_date = args.get('from_date')
        if from_date:
            from_date = fields.Datetime.from_string(from_date)
            domain += ['|', ('create_date', '>=', from_date), ('write_date', '>=', from_date)]

        partner_id = args.get('partner_id')
        if partner_id:
            domain += [('partner_id', '=', partner_id)]

        inv_obj = http.request.env['account.move'].sudo()
        read_fields = [
            'name', 'partner_id', 'name', 'line_ids', 'company_id', 'invoice_date', 'ref', 'internal_notes',
            "l10n_ar_afip_auth_mode", "l10n_ar_afip_auth_code"]
        invoices = inv_obj.search(domain).read(read_fields)

        read_fields = [
            'name', 'quantity', 'price_unit', 'discount', 'price_total', 'product_id', 'tax_ids',
            'x_isbn', 'analytic_account_id'
        ]

        for inv in invoices:
            inv.update({'line_ids': inv_obj.browse(inv.get('id')).line_ids.read(read_fields)})
        return {'count': len(invoices), 'invoices': invoices}
