from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestDoctorCategory(TransactionCase):
    def test_name_unique(self):
        self.env['hr.hospital.doctor.category'].create({'name': 'Unique Cat'})
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
            self.env['hr.hospital.doctor.category'].create({'name': 'Unique Cat'})

    def test_master_categories_exist(self):
        self.assertTrue(self.env.ref('hr_hospital.hr_hospital_category_intern'))
        self.assertTrue(self.env.ref('hr_hospital.hr_hospital_category_specialist'))
        self.assertTrue(self.env.ref('hr_hospital.hr_hospital_category_expert'))
