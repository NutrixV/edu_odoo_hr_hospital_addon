{
    "name": "HR Hospital",
    "summary": "Manage doctors, interns, patients, diseases and visits — with role-based access and PDF reports",
    "description": """
HR Hospital
===========

Run your clinic's daily workflow inside Odoo 19.

HR Hospital keeps doctor and patient records, tracks mentorship between doctors
and interns, schedules and closes visits, and classifies diseases. Access to
sensitive visit data is governed by a clear, hierarchical permission model, and
the module ships with print-ready PDF reports.

Highlights
----------

* Doctors with qualification categories, mentors and intern lists
* Patients with personal doctor history and quick visit creation
* Visit workflow (planned / done / cancelled) with completed-visit protection
* Hierarchical, translatable disease classifier
* Per-doctor PDF report and a disease report wizard
* Five inherited security roles: Patient, Intern, Doctor, Manager, Administrator
* Full Ukrainian translation
""",
    "author": "Vitalii Sorokolit",
    "version": "19.0.5.0.0",
    "category": "Customization",
    "license": "OPL-1",
    "depends": ["base", "web"],
    "external_dependencies": {"python": []},
    "data": [
        "security/hr_hospital_groups.xml",
        "security/ir.model.access.csv",
        "security/hr_hospital_security.xml",
        "data/hr_hospital_disease_data.xml",
        "data/hr_hospital_doctor_category_data.xml",
        "views/hr_hospital_doctor_category_views.xml",
        "views/hr_hospital_doctor_views.xml",
        "views/hr_hospital_patient_views.xml",
        "views/hr_hospital_disease_views.xml",
        "views/hr_hospital_visit_views.xml",
        "views/hr_hospital_doctor_history_views.xml",
        "wizard/hr_hospital_patient_reassign_doctor_views.xml",
        "wizard/hr_hospital_visit_report_views.xml",
        "wizard/hr_hospital_disease_report_views.xml",
        "report/hr_hospital_disease_report_templates.xml",
        "report/hr_hospital_doctor_report_templates.xml",
        "views/hr_hospital_menu.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "hr_hospital/static/src/scss/report_doctor.scss",
        ],
    },
    "demo": [
        "demo/hr_hospital_disease_demo.xml",
        "demo/hr_hospital_doctor_demo.xml",
        "demo/hr_hospital_patient_demo.xml",
        "demo/hr_hospital_doctor_history_demo.xml",
        "demo/hr_hospital_visit_demo.xml",
        "demo/hr_hospital_users_demo.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": [
        "static/description/anim_flow_pro.gif",
        "static/description/banner.png",
    ],
}
