{
    'name': 'personalizations_boggio',
    'version': '13.0.1.0.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account_analytic_default',
        'base_currency_inverse_rate',
        'account_check',
        'account_invoice_control',
        'account_multicompany_ux',
        'account_multicurrency_ux',
        'account_payment_group',
        'account_statement_move_import',
        'account_ux',
        'analytic',
        'base_report_to_printer',
        'board',
        'calendar',
        'crm_livechat',
        'delivery',
        'event',
        'helpdesk',
        'hr',
        'hr_holidays',
        'hr_timesheet',
        'im_livechat',
        'inter_company_rules',
        'l10n_ar_ux',
        'l10n_ar_sale',
        'l10n_ar_stock',
        'l10n_ar_website_sale',
        'account_journal_book_report',
        'mail_tracking_mass_mailing',
        'mgmtsystem_nonconformity',
        'mis_builder',
        'mrp',
        'note',
        'portal_sale_distributor',
        'price_security',
        'product_attribute_template',
        'product_brand',
        'product_catalog_aeroo_report_public_categ',
        'product_internal_code',
        'product_replenishment_cost',
        'product_sales_abc',
        'product_stock_by_location',
        'project',
        'purchase_suggest',
        'purchase_ux',
        'report_aeroo',
        'sale_margin',
        'sale_order_type_ux',
        'sale_quotation_products',
        'sale_require_purchase_order_number',
        'sale_stock_ux',
        'sale_ux',
        'sales_team',
        'sale_barcode',
        'stock_barcode',
        'stock_batch_picking_ux',
        'stock_picking_state',
        'stock_putaway_product_template',
        'stock_request_ux',
        'stock_ux',
        'stock_voucher',
        'transindar_personalization',
        'website_crm_partner_assign',
        'website_sale',
        'website_sale_ux',
        'base_automation',
        'sale_quotation_builder',
        'base_multi_store',
        'partner_sales_abc',
    ],
    'data': [
        'data/ir_cron.xml',
        'data/ir_actions_server.xml',
        'data/base_automation.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        # 'views/account_analytic_account_views.xml',
        'views/account_bank_statement_views.xml',
        'views/account_check_views.xml',
        'views/account_invoice_views.xml',
        'views/account_journal_book_group_views.xml',
        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
        'views/account_payment_views.xml',
        'views/account_payment_group_views.xml',
        'views/account_payment_term_views.xml',
        'wizards/account_statement_move_import_wizard_views.xml',
        'views/board_board_views.xml',
        'views/crm_lead_views.xml',
        'views/event_event_views.xml',
        'views/hr_employee_views.xml',
        'views/ir_actions_server_views.xml',
        'views/ir_default_views.xml',
        # 'views/mail_mass_mailing_views.xml',
        'views/mgmtsystem_nonconformity_views.xml',
        'views/mis_report_instance_views.xml',
        'wizards/mrp_product_produce_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_unbuild_views.xml',
        'views/procurement_group_views.xml',
        'views/product_attribute_views.xml',
        'views/product_attribute_line_views.xml',
        'views/product_attribute_template_views.xml',
        'views/product_attribute_value_views.xml',
        'views/product_pricelist_views.xml',
        'views/product_product_views.xml',
        'views/product_public_category_views.xml',
        'views/product_supplierinfo_views.xml',
        'views/product_template_views.xml',
        'views/project_tags_views.xml',
        'views/project_task_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_order_line_views.xml',
        'wizards/purchase_suggest_views.xml',
        'views/res_currency_views.xml',
        'views/res_groups_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_grade_views.xml',
        'views/res_partner_industry_views.xml',
        'views/res_users_views.xml',
        'views/res_users_discount_restriction_views.xml',
        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/sale_order_type_views.xml',
        'wizards/stock_backorder_confirmation_views.xml',
        'views/stock_batch_picking_views.xml',
        'views/stock_book_views.xml',
        'views/stock_inventory_views.xml',
        'views/stock_location_views.xml',
        'views/stock_move_views.xml',
        'views/stock_move_line_views.xml',
        'views/stock_picking_views.xml',
        'wizards/stock_print_stock_voucher_views.xml',
        'views/stock_request_order_views.xml',
        'wizards/stock_return_picking_views.xml',
        'views/stock_warehouse_orderpoint_views.xml',
        'views/x_controles_remitos_diarios_views.xml',
        'views/x_stock_picking_setstate_views.xml',
        'views/x_stock_breakout_views.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_ui_menu.xml',
        'report/ir_actions_report.xml',
    ],
    'installable': True,
    'auto-install': False,
    'application': False,
    'license': 'OPL-1',
}
