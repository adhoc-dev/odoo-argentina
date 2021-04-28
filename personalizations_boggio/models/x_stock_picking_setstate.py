from odoo import models, fields


class XStockPickingSetstate(models.Model):
    _name = 'x_stock.picking.setstate'
    _description = 'Seteo de estados de remitos'

    x_name = fields.Char(string="Name", copy=False)
    x_voucher_ids = fields.Many2many(string="Remitos", comodel_name="stock.picking.voucher", relation="x_stock_picking_voucher_x_stock_picking_setstate_rel", column1="x_stock_picking_setstate_id", column2="stock_picking_voucher_id")
    x_barcode_scanned = fields.Char(string="Barcode Scanned", help="Value of the last barcode scanned.")
    x_state = fields.Many2one(string="Estado", comodel_name="stock.picking.state_detail", on_delete="set null", readonly=True)
