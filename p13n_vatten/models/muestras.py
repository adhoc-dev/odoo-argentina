
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class Muestras(models.Model):
    _description = 'Muestras X'
    _name = 'muestras'
    _order = "sequence,id"

    sequence = fields.Integer(string='Secuencia')
    sample_type = fields.Selection(string='Tipo de Muestra', selection=[('Agua', 'Agua'),('Efluente', 'Efluente')], default='Agua')
    name = fields.Char(string='Punto de Muestreo', required='false', help='Asigne un nombre al punto de muestreo.')
    partner_service_id = fields.Many2one(comodel_name='res.partner', string='Dirección de Servicio', required="true", ondelete='cascade', help="Dirección donde se prestará el servicio.")
    parametro_ids = fields.One2many(comodel_name='parametros', inverse_name='muestra_id', string="Parámetros", copy=True)

    @api.model
    def default_get(self, fields):
        res = super(Muestras, self).default_get(fields)

        recs = self.env['chemical.parameter'].search([('sample_type', '=', 'Agua')], limit=11)

        r=[]
        for rec in recs:
            r.append((0, 0, {'name': rec.id, 'unit': rec.unit, 'in_report': True}))
        res["parametro_ids"] = r

        return res