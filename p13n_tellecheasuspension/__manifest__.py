{
    'name': 'Personalizations Tellechea Suspension',
    'version': "15.0.1.0.0",
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'stock',
        'product_template_tags',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_attributes_views.xml',
        'views/product_supplierinfo.xml',
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
