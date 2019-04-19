from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # probamos llevarlos como campos calculados y si dicen algo los pasamoas a metodo
    cuit = fields.Char(
        compute='_compute_cuit',
    )
    formated_cuit = fields.Char(
        compute='_compute_formated_cuit',
    )
    # renombrado y se computa y setee a VAT (no haria falta store)
    main_id_number = fields.Char(
        compute='_compute_main_id_number',
        inverse='_inverse_main_id_number',
        store=True,
        string='Main Identification Number',
    )
    main_id_category_id = fields.Many2one(
        string="Main Identification Category",
        comodel_name='res.partner.id_category',
        index=True,
        auto_join=True,
    )

    @api.multi
    def cuit_required(self):
        self.ensure_one()
        if not self.cuit:
            raise UserError(_('No CUIT configured for partner [%i] %s') % (
                self.id, self.name))
        return self.cuit

    @api.multi
    @api.depends(
        'cuit',
    )
    def _compute_formated_cuit(self):
        for rec in self:
            if not rec.cuit:
                continue
            cuit = rec.cuit
            rec.formated_cuit = "{0}-{1}-{2}".format(
                cuit[0:2], cuit[2:10], cuit[10:])

    # llevar a res.country estos campos desde l10n_ar_account
    # cuit_fisica = fields..
    # cuit_fisica = fields

    @api.multi
    @api.depends(
        'id_numbers.category_id.afip_code',
        'id_numbers.name',
        'main_id_number',
        'main_id_category_id',
    )
    def _compute_cuit(self):
        for rec in self:
            # el cuit solo lo devolvemos si es el doc principal
            # para que no sea engañoso si no tienen activado multiples doc
            # y esta seleccionado otro que no es cuit
            # igualmente, si es un partner del extranjero intentamos devolver
            # cuit fisica o juridica del pais
            if rec.main_id_category_id.afip_code != 80:
                country = rec.country_id
                if country and country.code != 'AR':
                    if rec.is_company:
                        rec.cuit = country.cuit_juridica
                    else:
                        rec.cuit = country.cuit_fisica
                continue
            cuit = rec.id_numbers.search([
                ('partner_id', '=', rec.id),
                ('category_id.afip_code', '=', 80),
            ], limit=1)
            # agregamos esto para el caso donde el registro todavia no se creo
            # queremos el cuit para que aparezca el boton de refrescar de afip
            if not cuit:
                rec.cuit = rec.main_id_number
            else:
                rec.cuit = cuit.name

    @api.multi
    @api.depends(
        'main_id_category_id',
        'id_numbers.category_id',
        'id_numbers.name',
    )
    def _compute_main_id_number(self):
        for partner in self:
            id_numbers = partner.id_numbers.filtered(
                lambda x: x.category_id == partner.main_id_category_id)
            if id_numbers:
                partner.main_id_number = id_numbers[0].name

    @api.multi
    def _inverse_main_id_number(self):
        to_unlink = self.env['res.partner.id_number']
        # we use sudo because user may have CRUD rights on partner
        # but no to partner id model because partner id module
        # only adds CRUD to "Manage contacts" group
        for partner in self:
            name = partner.main_id_number
            category_id = partner.main_id_category_id
            if category_id:
                partner_id_numbers = partner.id_numbers.filtered(
                    lambda d: d.category_id == category_id).sudo()
                if partner_id_numbers and name:
                    partner_id_numbers[0].name = name
                elif partner_id_numbers and not name:
                    to_unlink |= partner_id_numbers[0]
                # we only create new record if name has a value
                elif name:
                    partner_id_numbers.create({
                        'partner_id': partner.id,
                        'category_id': category_id.id,
                        'name': name
                    })
        to_unlink.unlink()

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        we search by id, if we found we return this results, else we do
        default search
        """
        if not args:
            args = []
        # solo para estos operadores para no romper cuando se usa, por ej,
        # no contiene algo del nombre
        if name and operator in ('ilike', 'like', '=', '=like', '=ilike'):
            recs = self.search(
                [('id_numbers.name', operator, name)] + args, limit=limit)
            if recs:
                return recs.name_get()
        return super(ResPartner, self).name_search(
            name, args=args, operator=operator, limit=limit)
