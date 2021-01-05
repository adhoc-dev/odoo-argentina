from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    def checkout_form_validate(self, mode, all_form_values, data):
        all_form_values['field_required'] = all_form_values['field_required'].replace('phone', 'mobile')
        return super().checkout_form_validate(mode, all_form_values, data)

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        response = super(WebsiteSale, self).address(**kw)
        if 'partner_id' in kw.keys():
            partner = request.website.sale_get_order().partner_id
            if partner:
                response.qcontext.update({'birthdate': partner.birthdate,
                                          'highschool_complete':
                                          partner.highschool_complete})
        return response

    def values_postprocess(self, order, mode, values, errors, error_msg, **kw):
        new_values, errors, error_msg = super(WebsiteSale, self).values_postprocess(order,
                                                                                    mode, values,
                                                                                    errors, error_msg)
        new_values['mobile'] = values.get('mobile')
        new_values['birthdate'] = values.get('birthdate')
        new_values['highschool_complete'] = True if values.get('highschool_complete') == 'on' else False
        return new_values, errors, error_msg
