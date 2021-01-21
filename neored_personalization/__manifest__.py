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
    'name': 'Neored Personalizations',
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
        'product_replenishment_cost',
        'purchase_ux',
        'base_automation',
        'product_internal_code',
        # solo para instalarlo en todos y que funcione bien odumbo sync
        # tmb necesarios por las automation rules que agregamos al final
        'website_sale',
        'product_dimension',
        'product_brand',
        'product_attribute_template',
        'product_uoms_purchase',
        'product_uoms_sale',
        'delivery_hs_code',
        'account_reports',
        'product_template_tags',
    ],
    'data': [
        'views/product_template_views.xml',
        'views/product_image_views.xml',
        'views/product_supplierinfo_views.xml',
        'security/ir.model.access.csv',
        'data/res_partner_categories_data.xml',
        'data/product_data.xml',
        'data/base_automation_data.xml',
        'data/base_automation_unlink_data.xml',
        'data/ir_cron_data.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}