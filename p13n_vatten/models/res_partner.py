# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('payment', 'Dirección de pago'), ('service', 'Dirección de servicio')])
    muestra_ids = fields.One2many(comodel_name='muestras', inverse_name='partner_service_id', string="Puntos de Muestreo")
    has_service_contact_child = fields.Boolean(compute='_compute_has_service_contact_child',help='Technical field for use in views', store=True)

    @api.depends('child_ids.type')
    def _compute_has_service_contact_child(self):
        datas = self.read_group([('parent_id','in',self.ids),('type','=','service')],['parent_id'],groupby=['parent_id'])
        parent_ids = {data['parent_id'][0] for data in datas}
#        with_service_c_recs = self.browse(parent_ids, prefetch=self._prefetch)
        with_service_c_recs = self.browse(parent_ids)
        with_service_c_recs.update({'has_service_contact_child': True})
        without_service_c_recs = self - with_service_c_recs
        without_service_c_recs.update({'has_service_contact_child': False})

# TODO terminar de borrar, no aportaria valor o no es la forma correcta de hacerlo llegado el caso
#     def name_get(self):
#         res = []
#         for record in self:
# #            print(record)
# #            if self.env.context.get('laboratory', False):
# #               print('>>> CON CONTEXTO')
# #                res.append((record.id, ("%(partner_name)s") % {'partner_name': record.name}))
# #            else:
# #                print('>>> SIN CONTEXTO')
# #                res.append((record.id, ("%(partner_name)s") % {'partner_name': record.name}))
# #            print('1>>> >>> : ', record.name)
# #            print('2>>> >>> : ', record.display_name)
# #            res.append((record.id, "popin"))
#             res.append((record.id, record.name))
#         return res
