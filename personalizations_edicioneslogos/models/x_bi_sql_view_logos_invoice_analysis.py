from odoo import models, fields


class XBiSqlViewLogosInvoiceAnalysis(models.Model):
    _name = 'x_bi_sql_view.logos_invoice_analysis'
    _description = 'Analisis de Facturas'

    x_price_unit = fields.Float(string="Price Unit", copy=False)
    x_discount = fields.Float(string="Discount", copy=False)
    x_price_subtotal_signed = fields.Float(string="Price Subtotal Signed", copy=False)
    x_quantity = fields.Float(string="Quantity", copy=False)
    x_price_subtotal = fields.Float(string="Price Subtotal", copy=False)
    x_price_gross_subtotal = fields.Float(string="Price Gross Subtotal", copy=False)
    x_discount_amount = fields.Float(string="Discount Amount", copy=False)
    x_partner_id = fields.Many2one(string="Partner", comodel_name="res.partner", on_delete="set null", copy=False)
    x_product_id = fields.Many2one(string="Product", comodel_name="product.product", on_delete="set null", copy=False)
    x_date_due = fields.Date(string="Date Due", copy=False)
    x_number = fields.Char(string="Number", copy=False)
    x_journal_id = fields.Many2one(string="Journal", comodel_name="account.journal", on_delete="set null", copy=False)
    x_user_id = fields.Many2one(string="User", comodel_name="res.users", on_delete="set null", copy=False)
    x_team_id = fields.Many2one(string="Team", comodel_name="crm.team", on_delete="set null", copy=False)
    x_company_id = fields.Many2one(string="Company", comodel_name="res.company", on_delete="set null", copy=False)
    x_type = fields.Char(string="Type", copy=False)
    x_state = fields.Char(string="State", copy=False)
    x_date_invoice = fields.Date(string="Date Invoice", copy=False)
    x_amount_total = fields.Float(string="Amount Total", copy=False)
    x_barcode = fields.Char(string="Barcode", copy=False)
    x_editorial_id = fields.Many2one(string="Editorial", comodel_name="product.attribute.value", on_delete="set null", copy=False)
    x_collection_id = fields.Many2one(string="Collection", comodel_name="product.attribute.value", on_delete="set null", copy=False)
    x_product_category_id = fields.Many2one(string="Product Category", comodel_name="product.category", on_delete="set null", copy=False)
    x_customer = fields.Boolean(string="Customer", copy=False)
    x_supplier = fields.Boolean(string="Supplier", copy=False)
    x_state_id = fields.Many2one(string="State", comodel_name="res.country.state", on_delete="set null", copy=False)
    x_country_id = fields.Many2one(string="Country", comodel_name="res.country", on_delete="set null", copy=False)
    x_city = fields.Char(string="City", copy=False)
