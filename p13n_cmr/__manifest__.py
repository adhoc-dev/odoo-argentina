{
    'name': 'personalizations_cmr',
    'version': '15.0.1.0.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account_payment_group',
        'public_budget',
    ],
    'data': [
        'data/ir_actions_server_data.xml',
        'data/ir_config_parameter_data.xml',
        'security/ir.model.access.csv',
        'wizards/download_files_wizard_views.xml',
        'views/res_company_view.xml',
    ],
    'application': False,
    'installable': True,
    'license': 'OPL-1',
}
