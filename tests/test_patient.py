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

    def test_visit_count_and_action_domain(self):
        doctor = self.env['hr.hospital.doctor'].create({'name': 'Doc'})
        patient = self.env['hr.hospital.patient'].create({
            'name': 'Visits Test',
            'doctor_id': doctor.id,
        })
        self.env['hr.hospital.visit'].create([
            {'patient_id': patient.id, 'doctor_id': doctor.id}
            for _dummy in range(2)
        ])
        self.assertEqual(patient.visit_count, 2)
        action = patient.action_view_visits()
        self.assertEqual(action['domain'], [('patient_id', '=', patient.id)])

    def test_quick_visit_defaults(self):
        doctor = self.env['hr.hospital.doctor'].create({'name': 'Personal Doc'})
        patient = self.env['hr.hospital.patient'].create({
            'name': 'Quick Visit Test',
            'doctor_id': doctor.id,
        })
        action = patient.action_create_quick_visit()
        self.assertEqual(action['target'], 'new')
        self.assertEqual(action['context']['default_patient_id'], patient.id)
        self.assertEqual(action['context']['default_doctor_id'], doctor.id)
