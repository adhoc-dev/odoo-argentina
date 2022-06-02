{
    'name': 'personalizations_baratec',
    'version': '13.0.1.0.0',
    'category': 'Personalizations',
    'license': 'OPL-1',
    'author': 'ADHOC SA',
    'depends': [
        'product_catalog_aeroo_report',
    ],
    'data': [
        'report/catalog_report_view.xml',
        'report/report_catalog.xml',
        'wizards/product_catalog_wizard_views_inherit.xml',
        'views/product_catalog_report_extension.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
