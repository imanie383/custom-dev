from odoo.tests import TransactionCase
from odoo.tools.misc import mute_logger
from psycopg2.errors import NotNullViolation


class TestSession(TransactionCase):

    @mute_logger('odoo.sql_db')
    def test_01_instructor_required(self):
        with self.assertRaises(NotNullViolation) as nnv:
            self.env['open_academy.session'].create({
                'name': 'session_1',
                'course_id': self.env.ref('open_academy.record_0').id,
                })
        the_exception = nnv.exception
        # 23502 = NotNullViolation
        self.assertEqual(the_exception.pgcode, '23502')

    def test_02_session_flow(self):
        session = self.env['open_academy.session'].create({
            'name': 'session_1',
            'course_id': self.env.ref('open_academy.record_0').id,
            'instructor_id': self.env.ref('base.res_partner_2').id,
            })
        self.assertEqual(session.state, 'draft')
        session.action_confirm()
        self.assertEqual(session.state, 'confirmed')
        session.action_done()
        self.assertEqual(session.state, 'done')

    @mute_logger('odoo.sql_db')
    def test_03_course_required(self):
        with self.assertRaises(NotNullViolation) as nnv:
            self.env['open_academy.session'].create({
                'name': 'session_1',
                'instructor_id': self.env.ref('base.res_partner_2').id,
                })
        the_exception = nnv.exception
        # 23502 = NotNullViolation
        self.assertEqual(the_exception.pgcode, '23502')
