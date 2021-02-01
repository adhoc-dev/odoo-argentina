##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Neored Setup',
    'version': '13.0.1.0.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': '',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'neored_personalization',
        'calendar',
        'l10n_ar_bank',
        'product_email_template',
        'product_replenishment_cost',
        'website_form',
        'base_automation',
        'note',
        'stock_picking_invoice_link',
        'base_location',
        'mass_editing',
        'sale_exception_credit_limit',
        'stock_lot_information',
        'sale_order_type',
        'product_stock_by_location',
        'account_withholding_automatic',
        'sale_exception',
        'base_address_city',
        'stock_quant_manual_assign',
        'account_invoice_commission',
        'product_template_tree_first',
        'sale_barcode',
        'account_invoice_move_currency',
        'contacts',
        'sale_order_type_invoice_policy',
        'social_media',
        'product_prices_update',
        'product_brand',
        'product_uoms',
        'purchase_suggest',
        'stock_picking_auto_create_lot',
        'stock_picking_batch',
        'stock_picking_mass_action',
        'product_internal_code',
        'product_planned_price',
        'product_unique',
        'sale_order_validity',
        'sale_require_purchase_order_number',
        'price_security_planned_price',
        'product_dimension',
        'sale_cancel_reason',
        'website_sale_product_description',
        'location_security',
        'account_journal_security',
        'stock_picking_batch',
        'base_name_search_improved',
        'product_attribute_template',
        'product_template_tags',
        'purchase_all_shipments',
        'sale_order_lot_selection',
        'stock_available_unreserved',
        'sale_margin',
        'barcodes',
        'account_3way_match',
        'mass_operation_abstract',
        'product_replenishment_cost_sale_margin',
    ],
    'data': [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
