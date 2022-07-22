# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_cedent",
    'version': "13.0.1.0.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'stock_ux'
    ],
    'data': [
        'data/ir_cron_data.xml',
        'views/stock_warehouse.xml',
        'wizards/orderpoint_update_maxmin_from_suggested_wizard_views.xml'
    ],
    'demo': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
