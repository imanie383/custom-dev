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

    instructor_id = fields.Many2one('res.partner', domain="['|', ('instructor', '=', 'True'), ('category', '!=', False)]")
    course_id = fields.Many2one('open_academy.course')
    attendee_ids = fields.Many2many('res.partner')
    attendee_count = fields.Integer(compute='_compute_attendee_count', store=True, readonly=True)

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for record in self:
            attendees = len(record.attendee_ids)
            seats = record.seats
            if attendees >= seats or seats == 0:
                percentage = 100
            else:
                percentage = (100 * attendees) / seats
            record.taken_seats = percentage

    @api.depends('attendee_ids')
    def _compute_attendee_count(self):
        for record in self:
            record.attendee_count = len(record.attendee_ids)

    @api.onchange('seats', 'attendee_ids')
    def _onchange_seats(self):
        if self.seats < 0:
            return {'warning': {'title': 'Warning', 'message': 'Invalid number of seats'}}

        if len(self.attendee_ids) > self.seats:
            return {'warning': {'title': 'Warning', 'message': 'Insufficient seats'}}

    @api.constrains('instructor', 'attendee_ids')
    def _check_instructor(self):
        for record in self:
            if record.instructor_id in record.attendee_ids:
                raise exceptions.ValidationError("Instructor %s is attendee in his/her own session" % record.instructor.name)
