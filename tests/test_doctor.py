from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestDoctor(TransactionCase):
    def setUp(self):
        super().setUp()
        self.intern_cat = self.env.ref('hr_hospital_management.hr_hospital_category_intern')
        self.Doctor = self.env['hr.hospital.doctor']

    def test_is_intern_computed(self):
        doctor = self.Doctor.create({
            'name': 'Intern D',
            'category_id': self.intern_cat.id,
        })
        self.assertTrue(doctor.is_intern)

    def test_is_intern_false_without_category(self):
        doctor = self.Doctor.create({'name': 'No Category'})
        self.assertFalse(doctor.is_intern)

    def test_intern_cannot_be_mentor(self):
        intern = self.Doctor.create({
            'name': 'Intern M',
            'category_id': self.intern_cat.id,
        })
        junior = self.Doctor.create({'name': 'Junior'})
        with self.assertRaises(ValidationError):
            junior.mentor_id = intern

    def test_intern_ids_inverse_of_mentor(self):
        mentor = self.Doctor.create({'name': 'Mentor X'})
        intern = self.Doctor.create({
            'name': 'Intern X',
            'category_id': self.intern_cat.id,
            'mentor_id': mentor.id,
        })
        self.assertEqual(mentor.intern_ids, intern)

    def test_quick_visit_defaults(self):
        doctor = self.Doctor.create({'name': 'Quick Doc'})
        action = doctor.action_create_quick_visit()
        self.assertEqual(action['target'], 'new')
        self.assertEqual(action['context']['default_doctor_id'], doctor.id)

    def test_mentor_cannot_become_intern(self):
        mentor = self.Doctor.create({'name': 'Mentor'})
        self.Doctor.create({
            'name': 'Mentee',
            'category_id': self.intern_cat.id,
            'mentor_id': mentor.id,
        })
        with self.assertRaises(ValidationError):
            mentor.category_id = self.intern_cat

    def test_visit_ids_newest_first(self):
        doctor = self.Doctor.create({'name': 'Report Doc'})
        patient = self.env['hr.hospital.patient'].create({'name': 'Report Pat'})
        old = self.env['hr.hospital.visit'].create({
            'doctor_id': doctor.id,
            'patient_id': patient.id,
            'scheduled_date': '2026-01-10 09:00:00',
        })
        new = self.env['hr.hospital.visit'].create({
            'doctor_id': doctor.id,
            'patient_id': patient.id,
            'scheduled_date': '2026-03-10 09:00:00',
        })
        doctor.invalidate_recordset(['visit_ids'])
        self.assertEqual(doctor.visit_ids.ids, [new.id, old.id])

    def test_patient_ids_inverse_of_personal_doctor(self):
        doctor = self.Doctor.create({'name': 'Personal Doc'})
        patient = self.env['hr.hospital.patient'].create({
            'name': 'Linked Pat',
            'doctor_id': doctor.id,
        })
        self.assertEqual(doctor.patient_ids, patient)
