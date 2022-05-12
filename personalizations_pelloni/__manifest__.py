{
    'name': 'personalizations_Pelloni',
    'version': '13.0.1.9.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'sale_subscription',
        'l10n_ar_account_direct_debit',
    ],
    'data': [
        'views/account_direct_debit_mandate_views.xml',
        'views/sale_subscription_views.xml',
        'views/account_move_views.xml',
    ],
    'application': False,
    'installable': False,
    'license': 'OPL-1',
}
