{
    'name': 'Personalizations Texter feed',
    'version': "15.0.1.0.0",
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account',
        'account_payment_group',
        'account_reports',
        'l10n_ar_ux',
        'base',
        'sale',
        'purchase',
        'stock_quant_manual_assign',
    ],
    'data': [
        'data/ir_ui_menu.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/account_move_form_extension.xml',
        'wizard/stock_manual_quants_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
