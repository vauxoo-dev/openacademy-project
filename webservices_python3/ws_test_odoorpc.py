import odoorpc

odoo = odoorpc.ODOO('localhost', port=8069)
print(odoo.db.list())


odoo.login('odoodb', 'admin', 'admin')
user = odoo.env.user
print(user)

print(user.name)            # name of the user connected
print("active", user.company_id.partner_id.name) # the name of its company


user_data = odoo.execute('res.users', 'read', [user.id], ['password'])
print(user_data)

user.name = 'moylop260'
