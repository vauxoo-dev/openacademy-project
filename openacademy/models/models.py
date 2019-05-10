# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import time
from psycopg2 import IntegrityError
from datetime import timedelta

def get_uid(self, *a):
    return self.env.uid

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
        'res.users', string="Responsible",
        index=True, ondelete='set null',
        # default=lambda self, *a: self.env.uid)
        default=get_uid)
    session_ids = fields.One2many('openacademy.session', 'course_id')

    _sql_constraints = [
        ('name_description_check',
         'CHECK( name != description )',
         "The title of the course should not be the description"
        ),
        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique",
        ),
    ]

    def copy(self, default=None):
        if default is None:
            default = {}
        copied_count = self.search_count([
            ('name', 'ilike', _('Copy of %s%%') % (self.name))])
        if not copied_count:
            new_name = _("Copy of %s") % (self.name)
        else:
            new_name = _("Copy of %s (%s)") % (self.name, copied_count)
        default['name'] = new_name
        # try:
        return super(Course, self).copy(default)
        # except IntegrityError:
        #     import pdb; pdb.set_trace()

class Session(models.Model):
    _inherit = ['mail.thread']
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    datetime_test = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string='Instructor',
                                    domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Teacher')],
                                    company_dependent=True,)
    course_id = fields.Many2one('openacademy.course', ondelete='cascade',
                                string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(compute='_taken_seats', store=True)
    active = fields.Boolean(default=True)
    end_date = fields.Date(store=True, compute='_get_end_date',
                           inverse='_set_end_date')
    attendees_count = fields.Integer(compute='_get_attendees_count', store=True)
    color = fields.Float()
    hours = fields.Float(
        string="Duration in hours",
        compute='_get_hours', inverse='_set_hours')


    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for record in self.filtered('start_date'):
            record.end_date = record.start_date + timedelta(days=record.duration, seconds=-1)

    def _set_end_date(self):
        for record in self.filtered('start_date'):
            start_date = fields.Datetime.from_string(record.start_date)
            end_date = fields.Datetime.from_string(record.end_date)
            record.duration = (end_date - start_date).days + 1

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self.filtered(lambda r: r.seats):
            record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.filtered(lambda r: r.seats < 0):
            self.active = False
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats may not be negative"),
                }
            }
        if self.seats < len(self.attendee_ids):
            self.active = False
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                }
            }
        self.active = True

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self.filtered('instructor_id'):
            if record.instructor_id in record.attendee_ids:
                raise exceptions.ValidationError(
                        _("A session's instructor can't be an attendee"))

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        # __import__('pdb').set_trace()
        res['fields']['name']['string'] = 'Que ondas Boludo'
        return res
