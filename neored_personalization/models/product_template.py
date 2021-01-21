from odoo import models, fields, _
from odoo.exceptions import ValidationError
import requests
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_abstract_id = fields.Many2one('product.abstract',)
    comparable_product_ids = fields.Many2many(
        'product.template', domain="[('id', '!=', id)]",
        compute='_compute_comparable_products', inverse='_inverse_comparable_products')
    # agregaro para almacenar facilmente url de las imagenes y que luego podamos definir
    # si usamos el modulo de las urls o no
    neored_image_url = fields.Char()
    last_syncked_neored_image_url = fields.Char(readonly=True)
    hs_code = fields.Char(string="Electrobase")
    company_id = fields.Many2one(default=False)

    def get_image_from_neored_image_url(self):
        with requests.Session() as session:
            session.stream = True
        _logger.info('Getting neored image for %s products', len(self))
        for rec in self.filtered('neored_image_url'):
            try:
                rec.write({
                    'image': self.env['base_import.import']._import_image_by_url(
                        rec.neored_image_url, session, 'neored_image_url', 0),
                    'last_syncked_neored_image_url': rec.neored_image_url,
                })
                rec.env.cr.commit()
            except Exception as e:
                _logger.warning('No se pudo obtener la imagen, esto es lo que obtuvimos:\n %s', e)

    #  al final fuimos por otro camino porque si no tendriamos que meter logica de external id de odumbo y demas
    # en este script que empezamos Impuestos de productos (TODAVIA NO TERMINADO)
    # vamos a probar sincronizar con id de impuesto y bloquear edición de los mismos, si no otra alternativa es
    # crear campo comptutado con inverso, pero puede ser poco performante
    # def set_vat_aliquot(self, tax_group_extid, tax_type):
    #     for company in self.env['res.company'].search([]):
    #         # map between tax type and pt tax field
    #         tax_field = {'sale': 'taxes_id', 'purchase': 'supplier_taxes_id'}.get(tax_type)
    #         tax_group = self.env.ref(tax_group_extid)
    #         base_domain = [('company_id', '', company.id), ('type', '=', tax_type)]
    #         tax = self.env['account.tax'].search(base_domain + [('tax_group_id', '=', tax_group)], limit=1)
    #         if not tax:
    #             raise ValidationError(_(
    #                 'No encontramos un impuesto tipo %s para tax group id %s'), (tax_type, tax_group))
    #         other_vats = self.env['account.tax'].search(
    #             base_domain + [
    #                 ('tax_group_id.tax', '=', 'vat'), ('tax_group_id.tax', '=', 'vat'), ('type', '=', 'tax')]
    #             ) - tax
    #         to_remove = [(3, tax.id, 0) for tax in other_vats]
    #         self.write({tax_field: to_remove + [(4, tax.id, 0)]})

    def _compute_comparable_products(self):
        for rec in self:
            rec.comparable_product_ids = rec.product_abstract_id.product_tmpl_ids - rec

    def _inverse_comparable_products(self):
        for rec in self:
            # productos que se sacaron de la lista
            (rec.product_abstract_id.product_tmpl_ids - rec.comparable_product_ids - rec).write({'product_abstract_id': False})

            # productos nuevos a la lista
            product_abstract = rec.comparable_product_ids.mapped('product_abstract_id')
            # si se desvincularon todos los productos borramos el product abstract
            if not rec.comparable_product_ids and rec.product_abstract_id:
                rec.product_abstract_id.unlink()
            # para no favorecer errores, si eligieron más de un produc abstract damos error
            elif len(product_abstract - rec.product_abstract_id) > 1:
                raise ValidationError('Ha seleccionado productos que pertenecen a varios grupos de productos distintos')
            # si eligieron productos de otro product abstract los fusionamos
            elif rec.product_abstract_id and product_abstract and rec.product_abstract_id != product_abstract:
                related_prod_to_merge = rec.comparable_product_ids.mapped('product_abstract_id.product_tmpl_ids')
                (rec.comparable_product_ids + related_prod_to_merge).write(
                    {'product_abstract_id': rec.product_abstract_id.id})
                (product_abstract - rec.product_abstract_id).unlink()
            # esta condicion se podria fusionar con la anterior pero la dejamos separada por si quieren agregar un
            # raise en la anterior
            elif rec.product_abstract_id:
                rec.comparable_product_ids.write({'product_abstract_id': rec.product_abstract_id.id})
            elif product_abstract:
                rec.product_abstract_id = product_abstract.id
            # no product abstract yet
            else:
                product_abstract = product_abstract.create({})
                (rec + rec.comparable_product_ids).write({'product_abstract_id': product_abstract.id})

    def _check_uom(self):
        if self._context.get('odumbo_sync'):
            _logger.info('Check uom disabled on odumbo_sync')
            return True
        else:
            return super()._check_uom()
