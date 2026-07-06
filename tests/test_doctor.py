from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestDoctor(TransactionCase):
    def setUp(self):
        super().setUp()
        self.intern_cat = self.env.ref('hr_hospital.hr_hospital_category_intern')
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

    def test_mentor_cannot_become_intern(self):
        mentor = self.Doctor.create({'name': 'Mentor'})
        self.Doctor.create({
            'name': 'Mentee',
            'category_id': self.intern_cat.id,
            'mentor_id': mentor.id,
        })
        with self.assertRaises(ValidationError):
            mentor.category_id = self.intern_cat
