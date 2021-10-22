# SBA Personalizations

Este es el modulo de personalizaciones par Sociedadd Biblica.

Comprende un par de endpoints diseñados especialmente para ellos a petición que utilizaran para conectarse y extraer/actualizar información desde SalesForce. Los endpoint disponibles via REST API son los siguientes.

* `GET /api/{api_key}/get_new_contacts`: Este devolverá todos los contactos que estan en el Odoo y los valores de sus campos. Se le puede pasar un body opcional con el valor {"from_date": "2021-06-06 10:20:00"} el cual lo que hace es devolver solo los contactos cuya fecha de creación o de actualización haya sido mayor o igual a la fecha "from_date" suministrada.

* `POST /api/{api_key}/update_contact`: Este endpoint permite actualizar un contacto en el Odoo, para poder funcionar necesitamos enviarle un body con el siguiente formato {"values": {"ref": "hola prueba"}, "partner_id": 5} donde:

  * `values`: son los valores que queremos escribir en el Odoo, en el ejemplo estamos escribiendo "hola prueba" en el campo "ref" del contacto.
  * `partner_id`> es un numero entero y representa el ID del res.partner que queremos actualizar.

* `GET /api/{api_key}/get_validated_invoices`: Este endpoint permite devolver la información de las facturas validadas en Odoo y el detalle de sus lineas. Se le puede pasar un body opcional con el valor {"from_date": "2021-06-06 10:20:00"} el cual lo que hace es devolver solo las facturas cuya fecha de creación o de actualización haya sido mayor o igual a la fecha "from_date" suministrada.
