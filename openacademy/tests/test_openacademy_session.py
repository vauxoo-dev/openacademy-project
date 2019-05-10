# -*- encoding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError

class GlobalTestOpenAcademySession(TransactionCase):
    '''
    This create global test to sessions
    '''

    # Seudo constructor method
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.partner_axelor = self.env.ref('base.res_partner_12')
        self.course = self.env.ref('openacademy.course1')
        self.partner_attendee = self.env.ref('base.res_partner_18')

    # Generic methods

    # Test methods
    def test_10_instructor_is_attendee(self):
        '''
        Check thst raise of 'A session's instructor cant't be an attendee
        '''
        with self.assertRaisesRegexp(
                ValidationError,
                "A session's instructor can't be an attendee"
            ):
            self.session.create({
                'name': 'Session Test 1',
                'seats': 1,
                'instructor_id': self.partner_axelor.id,
                'attendee_ids': [(6, 0, [self.partner_axelor.id])],
                'course_id': self.course.id,
            })
