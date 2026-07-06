from datetime import date

from odoo.tests.common import TransactionCase


class TestPatient(TransactionCase):
    def test_age_computed_from_birthdate(self):
        patient = self.env['hr.hospital.patient'].create({
            'name': 'Age Test',
            'birthdate': date(2000, 1, 1),
        })
        self.assertGreaterEqual(patient.age, 25)

    def test_age_zero_without_birthdate(self):
        patient = self.env['hr.hospital.patient'].create({'name': 'No Birthdate'})
        self.assertEqual(patient.age, 0)
