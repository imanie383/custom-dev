from odoo import models, fields, api, exceptions


class Session(models.Model):
    _name = 'open_academy.session'
    _description = 'Session model'

    name = fields.Char()
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float()
    seats = fields.Integer()
    active = fields.Boolean(default=True)

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

    @api.onchange('seats', 'attendees')
    def _onchange_seats(self):
        if self.seats < 0:
            return {'warning': {'title': 'Warning', 'message': 'Invalid number of seats'}}

        if len(self.attendees) > self.seats:
            return {'warning': {'title': 'Warning', 'message': 'Insufficient seats'}}

    @api.constrains('instructor', 'attendees')
    def _check_instructor(self):
        for record in self:
            if record.instructor in record.attendees:
                raise exceptions.ValidationError("Instructor %s is attendeer in his/her own session" % record.instructor.name)
