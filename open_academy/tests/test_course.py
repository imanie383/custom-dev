from odoo.tests import TransactionCase
from odoo.tools.misc import mute_logger
from psycopg2.errors import CheckViolation, UniqueViolation


class TestCourse(TransactionCase):
    def create_course(self, name, description):
        return self.env['open_academy.course'].create({
            'name': name,
            'description': description,
            })

    @mute_logger('odoo.sql_db')
    def test_04_validate_name_and_description(self):
        with self.assertRaises(CheckViolation) as cv:
            self.create_course('test_course', 'test_course')
        the_exception = cv.exception
        # 23514 = CheckViolation
        self.assertEqual(the_exception.pgcode, '23514')

    @mute_logger('odoo.sql_db')
    def test_05_validate_name_unique(self):
        with self.assertRaises(UniqueViolation) as uv:
            self.create_course('test_course', 'course A')
            self.create_course('test_course', 'course B')
        the_exception = uv.exception
        # 23505 = UniqueViolation
        self.assertEqual(the_exception.pgcode, '23505')

    def test_06_duplication(self):
        course = self.create_course('test_course', 'course A')
        course.copy()
