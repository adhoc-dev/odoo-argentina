# -*- coding: utf-8 -*-

import logging
import werkzeug
from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
import stdnum.exceptions
import stdnum.ar

_logger = logging.getLogger(__name__)


class AuthSignupHome(AuthSignupHome):
    def do_signup(self, qcontext):
        # Values: valores que vamos a pasar en el método _signup_with_values para crear el usuario.
        # Tienen que ser campos existentes en res.partner/res.users
        # Por las dudas los campos que agreguemos en el xml, deberían tener el mismo nombre que el campo en el modelo
        # Por ejemplo: para el campo 'vat', le tengo que poner el mismo nombre al input asociado
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'phone', 'l10n_ar_afip_responsibility_type_id',
                                                     'vat')}
        values['l10n_latam_identification_type_id'] = int(qcontext.get('l10n_latam_identification_type_id'))
        qcontext['l10n_ar_afip_code'] = request.env['l10n_latam.identification.type'].sudo().browse(int(qcontext['l10n_latam_identification_type_id'])).l10n_ar_afip_code
        responsability_type = request.env['l10n_ar.afip.responsibility.type'].sudo().browse(int(qcontext['l10n_ar_afip_responsibility_type_id']))
        # Verifico que:
        #  *si elige DNI que haya seleccionado tipo de responsabilidad Consumidor Final
        #  *si elige CUIT que no haya seleccionado Consumidor Final
        if qcontext['l10n_ar_afip_code'] == '96' and responsability_type.code == '5': #DNI
            values['property_product_pricelist'] = int(request.env['ir.config_parameter'].sudo().get_param(
            'personalizations_grupomicro.signup_person_pricelist_id'))
            values['is_company'] = False
        elif qcontext['l10n_ar_afip_code'] == '80' and responsability_type.code != '5': #CUIT
            values['property_product_pricelist'] = int(request.env['ir.config_parameter'].sudo().get_param(
            'personalizations_grupomicro.signup_company_pricelist_id'))
            values['is_company'] = True
        else:
            raise UserError(_("Error, usted seleccionó %s y puso tipo de responsabilidad %s" %(request.env['l10n_latam.identification.type'].sudo().browse(int(qcontext['l10n_latam_identification_type_id'])).name, responsability_type.name)))
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()


    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        vals = super().web_auth_signup(*args, **kw)
        vals.qcontext['responsabilities'] = request.env['l10n_ar.afip.responsibility.type'].sudo().search([('code','!=','99')])
        vals.qcontext['identifications'] = request.env['l10n_latam.identification.type'].sudo().search([('l10n_ar_afip_code','in',[80,96])])
        # Dejo este condicional porque siempre va a aparecer un error si está mal ingresado el CUIT o DNI, 
        # lo único que no especifica el error. Por eso acá lo que busco es capturar que tipo de error es
        if 'error' in vals.qcontext:
            try:
                identification_type = request.env['l10n_latam.identification.type'].sudo().browse(int(vals.qcontext['l10n_latam_identification_type_id']))
                module = stdnum.ar.dni if identification_type.l10n_ar_afip_code == '96' else stdnum.ar.cuit
                module.validate(vals.qcontext['vat'])
            except module.InvalidChecksum:
                vals.qcontext['error'] = _('The validation digit is not valid for "%s"') % identification_type.name
            except module.InvalidLength:
                vals.qcontext['error'] = _('Invalid length for "%s"') % identification_type.name
            except module.InvalidFormat:
                vals.qcontext['error'] = _('Only numbers allowed for "%s"') % identification_type.name
            except Exception as error:
                 raise ValidationError(repr(error))
        return vals

