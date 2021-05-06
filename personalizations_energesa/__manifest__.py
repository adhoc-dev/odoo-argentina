{
    'name': 'personalizations_energesa',
    'version': '13.0.1.0.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account',
        'account_analytic_default',
        'account_asset',
        'account_budget',
        'account_check',
        'account_journal_book_report',
        'account_journal_security',
        'account_payment_group',
        'account_payment_group_document',
        'account_reports',
        'barcodes',
        'base',
        'base_automation',
        'calendar',
        'crm',
        'date_range',
        'delivery',
        'document_page',
        'google_drive',
        'helpdesk',
        'helpdesk_timesheet',
        'hr_timesheet',
        'l10n_ar_ux',
        'l10n_ar_sale',
        'mail',
        'mgmtsystem',
        'mrp',
        'partner_identification',
        'payment',
        'product',
        'product_catalog_aeroo_report',
        'product_margin',
        'product_pack',
        'product_planned_price',
        'product_price_taxes_included',
        'product_replenishment_cost',
        'project',
        'project_forecast',
        'project_ux',
        'purchase_ux',
        'purchase_stock_ux',
        'purchase_request_department',
        'purchase_requisition',
        'report_aeroo',
        'resource',
        'sale',
        'sale_margin',
        'sale_order_type_user_default',
        'sale_stock_ux',
        'sale_product_pack',
        'sale_timesheet',
        'sale_ux',
        'sales_team',
        'stock',
        'stock_analytic',
        'stock_inventory_preparation_filter',
        'stock_picking_invoice_link',
        'utm',
    ],
    'data': [
        'security/res_groups.xml',
        'views/account_account_views.xml',
        'views/account_check_views.xml',
        'views/account_invoice_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_line_views.xml',
        'views/account_payment_views.xml',
        'views/account_payment_group_views.xml',
        'views/crm_activity_report_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_team_views.xml',
        'views/document_page_views.xml',
        'views/helpdesk_stage_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/mail_mail_views.xml',
        'views/mrp_production_views.xml',
        'views/procurement_group_views.xml',
        'views/product_pack_line_views.xml',
        'views/product_pricelist_views.xml',
        'views/product_product_views.xml',
        'views/product_supplierinfo_views.xml',
        'views/product_template_views.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        'views/project_task_type_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_request_views.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/sale_report_views.xml',
        'views/stock_inventory_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_production_lot_views.xml',
        # 'views/utm_campaign_views.xml',
        'views/x_account_payment_group_stage_views.xml',
        'views/x_instaladores_views.xml',
        'views/x_tipoinsta_views.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_actions_server.xml',
        'data/ir_ui_menu.xml',
        'data/base_automation.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'application': False,
    'installable': True,
    'auto-install': False,
    'license': 'OPL-1',
}
