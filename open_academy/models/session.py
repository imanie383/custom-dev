from odoo import models, fields, api


class Session(models.Model):
    _name = 'open_academy.session'
    _description = 'Session model'

    name = fields.Char()
    start_date = fields.Date()
    duration = fields.Float()
    seats = fields.Integer()
    taken_seats = fields.Float(compute='_compute_taken_seats')

    instructor = fields.Many2one('res.partner', domain="['|', ('instructor', '=', 'True'), ('category', '!=', False)]")
    course = fields.Many2one('open_academy.course')
    attendees = fields.Many2many('res.partner')

    @api.depends('seats', 'attendees')
    def _compute_taken_seats(self):
        for record in self:
            attendees = len(record.attendees)
            seats = record.seats
            if attendees >= seats or seats == 0:
                percentage = 100
            else:
                percentage = (100 * attendees) / seats
            record.taken_seats = percentage
