{
    'name': 'Personalizations Apromark',
    'version': "15.0.1.0.0",
    'sequence': 14,
    'summary': '',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'crm',
        'sale',
        'website_sale',
        'l10n_ar',
        'sale_subscription',
        'account_payment_group',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/account_payment_group_view.xml',
        'views/templates.xml',
        'views/crm_lead_views.xml',
        'views/sale_subscription.xml',
        'data/base_automation.xml',
    ],
    'application': False,
    'installable': True,
    'auto-install': False,
}
