# pip3 install odooly
# usar base de datos sin data demo
from odooly import Client
## AJUSTAR
new_url = 'http://test-vattenaguas-26-04-1.adhoc.ar/jsonrpc'
new_db = 'test-vattenaguas-26-04-1'  #cambiarbase
new_pass = 'adminadmin'
### no seria necesario cambiar
old_url = 'http://odoo.vattenaguas.ar/jsonrpc'
old_db = 'vattenaguas-14-t0'
old_user = 'diego'
old_pass = 'diego'
# script
old_vatten = Client(old_url, db=old_db, user=old_user, password=old_pass)
new_vatten = Client(new_url, db=new_db, user='admin', password=new_pass)

for i, old_muestra in enumerate(old_vatten.env['muestras'].search([])):
    partner_id = new_vatten.env['res.partner'].search_read([('name', '=', old_muestra.partner_service_id.name)], ['id'], limit=1)
    print(i)
    if partner_id:
        print(partner_id)
        new_muestra_id = new_vatten.env['muestras'].create({
            'name': old_muestra.name,
            'partner_service_id': partner_id[0]['id'],
            'parametro_ids': None,
        })
        for old_param in old_muestra.parametro_ids:
            print('in'+str(i))
            try:
                if new_vatten.env['chemical.parameter'].search([('unit','=', old_param.name.unit),('name','=',old_param.name.name),('sample_type','=',old_param.name.sample_type)]):
                    new_chemical_param_id = new_vatten.env['chemical.parameter'].search([('unit','=', old_param.name.unit),('name','=',old_param.name.name),('sample_type','=',old_param.name.sample_type)])[0].id
                else:
                    new_chemical_param_id = new_vatten.env['chemical.parameter'].create(old_param.name.read()).id
                    print("nuevo parametro creado: %s" %old_param.name.name )

                new_vatten.env['parametros'].create({
                    'chemical_parameter_id': new_chemical_param_id,
                    'muestra_id': new_muestra_id.id,
                    'min_value': old_param.min_value,
                    'max_value': old_param.max_value,
                    'in_report': old_param.in_report,
                    'in_chart': old_param.in_chart,
                })
            except:
                print('error')
