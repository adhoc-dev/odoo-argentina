{
    'name': 'Personalizations Netnix',
    'version': "15.0.1.0.0",
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'helpdesk',
        'project',
        'mail',
    ],
    'data': [
        'security/netnix_security.xml',
        'security/ir.model.access.csv',
        'data/cron.xml'
    ],
    'installable': True,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
