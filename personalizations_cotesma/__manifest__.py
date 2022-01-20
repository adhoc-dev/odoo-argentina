# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_cotesma",
    'version': "13.0.1.6.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'stock_request_ux',
        'purchase_requisition',
        'purchase_suggest',
        'product_template_tags',
        'project_ux',
    ],
    'data': [
        'security/cotesma_security.xml',
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/res_users_views.xml',
        'views/stock_request_order_views.xml',
        'views/purchase_requisition_views.xml',
        'wizards/purchase_suggest_view.xml',
    ],
    'demo': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
