from odoo import models, fields


class AddAttendee(models.TransientModel):
    _name = 'open_academy.session.add_attendee'
    _description = 'Wizard model for add attedees to session'

    session_id = fields.Many2one('open_academy.session')
    attendee_ids = fields.Many2many('res.partner')
