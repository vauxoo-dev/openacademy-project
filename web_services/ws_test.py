import xmlrpclib
import functools

HOST = 'localhost'
PORT = 8069
DB = 'i18n_plantilla'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1. Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print "Logged in as %s (uid:%d)" % (USER,uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# 2. Read the sessions
model = 'openacademy.session'
domain = []
method_name = 'search_read'
sessions = call(model, method_name, domain, ['name', 'seats', 'taken_seats'])
print "sessions",sessions

for session in sessions:
    print "Session %s (%s seats), taken seats %d" % (session['name'], session['seats'], session['taken_seats'])

method_name = 'search'
domain = [('name', '=', 'Curso Odoo 1')]
course_ids = call('openacademy.course', method_name, domain)
course_id = course_ids[0]
print "course_ids",course_ids


method_name = 'create'
course_id = call('openacademy.course', method_name, {'name': 'Curso Odoo 1'})

method_name = 'create'
new_sesion_id = call(model, method_name, {
	'name': 'Sesion from ws', 
	'course_id': course_id,
 
     })
print "new_sesion_id",new_sesion_id
