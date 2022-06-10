{
    'name': 'Personalizations Gastrotex',
    'version': '13.0.1.4.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'crm',
        'l10n_ar_ux',
    ],
    'data': [
        'views/crm_lead_views.xml',
        'views/report_invoice.xml',
        'security/res_groups.xml',
        'security/ir_rule.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
