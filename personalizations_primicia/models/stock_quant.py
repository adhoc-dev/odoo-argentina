from odoo import fields, models

class QuantPackage(models.Model):
    _inherit = "stock.quant.package"

    def get_picking(self):
        domain = ['|', ('result_package_id', 'in', self.ids), ('package_id', 'in', self.ids)]
        pickings = self.env['stock.move.line'].search(domain).mapped('picking_id').filtered(lambda p: p.picking_type_id.code == 'outgoing')
        return pickings
