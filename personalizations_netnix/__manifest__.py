{
    'name': 'Personalizations Netnix',
    'version': '13.0.1.1.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'helpdesk',
        'project',
    ],
    'data': [
        'security/netnix_security.xml',
        'security/ir.model.access.csv',
        'data/cron.xml'
    ],
    'installable': False,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
