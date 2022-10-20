from odoo import models, fields, api, _


class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'Course model'
    _sql_constraints = [
        ('name-description-diff', 'CHECK(name != description)', 'The description and name must be different'),
        ('name-unique', 'UNIQUE(name)', 'The name must be unique'),
    ]

    name = fields.Char(required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users')
    session_ids = fields.One2many('open_academy.session', 'course_id')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        count = self.search_count([
            ('name', '=like', _('Copy of %s%%') % self.name)])
        if not count:
            new_name = _('Copy of %s') % self.name
        else:
            new_name = _('Copy of %s (%d)' % (self.name, count))

        if default is None:
            default = {}
        default['name'] = new_name

        return super(models.Model, self).copy(default)
