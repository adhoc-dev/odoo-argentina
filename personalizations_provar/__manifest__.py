{
    'name': 'personalizations_provar',
    'version': '13.0.1.1.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'stock',
    ],
    'demo': [
        'data/stock_locations_demo.xml',
    ],
    'data': [
        'views/stock_location_views.xml',
        'views/stock_quant_views.xml',
        'data/sync_stock_cron.xml',
        'data/ir_config_parameter.xml',
    ],
    'external_dependencies': {
        'python': [
            'odooly',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
