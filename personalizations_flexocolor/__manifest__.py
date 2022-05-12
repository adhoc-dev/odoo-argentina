{
    'name': 'Personalizations Flexocolor',
    'version': '13.0.1.0.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'product',
        'account',
        'sale',
        'sale_management'
    ],
    'data': [
        'report/ir.action.reports.xml',
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_template_templates.xml',
        'views/custom_header.xml'
    ],
    'installable': False,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
