from odoo import models, fields


class XControlesRemitosDiarios(models.Model):
    _name = 'x_controles_remitos_diarios'
    _description = 'Controles de remitos diarios'

    x_fecha = fields.Date(string="Fecha", required=True, copy=False)
    x_team_id = fields.Many2one(string="Equipo de ventas", comodel_name="crm.team", on_delete="set null", required=True, copy=False)
    x_num_control = fields.Integer(string="Numero pedidos controlados", required=True, copy=False)
    x_num_desvio = fields.Integer(string="Numero Pedidos con Desvios", required=True, copy=False)
    x_porc_correctos = fields.Float(string="Porcentaje de remitos correctos", compute="_compute_x_porc_correctos", readonly=True, copy=False)
    x_write_uid2 = fields.Many2one(string="Preparador real", comodel_name="res.users", help="Usuario real que preparo el pedido	", on_delete="set null")

    def _compute_x_porc_correctos(self):
        for record in self:
            record['x_porc_correctos'] = 100 - (record.x_num_control>0 and 100*float(record.x_num_desvio)/float(record.x_num_control) or 0)
