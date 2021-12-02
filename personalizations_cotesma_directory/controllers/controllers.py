
from odoo import http


class TelephoneDirectory(http.Controller):

    @http.route(['/guia',
                '/guia/page/<int:page>'],
                type='http', auth='public', website=True, csrf=True)
    def directory_telephone_post(self, page=0, search='', **post):
        self.directory = http.request.env['directory.telephone']
        phone_for_page = self.directory.PHONE_FOR_PAGE
        page = page or 1
        total = 0
        model_ids = []
        list_ids = []

        if search:
            post['search'] = search
            model_ids, list_ids = self.directory._search_with_parameters(
                search, page)
            total = list_ids

        pager = http.request.website.pager(
            url='/guia',
            total=total,
            page=page,
            step=phone_for_page,
            url_args=post
        )

        return http.request.render('personalizations_cotesma_directory.telephone_page_template',
                                   {'telephones': model_ids or [],
                                    'pager': pager})
