# -*- coding: utf-8 -*-
from odoo import models, fields

import logging
_logger = logging.getLogger(__name__)


class ChemicalParameter(models.Model):
    _name = 'chemical.parameter'
    _description = 'Chemical Parameter'
    _order = "sequence,id"

    sequence = fields.Integer(string='Secuencia')
    name = fields.Char(string='Parámetro', required=True)
    unit = fields.Char(string='Unidad', required=True)
    description = fields.Char(string='Descripción', required=False)
    method = fields.Char(string='Método', required=False)
    sample_type = fields.Selection(selection=[('Agua', 'Agua'),('Efluente', 'Efluente')],
                                    default='Agua',
                                    required=True,
                                    string='Tipo de muestra',
                                    help='Ingrese el tipo de muestra')
