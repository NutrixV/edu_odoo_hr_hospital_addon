from datetime import date

from odoo.tests.common import TransactionCase


class TestDoctorHistory(TransactionCase):
    def setUp(self):
        super().setUp()
        self.patient = self.env['hr.hospital.patient'].create({'name': 'John Roe'})
        self.category = self.env['hr.hospital.doctor.category'].create({'name': 'Test Cat'})
        self.doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Dr House',
            'category_id': self.category.id,
        })

    def test_display_name_format(self):
        history = self.env['hr.hospital.doctor.history'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'assign_date': date(2026, 1, 5),
        })
        self.assertEqual(history.display_name, 'John Roe - Dr House (Test Cat) 2026-01-05')

    def test_display_name_without_category(self):
        doctor = self.env['hr.hospital.doctor'].create({'name': 'Dr NoCat'})
        history = self.env['hr.hospital.doctor.history'].create({
            'patient_id': self.patient.id,
            'doctor_id': doctor.id,
            'assign_date': date(2026, 2, 10),
        })
        self.assertEqual(history.display_name, 'John Roe - Dr NoCat () 2026-02-10')

    def test_onchange_change_date_warning(self):
        history = self.env['hr.hospital.doctor.history'].new({
            'assign_date': date(2026, 2, 1),
            'change_date': date(2026, 1, 1),
        })
        result = history._onchange_change_date()
        self.assertIn('warning', result)

    def test_onchange_valid_dates_no_warning(self):
        history = self.env['hr.hospital.doctor.history'].new({
            'assign_date': date(2026, 1, 1),
            'change_date': date(2026, 2, 1),
        })
        self.assertIsNone(history._onchange_change_date())

    def test_demo_history_records(self):
        demo = self.env.ref(
            'hr_hospital.hr_hospital_doctor_history_demo_1',
            raise_if_not_found=False,
        )
        if not demo:
            self.skipTest('Demo data is not loaded in this database.')
        self.assertTrue(demo.change_date)
