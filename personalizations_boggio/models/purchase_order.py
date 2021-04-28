from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_monto_USD = fields.Float(string="Monto en USD sin IVA", help="Se graba el monto del comprobante en dolares sin IVA (antes de 1 de mayo 2020 se grababa con IVA)", readonly=True, copy=False)
    x_carrier_id = fields.Many2one(string="Forma de envío", comodel_name="delivery.carrier", help="Rellene este campo si va a facturar el envío basado en la recolección.	", on_delete="set null")
    x_rotacion = fields.Float(string="ROTACION IR ", copy=False)
    x_stock_val = fields.Float(string="Stock Val", help="(ROT1 *STOCK_VAL1 + ROT2 +STOCK_VAL2)/( STOCK_VAL1+STOCK_VAL2)", readonly=True, copy=False)
    x_rotacion_local = fields.Float(string="ROTACION IR Local", help="Indice de rotacion local", copy=False)
    x_stock_val_local = fields.Float(string="Stock Val Local", readonly=True, copy=False)
