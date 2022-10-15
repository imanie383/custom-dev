from odoo import models, fields


class AddAttendee(models.TransientModel):
    _name = 'open_academy.session.add_attendee'
    _description = 'Wizard model for add attedees to session'

    session_id = fields.Many2one('open_academy.session', default=lambda self: self._get_session_id())
    attendee_ids = fields.Many2many('res.partner')

    def _get_session_id(self):
        return self._context.get('active_id')
