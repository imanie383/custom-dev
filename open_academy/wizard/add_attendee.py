from odoo import models, fields


class AddAttendee(models.TransientModel):
    _name = 'open_academy.session.add_attendee'
    _description = 'Wizard model for add attedees to session'

    session_ids = fields.Many2many('open_academy.session', default=lambda self: self._get_session_ids())
    attendee_ids = fields.Many2many('res.partner')

    def _get_session_ids(self):
        return self._context.get('active_ids')

    def add_attendee(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
