from odoo import fields, models

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    inv_ref = fields.Many2one('account.move',  domain="[('partner_id', '=', vendor_id), ('state', '=', 'posted')]")
