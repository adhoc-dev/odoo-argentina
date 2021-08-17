{
    'name': 'Personalizations Apromark',
    'version': '13.0.1.12.0',
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
        'account_analytic_default',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/account_payment_group_view.xml',
        'views/templates.xml',
        'views/crm_lead_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto-install': False,
}
