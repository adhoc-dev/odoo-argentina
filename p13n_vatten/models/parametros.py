from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class Parametros(models.Model):
    _description = 'Parametros'
    _name = 'parametros'
    _order = "sequence,id"

    sequence = fields.Integer(string='Secuencia')
    muestra_id = fields.Many2one(comodel_name='muestras', ondelete='cascade')
    chemical_parameter_id = fields.Many2one(comodel_name='chemical.parameter', required=True)
    name = fields.Char(string='Parámetro', related="chemical_parameter_id.name")
    unit = fields.Char(string='Unidad', readonly=False, store=True, related="chemical_parameter_id.unit")
    min_value = fields.Char(string='Mínimo')
    max_value = fields.Char(string='Máximo')
    in_report = fields.Boolean(string='Se reporta', default=True)
    in_chart = fields.Boolean(string='Se grafica')
