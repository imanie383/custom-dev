from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean()
    sessions = fields.Many2many('open_academy.session', 'instructor')
    category = fields.Selection([('a', 'Teacher/Level 1'), ('b', 'Teacher/Level 2'),])
