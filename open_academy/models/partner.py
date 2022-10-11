from odoo import models, fields


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    instructor = fields.Boolean()
    sessions = fields.Many2many('open_academy.session', 'instructor')
