import xmlrpc.client
import functools


HOST = 'localhost'
PORT = 8069

DB = 'odoodb'
USER = 'admin'
PASS = 'admin'

root = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

uid = xmlrpc.client.ServerProxy(root + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid: %d)" % (USER, uid))

call = functools.partial(
    xmlrpc.client.ServerProxy(root + 'object').execute,
    DB, uid, PASS)

sessions = call('openacademy.session', 'search_read', [], ['name', 'seats', 'taken_seats'])
for session in sessions:
    print("Session %s (%s seats) Taken Seats %d" % (session['name'], session['seats'], round(session['taken_seats'], 0)))

users = call('res.users', 'search_read', [('id', '=', uid)], ['name', 'company_id', 'password'])
print("users data:", users)

instructor_id = 14
try:
    course_id = call('openacademy.course', 'search', [('name', 'ilike', 'Course 0')])
    if course_id:
        course_id = course_id[0]
        session_id = call('openacademy.session', 'create', {
            'name': 'My session',
            'course_id': course_id,
            'instructor_id': instructor_id,
            'attendee_ids': [(4, instructor_id)]
        })
    else:
        print("Ni siquiera aparecio, pero sin error")
except IndexError as e:
    print("No se pudo crear la session, porque no se encontró el curso %s" % e)

# call('openacademy.course', 'create', {
#         'name': 'Course 0',
#     })


