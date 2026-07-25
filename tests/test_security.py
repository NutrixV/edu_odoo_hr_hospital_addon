from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestSecurity(TransactionCase):
    """Access rights and record rules for the hospital group hierarchy."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Users = cls.env['res.users']

        def make_user(name, login, group_xmlid):
            return Users.create({
                'name': name,
                'login': login,
                'group_ids': [Command.set([cls.env.ref(group_xmlid).id])],
            })

        cls.user_patient = make_user('Sec Patient User', 'sec_patient', 'hr_hospital_management.group_hospital_patient')
        cls.user_intern = make_user('Sec Intern User', 'sec_intern', 'hr_hospital_management.group_hospital_intern')
        cls.user_doctor = make_user('Sec Doctor User', 'sec_doctor', 'hr_hospital_management.group_hospital_doctor')
        cls.user_other = make_user('Sec Other Doctor User', 'sec_other', 'hr_hospital_management.group_hospital_doctor')
        cls.user_manager = make_user('Sec Manager User', 'sec_manager', 'hr_hospital_management.group_hospital_manager')
        cls.user_admin = make_user('Sec Admin User', 'sec_admin', 'hr_hospital_management.group_hospital_admin')

        Doctor = cls.env['hr.hospital.doctor']
        cls.doctor = Doctor.create({'name': 'Sec Doctor', 'user_id': cls.user_doctor.id})
        cls.intern = Doctor.create({
            'name': 'Sec Intern',
            'user_id': cls.user_intern.id,
            'category_id': cls.env.ref('hr_hospital_management.hr_hospital_category_intern').id,
            'mentor_id': cls.doctor.id,
        })
        cls.other_doctor = Doctor.create({'name': 'Sec Other Doctor', 'user_id': cls.user_other.id})

        Patient = cls.env['hr.hospital.patient']
        cls.patient = Patient.create({'name': 'Sec Patient', 'user_id': cls.user_patient.id})
        cls.other_patient = Patient.create({'name': 'Sec Other Patient'})

        Visit = cls.env['hr.hospital.visit']
        cls.visit_of_patient = Visit.create({'patient_id': cls.patient.id, 'doctor_id': cls.other_doctor.id})
        cls.visit_of_intern = Visit.create({'patient_id': cls.other_patient.id, 'doctor_id': cls.intern.id})
        cls.visit_of_doctor = Visit.create({'patient_id': cls.other_patient.id, 'doctor_id': cls.doctor.id})
        cls.visit_foreign = Visit.create({'patient_id': cls.other_patient.id, 'doctor_id': cls.other_doctor.id})

    def _visible_visits(self, user):
        return self.env['hr.hospital.visit'].with_user(user).search([])

    def test_patient_reads_only_own_visits(self):
        self.assertEqual(set(self._visible_visits(self.user_patient).ids), {self.visit_of_patient.id})

    def test_patient_cannot_write_visit(self):
        with self.assertRaises(AccessError):
            self.visit_of_patient.with_user(self.user_patient).write({'note': 'hacked'})

    def test_patient_reads_only_own_patient_record(self):
        found = self.env['hr.hospital.patient'].with_user(self.user_patient).search([])
        self.assertEqual(set(found.ids), {self.patient.id})

    def test_intern_reads_and_edits_own_visits(self):
        self.assertEqual(set(self._visible_visits(self.user_intern).ids), {self.visit_of_intern.id})
        self.visit_of_intern.with_user(self.user_intern).write({'note': 'intern note'})
        self.assertEqual(self.visit_of_intern.note, 'intern note')

    def test_intern_cannot_read_foreign_visit(self):
        with self.assertRaises(AccessError):
            self.visit_of_doctor.with_user(self.user_intern).read(['note'])

    def test_intern_cannot_create_visit(self):
        with self.assertRaises(AccessError):
            self.env['hr.hospital.visit'].with_user(self.user_intern).create({
                'patient_id': self.other_patient.id,
                'doctor_id': self.intern.id,
            })

    def test_doctor_sees_own_and_intern_visits(self):
        self.assertEqual(
            set(self._visible_visits(self.user_doctor).ids),
            {self.visit_of_doctor.id, self.visit_of_intern.id},
        )

    def test_doctor_edits_intern_visit(self):
        self.visit_of_intern.with_user(self.user_doctor).write({'note': 'mentor note'})
        self.assertEqual(self.visit_of_intern.note, 'mentor note')

    def test_doctor_cannot_read_unrelated_visit(self):
        with self.assertRaises(AccessError):
            self.visit_foreign.with_user(self.user_doctor).read(['note'])

    def test_manager_sees_all_visits(self):
        ours = {
            self.visit_of_patient.id,
            self.visit_of_intern.id,
            self.visit_of_doctor.id,
            self.visit_foreign.id,
        }
        all_visits = set(self.env['hr.hospital.visit'].sudo().search([]).ids)
        visible = set(self._visible_visits(self.user_manager).ids)
        self.assertEqual(visible, all_visits)
        self.assertTrue(ours <= visible)

    def test_manager_cannot_unlink_visit(self):
        with self.assertRaises(AccessError):
            self.visit_foreign.with_user(self.user_manager).unlink()

    def test_admin_unlinks_any_module_data(self):
        self.visit_foreign.with_user(self.user_admin).unlink()
        self.assertFalse(self.visit_foreign.exists())
        disease = self.env['hr.hospital.disease'].create({'name': 'Sec Disease'})
        disease.with_user(self.user_admin).unlink()
        self.assertFalse(disease.exists())
