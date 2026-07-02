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

    def test_insurance_size_limit(self):
        field = self.env['hr.hospital.patient']._fields['insurance_number']
        self.assertEqual(field.size, 20)

    def test_inherits_medic_mixin(self):
        patient_model = self.env['hr.hospital.patient']
        for field_name in ('blood_group', 'rh_factor', 'gender', 'birthdate', 'age'):
            self.assertIn(field_name, patient_model._fields)
