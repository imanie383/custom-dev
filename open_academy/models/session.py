from odoo import models, fields


class Session(models.Model):
    _name = 'open_academy.session'
    _description = 'Session model'

    name = fields.Char()
    start_date = fields.Date()
    duration = fields.Float()
    seats = fields.Integer()

    instructor = fields.Many2one('res.partner', domain="['|', ('instructor', '=', 'True'), ('category', '!=', False)]")
    course = fields.Many2one('open_academy.course')
    attendees = fields.Many2many('res.partner')
