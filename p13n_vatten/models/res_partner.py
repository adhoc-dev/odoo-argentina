# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('service', 'Dirección de servicio')])
    muestra_ids = fields.One2many(comodel_name='muestras', inverse_name='partner_service_id', string="Puntos de Muestreo")
