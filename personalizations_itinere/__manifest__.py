# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_itinere",
    'version': "13.0.1.0.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'contacts',
        'hr_recruitment',
    ],
    'data': [
        'views/hr_recruitment_views.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
