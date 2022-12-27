# pip3 install odooly
# usar base de datos sin data demo

from odooly import Client
## AJUSTAR
new_url = 'http://p13n_vatten.15.odoo.localhost/jsonrpc'
new_db = 'p13n_vatten'
new_pass = 'admin'

### no seria necesario cambiar
old_url = 'http://odoo.vattenaguas.ar/jsonrpc'
old_db = 'vattenaguas-14-t0'
old_user = 'diego'
old_pass = 'diego'

# script
old_vatten = Client(old_url, db=old_db, user=old_user, password=old_pass)
new_vatten = Client(new_url, db=new_db, user='admin', password=new_pass)

data_list = [
    ('res.partner', [],
        ['id', 'name', 'state_id/id', 'parent_id/id'],
        ['id', 'name', 'state_id/id', 'parent_id/id'],
        'parent_id desc'),
]
# for model, domain, fields in data_list:
model, domain, export_fields, import_fields, order = data_list[0]
datas = old_vatten.env[model].search(domain, order=order).export_data(export_fields)['datas']
# TODo falta ver que las direciones de servicio no tienen nombre
new_vatten.env[model].load(import_fields, datas)

