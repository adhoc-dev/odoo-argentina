import logging
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)


class ShopifyController(http.Controller):

    @http.route(['/shopify/update'], type='json', methods=['GET'], auth='public')
    def test_shopify(self, **kwargs):
        context = {
            'pricelist': kwargs['pricelist'],
            'location': kwargs['location'],
            'taxes_included': True,
        }
        products = request.env['product.product'].sudo().with_context(context).search([('barcode', '!=', False)])
        product_fields = ["barcode", "qty_available", "price"]
        res = products.read(product_fields)
        _logger.info('Shopify: updating %s products', len(res))
        return res