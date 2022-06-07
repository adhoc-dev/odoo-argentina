# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # This is to avoid this Errors:
    #  - "Non-stored field mrp.production.picking_ids cannot be searched."
    #  - "inconsistent 'compute_sudo' for computed fields: delivery_count, picking_ids."
    picking_ids = fields.Many2many(store=True, compute_sudo=False)
    wh_production_done = fields.Selection([('done', 'Material Entregado'), ('draft', 'Material No Entregado')], "Material Entregado", compute='_compute_wh_production_done',
                                        readonly=True, store=True, tracking=True)

    @api.depends('picking_ids.state', 'move_raw_ids.state')
    def _compute_wh_production_done(self):
        for production in self.filtered(lambda x: x.state not in ('done', 'cancel')):
            production.wh_production_done = 'draft'
            picking_src = production.picking_ids.filtered(lambda x: x.location_dest_id == production.location_src_id)
            if picking_src and all(move.state == 'done' for move in picking_src):
                production.wh_production_done = 'done'
            elif all(move.state == 'done' for move in production.move_raw_ids):
                production.wh_production_done = 'done'

    def action_confirm(self):
        ctx = self._context
        if not ctx.get('not_confirm_pr', False):
            super().action_confirm()
        return True
