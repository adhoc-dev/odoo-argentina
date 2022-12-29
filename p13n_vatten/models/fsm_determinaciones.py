# -*- coding: utf-8 -*-
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class Determinaciones(models.Model):
    _description = 'Determinaciones'
    _name = 'fsm_determinaciones'

    order_id = fields.Many2one(comodel_name='worksheet_control_analitico_agua', ondelete='cascade')
    muestra_name = fields.Char(string='Muestra')
    parametro_name = fields.Char(string='Parámetro')
    unit_name = fields.Char(string='Unidad')
    parametro_display = fields.Char(string='Parámetro+Unidad')
    valor = fields.Char(string='Valor', default=None)
    min_value = fields.Char(string='Mínimo')
    max_value = fields.Char(string='Máximo')
    in_report = fields.Boolean(string='Se reporta')
    in_chart = fields.Boolean(string='Se grafica')
