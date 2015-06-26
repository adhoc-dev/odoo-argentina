# -*- coding: utf-8 -*-
{
    'name': 'Tax Settlement',
    'version': '1.0',
    'category': 'Argentinian Localization',
    'sequence': 14,
    'summary': '',
    'description': """
Tax Settlement
==============
    """,
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'images': [
    ],
    'depends': [
        'l10n_ar_invoice',
    ],
    'data': [
        'views/account_tax_settlement_view.xml',
        'views/account_tax_settlement_detail_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        # No podemos usar estos datos demo porque este modulo no depende del chart of account
        # 'demo/demo_data.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
