from odoo import models, fields


class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'Course model'

    title = fields.Char(required=True)
    description = fields.Text()
