{
    'name': 'Personalizations Netso',
    'version': '13.0.1.1.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'purchase',
        'account',
    ],
    'data': [
        'data/ir_cron.xml',
        'views/res_partner_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_report_templates.xml'
    ],
    'installable': False,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
