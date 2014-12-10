from openerp import fields, models

'''
This module create model of Course
'''

class Course(models.Model):
    '''
    This class create model of Course
    '''
    _name = 'openacademy.course'  #  Model odoo name

    name = fields.Char(string='Title', required=True)  #  Field reserved to identified name rec
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users',
                     		     ondelete='set null',
				     string="Responsible", index=True)

