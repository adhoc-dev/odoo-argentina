# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class StockController(http.Controller):

    @http.route(['/stock'], type='json', auth='none', methods=['GET'])
    def get_product_stock_by_location(self):
        token = request.params.get('token')
        server_token = request.env["ir.config_parameter"].sudo().get_param("personalizations_provar.stock_token_server")
        if token != server_token:
            return {'error': "Invalid token"}
        default_code = request.params.get('default_code')
        product_id = request.env['product.product'].sudo().search([('default_code', '=', default_code)], limit=1).id
        if not product_id:
            return {'error': "No se encontró el producto con código %s en Catálogo Neored" % default_code}
        quants = request.env['stock.quant'].sudo().read_group(
            domain=[('product_id', '=', product_id)],
            fields=['location_id', 'quantity', 'reserved_quantity'],
            groupby=['location_id', 'lot_name'],
            lazy=False,
        )
        res = []
        for quant in quants:
            _, location_name = quant['location_id']
            res.append({
                'location_name': location_name,
                'on_hand': quant['quantity'],
                'reserved': quant['reserved_quantity'],
                'available': quant['quantity'] - quant['reserved_quantity'],
                'lot_name': quant['lot_name'],
            })
        return res
