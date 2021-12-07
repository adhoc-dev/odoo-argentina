# Copyright 2019 Vauxoo
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_cotesma",
    'version': "13.0.1.1.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'stock_request_ux',
        ],
    'data': [
        'views/res_users_views.xml',
        'views/stock_request_order_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
