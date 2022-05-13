# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_jureclaplata",
    'version': "13.0.1.0.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'academic',
        'contacts',
        'sale_subscription',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_subscription_views.xml',
        'data/base_automation.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
