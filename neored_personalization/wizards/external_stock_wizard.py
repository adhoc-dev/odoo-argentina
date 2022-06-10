from jinja2 import Undefined
from odoo import fields, models, api
from odoo.exceptions import UserError
from werkzeug import urls
import requests
import json

PROVAR_BASE_URL = 'https://provar.adhoc.ar/'


class ExternalStockWizard(models.TransientModel):
    _name = 'external.stock.wizard'
    _description = 'External stock show by locations'

    @api.model
    def _default_lines(self):
        product = self.env['product.template'].browse(self._context.get('product_id'))
        token = self.env["ir.config_parameter"].sudo().get_param("neored_personalization.stock_token_client")
        url = PROVAR_BASE_URL + 'stock'
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({
            "params": {
                "default_code": product.default_code,
                "token": token,
            }
        })
        try:
            req = requests.request("GET", url, headers=headers, data=data)
            req.raise_for_status()
            lines = req.json()['result']
        except requests.HTTPError as e:
            raise UserError(e)
        if 'error' in lines:
            raise UserError(lines['error'])
        else:
            lines_ids = []
            locations = {line['location_name'] for line in lines}
            for loc in locations:
                line = {
                    'location_name': loc,
                    'on_hand': 0,
                    'reserved': 0,
                    'available': 0,
                    'lot_count': 0,
                    'lot_lines_ids': [],
                }
                for lot_line in filter(lambda l: l['location_name'] == loc, lines):
                    line['on_hand'] += lot_line['on_hand']
                    line['reserved'] += lot_line['reserved']
                    line['available'] += lot_line['available']
                    if lot_line['lot_name']:
                        line['lot_count'] += 1
                        line['lot_lines_ids'].append((0, 0, {
                            'on_hand': lot_line['on_hand'],
                            'reserved': lot_line['reserved'],
                            'available': lot_line['available'],
                            'lot_name': lot_line['lot_name'],
                        }))
                lines_ids.append((0, 0, line))
            return lines_ids

    line_ids = fields.One2many('external.stock.wizard.line', 'wizard_id', string='Lines', readonly=True, default=_default_lines)


class ExternalStockWizardLine(models.TransientModel):
    _name = 'external.stock.wizard.line'
    _description = 'External stock lines'

    wizard_id = fields.Many2one('external.stock.wizard', string='Wizard', readonly=True)
    location_name = fields.Char(string='Location', readonly=True)
    on_hand = fields.Integer(string='On Hand Quantity', readonly=True)
    reserved = fields.Integer(string='Reserved Quantity', readonly=True)
    available = fields.Integer(string='Available Quantity', readonly=True)
    lot_count = fields.Integer(string='Lots', readonly=True)
    lot_lines_ids = fields.One2many('external.stock.wizard.lot.line', 'location_line_id', string='Lot Lines', readonly=True)


class ExternalStockWizardLotLine(models.TransientModel):
    _name = 'external.stock.wizard.lot.line'
    _description = 'External stock lot lines'

    location_line_id = fields.Many2one('external.stock.wizard.line', string='Location Line', readonly=True)
    on_hand = fields.Integer(string='On Hand Quantity', readonly=True)
    reserved = fields.Integer(string='Reserved Quantity', readonly=True)
    available = fields.Integer(string='Available Quantity', readonly=True)
    lot_name = fields.Char(string='Lot Name', readonly=True)
