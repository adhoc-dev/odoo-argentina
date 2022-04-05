{
    'name': 'personalizations_sba',
    'version': '13.0.1.6.0',
    'category': 'Personalizations',
    'license': 'OPL-1',
    'author': 'ADHOC SA',
    'depends': [
        'account_analytic_default',
        'hr_expense',
        'purchase',
        'sale_ux',
        'stock_ux',
        'helpdesk',
        'stock_request_ux',
        'sale_exception_credit_limit',
        'l10n_ar',
        'product_management_group',
        'product_template_tags',
        'purchase_ux',
        'product_ux',
        'delivery',
    ],
    'data': [
        'security/personalizations_sba_security.xml',
        'views/account_invoice_views.xml',
        'views/hr_expense_views.xml',
        'views/hr_expense_sheet_views.xml',
        'views/product_pricelist_views.xml',
        'views/product_pricelist_item_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_bank_views.xml',
        'views/sale_order_views.xml',
        'views/stock_move_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',
        'views/account_move_report_personalization.xml',
        'views/sale_report_personalization.xml',
        'wizards/stock_return_picking_views.xml',
        'views/x_product_autor_views.xml',
        'views/x_product_categoria_views.xml',
        'views/x_product_editorial_views.xml',
        'views/x_product_familia_views.xml',
        'views/x_product_language_views.xml',
        'views/x_product_subcategoria_views.xml',
        'views/x_product_version_views.xml',
        'views/x_res_partner_stage_views.xml',
        'data/ir_actions_act_window.xml',
        'report/ir_actions_report.xml',
        'data/ir_ui_menu.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
