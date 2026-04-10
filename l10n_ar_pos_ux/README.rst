.. |company| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. |company_logo| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

================================
Argentinian Point of Sale UX
================================

This module extends the Point of Sale functionality to properly handle Argentine tax perceptions when generating invoices from POS orders.

**Problem**
-----------

In Odoo's standard Point of Sale flow, when creating invoices from POS orders, the tax IDs are explicitly passed to the invoice lines. This prevents the automatic computation of Argentine tax perceptions that should be added based on the customer's fiscal position.

The issue occurs because:

1. POS passes explicit ``tax_ids`` when creating invoice lines
2. This bypasses the ``_get_computed_taxes()`` method where perceptions are normally added
3. Result: Invoices are created with VAT but without the required perceptions

**Solution**
------------

This module fixes the perception calculation by:

1. **Ensuring Fiscal Position Assignment**: Overrides ``_complete_values_from_session()`` to properly calculate and assign the customer's fiscal position to the POS order, using either the manually set fiscal position or the automatically computed one based on customer data.

2. **Enabling Automatic Tax Computation**: Overrides ``_get_invoice_lines_values()`` to detect when a fiscal position has configured perceptions. When perceptions are present, it removes the explicit ``tax_ids`` from the invoice line creation data, allowing Odoo's standard tax computation flow to execute.

3. **Leveraging Existing Infrastructure**: Uses the existing ``l10n_ar_tax`` module's ``_get_computed_taxes()`` override, which automatically adds perceptions from the fiscal position through the ``_l10n_ar_add_taxes()`` method.

**Technical Details**
---------------------

The module works by intercepting the invoice creation process:

.. code-block:: python

    # Standard flow (without this module):
    POS Order → Invoice Lines with explicit taxes → No perception computation

    # With this module:
    POS Order → Fiscal position detected → No explicit taxes passed → 
    _compute_tax_ids() → _get_computed_taxes() → Perceptions added automatically

**Installation**
================

1. Install the module:

   .. code-block:: bash

      odoo-bin -i l10n_ar_pos_ux -d your_database

2. No additional configuration is required.

**Configuration**
=================

Ensure your customers have:

1. A fiscal position with Argentine tax perceptions configured (``l10n_ar_tax_ids``)
2. Appropriate perception taxes configured in the fiscal position
3. Partner perception configuration if using partner-specific rates

**Usage**
=========

1. Open a POS session
2. Create an order for a customer that has a fiscal position with perceptions
3. Generate the invoice from the POS order
4. The invoice will now include both VAT and the configured perceptions automatically

**Example**
-----------

Customer setup:
- Fiscal Position: "CABA Percepciones"
- Perception: IIBB CABA 3%

POS Order:
- Product: $100
- VAT 21%: $21
- **Perception IIBB 3%: $3** (automatically added)
- **Total: $124**

**Bug Tracker**
===============

Bugs are tracked on `GitHub Issues <https://github.com/ingadhoc/odoo-argentina/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

**Credits**
===========

**Images**
----------

* ADHOC SA: `Icon <https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png>`_.

**Contributors**
----------------

* ADHOC SA <https://www.adhoc.com.ar>

**Maintainer**
--------------

|company_logo|

This module is maintained by ADHOC SA.

To contribute to this module, please visit https://www.adhoc.com.ar.
