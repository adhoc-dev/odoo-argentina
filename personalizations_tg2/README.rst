.. |company| replace:: ADHOC SA

.. |company_logo| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. |icon| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-icon.png

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

====================
Personalizations tg2
====================

Cambios hecho por personalización:

En lineas analíticas:

- Campo x_presupuestado

- Restringir que no se pueda crear una linea analítica si no hay producto elegido.

- Al crear asiento manual para diarios del tipo "general" dejar crear sin tener el producto asignado.

- Campo producto en empleado para que al cargar hs se genere la linea analítica con el producto de ese empleado



 En ordenes de venta

- Crear campo state, y visualizarlo en vista lista de pedidos y con botón en la vista form para cerrar y abrir la OV.

- Campo "Monto a facturar " en la vista lista para ver el monto que se queda para facturar.



 En Ordenes de compra.

- Campos cuenta analítica y etiqueta analíticas que al elegir completa con ese valor en las lineas de la orden.



En Transferencias (inventario)

- Campos cuenta analítica y etiqueta analíticas que al elegir completa con ese valor en las lineas de la transferencia.



En cuentas analíticas:

-Si no tiene padre, muestra un botón para acceder a las cuentas analíticas hijas, llamadas “Rubros”

-Al acceder a los “Rubros” desde dicho botón, se pueden Crear nuevos Rubros y esto crea una cuenta analítica indicando “Cuenta analítica madre” por defecto = a la original desde donde se accedió.

-En cuentas analíticas que SI tienen padre, se muestra en la vista form, una solapa “Lineas de presupuesto” que muestra el listado de apuntes analíticos del tipo Presupuestado. En modo edición se pueden crear lineas de este tipo.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: http://runbot.adhoc.com.ar/

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/ingadhoc/personalizations/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* |company| |icon|

Contributors
------------

Maintainer
----------

|company_logo|

This module is maintained by the |company|.

To contribute to this module, please visit https://www.adhoc.com.ar.
