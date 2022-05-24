# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_qmax-erp",
    'version': "13.0.1.0.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'report_xlsx',
        'mrp',
    ],
    'data': [
        'report/bom_structure_xlsx.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
