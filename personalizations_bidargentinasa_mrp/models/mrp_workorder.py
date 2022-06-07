# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    wh_production_done = fields.Selection('Material Entregado', readonly=True, store=True,
                                          related='production_id.wh_production_done')
