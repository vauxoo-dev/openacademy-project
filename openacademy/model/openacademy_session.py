# -*- coding: utf-8 -*-
from openerp import fields, models

class Session(models.Model):
   _name = 'openacademy.session'

   name = fields.Char(required=True)
   start_date = fields.Date()
   duration = fields.Float(digits=(6, 2), help="Duration in days")
   seats = fields.Integer(string="Number of seats")
   instructor_id = fields.Many2one('res.partner', string="Instructor")
   course_id = fields.Many2one('openacademy.course',
        ondelete='cascade', string="Course", required=True)

