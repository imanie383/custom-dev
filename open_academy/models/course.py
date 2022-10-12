from odoo import models, fields


class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'Course model'
    _sql_constraints = [
        ('title-description-diff', 'CHECK(title != description)', 'The description and title must be different'),
        ('title-unique', 'UNIQUE(title)', 'The title must be unique'),
    ]

    title = fields.Char(required=True)
    description = fields.Text()

    responsible = fields.Many2one('res.users')
    sessions = fields.One2many('open_academy.session', 'course')
