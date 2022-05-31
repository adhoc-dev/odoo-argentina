# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_jureclaplata",
    'version': "13.0.2.0.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'academic',
        'base',
        'contacts',
        'sale_subscription',
    ],
    'data': [
        'data/base_automation.xml',
        'data/student_code.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'views/sale_subscription_views.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
