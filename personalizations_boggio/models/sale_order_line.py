from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_location_id = fields.Many2one(string="Ubicación", related="product_id.location_id", on_delete="set null", readonly=True, copy=False)
    x_qty_available = fields.Float(string="Stock en Mano", related="product_id.qty_available", help="Current quantity of products."
"In a context with a single Stock Location, this includes goods stored at this Location, or any of its children."
"In a context with a single Warehouse, this includes goods stored in the Stock Location of this Warehouse, or any of its children."
"stored in the Stock Location of the Warehouse of this Shop, or any of its children."
"Otherwise, this includes goods stored in any Stock Location with 'internal' type.", readonly=True, copy=False)
    x_virtual_available = fields.Float(string="Stock Virtual", related="product_id.virtual_available", help="Forecast quantity (computed as Quantity On Hand - Outgoing + Incoming)"
"In a context with a single Stock Location, this includes goods stored in this location, or any of its children."
"In a context with a single Warehouse, this includes goods stored in the Stock Location of this Warehouse, or any of its children."
"Otherwise, this includes goods stored in any Stock Location with 'internal' type.", readonly=True, copy=False)
    x_active = fields.Boolean(string="Active", related="product_id.active", help="If unchecked, it will allow you to hide the product without removing it.", track_visibility="onchange", readonly=True, copy=False)



    @api.onchange('name')
    def change_name(self):
        line = self.new({'product_id': self.product_id.id})
        line.product_id_change()
        name = line.name
        if self.name and name and self.name.find(name) == -1:
            self.name = self._origin.name
            return {'warning': {
                    'title': '¡Cuidado!',
                    'message': 'No puede cambiar la descripcion sino esta prestente este valor original: \n "%s"' % name,
                    }}
