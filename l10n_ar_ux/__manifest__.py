{
    'name': 'Argentinian Accounting UX',
    'version': "13.0.1.0.0",
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'l10n_ar', 'base_ux',
    ],
    'data': [
        'data/res_currency_data.xml',
        'data/account_account_tag_data.xml',
        'data/account_tax_group_data.xml',
        'views/portal_templates.xml',
        'views/account_move_view.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
