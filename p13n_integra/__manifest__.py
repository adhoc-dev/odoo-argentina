{
    'name': 'Personalizations Integra',
    'version': "15.0.1.1.0",
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account',
        'hr_timesheet',
        'payment',
        'project',
        'purchase',
        'sale',
    ],
    'data': [
        'data/ir_actions_server.xml',
        'data/mail_template_data.xml',
        'views/portal_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
