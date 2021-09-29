from odoo import models, fields, SUPERUSER_ID


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    x_origen = fields.Many2one(string="Origen de inventario", comodel_name="x_origen_tags", help="En que capa surgió el problema de inventario? (cliente, interno, auditoria o proveedor)")

    def action_validate(self):
        # hacemos esto para evitar derle el permiso de manager de inventario para poder validar un ajuste de inventario
        if not self.user_has_groups('stock.group_stock_manager') and self.user_has_groups('personalizations_boggio.stock_validar_inventario'):
            previus_user = self.env.user
            self = self.with_user(SUPERUSER_ID)
            res = super().action_validate()
            self.with_user(previus_user.id).write({'state': self.state})
            return res
        return super().action_validate()
