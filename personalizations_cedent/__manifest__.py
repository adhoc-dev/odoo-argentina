# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_cedent",
    'version': "15.0.1.0.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'stock_ux',
        'sale',
        'sale_coupon',
    ],
    'data': [
        'data/ir_cron_data.xml',
        'data/ir_actions_server.xml',
        'views/stock_warehouse.xml',
        'views/sale_coupon_program_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
