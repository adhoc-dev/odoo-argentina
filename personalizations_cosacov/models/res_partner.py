from odoo import api, models, _
class Partner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id.product_pricelist:
            return {'warning': {
                'title':"Aviso",
                'message':_('Para %(state)s se sugiere la tarifa: \'%(tarifa)s\'') % {
                    'state': self.state_id.display_name,
                    'tarifa': self.state_id.product_pricelist.display_name
                }
            }}
