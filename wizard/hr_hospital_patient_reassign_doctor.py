from odoo import fields, models


class HrHospitalPatientReassignDoctor(models.TransientModel):
    _name = 'hr.hospital.patient.reassign.doctor'
    _description = 'Mass Reassign Personal Doctor'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
        required=True,
    )
    change_date = fields.Date(default=fields.Date.context_today)

    def action_apply(self):
        self.ensure_one()
        history_model = self.env['hr.hospital.doctor.history']
        patients = self.env['hr.hospital.patient'].browse(
            self.env.context.get('active_ids', []),
        ).filtered(lambda patient: patient.doctor_id != self.doctor_id)
        if not patients:
            return {'type': 'ir.actions.act_window_close'}
        open_lines = history_model.search([
            ('patient_id', 'in', patients.ids),
            ('change_date', '=', False),
        ])
        open_lines.write({'change_date': self.change_date})
        history_model.create([
            {
                'patient_id': patient.id,
                'doctor_id': self.doctor_id.id,
                'assign_date': self.change_date,
            }
            for patient in patients
        ])
        patients.write({'doctor_id': self.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
