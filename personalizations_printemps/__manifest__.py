{
    'name': 'Personalizations Printemps',
    'version': '13.0.1.1.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account',
        'product',
        'stock_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/price_history_views.xml',
        'views/product_views.xml',
        'views/res_partner_view.xml',
    ],
    'installable': False,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
