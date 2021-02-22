from odoo import models, fields, _
import requests
import logging

_logger = logging.getLogger(__name__)


class ProductImage(models.Model):
    _inherit = 'product.image'

    neored_image_url = fields.Char()
    last_syncked_neored_image_url = fields.Char(readonly=True)

    def get_image_from_neored_image_url(self):
        with requests.Session() as session:
            session.stream = True
        _logger.info('Getting neored image for %s products images', len(self))
        for rec in self.filtered('neored_image_url'):
            try:
                rec.write({
                    'image_1920': self.env['base_import.import']._import_image_by_url(
                        rec.neored_image_url, session, 'neored_image_url', 0),
                    'last_syncked_neored_image_url': rec.neored_image_url,
                })
                rec.env.cr.commit()
            except Exception as e:
                _logger.warning('No se pudo obtener la imagen, esto es lo que obtuvimos:\n %s', e)
