{
    'name': 'Personalizations Gastrotex',
    'version': "15.0.1.0.0",
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'crm',
        'sale',
        'l10n_ar_ux',
        'account_invoice_partial',
    ],
    'data': [
        'views/crm_lead_views.xml',
        'views/report_invoice.xml',
        'views/account_move_views.xml',
        'security/res_groups.xml',
        'security/ir_rule.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
