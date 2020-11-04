# -*- coding: utf-8 -*-
{
    'name': 'Personalizations Apromark',
    'version': '13.0.1.0.0',
    'sequence': 14,
    'summary': '',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'base', 'crm', 'contacts', 'stock', 'l10n_ar'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/crm_lead_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto-install': False,
}
