{
    "name": "HR Hospital",
    "summary": "Hospital management: doctors, patients, diseases and visits",
    "description": """
HR Hospital
===========

Module for hospital automation. Keeps records of:

* Doctors (with a supervising doctor)
* Patients
* Disease types
* Patient visits
""",
    "author": "Vitalii Sorokolit",
    "version": "19.0.4.0.0",
    "category": "Customization",
    "license": "OPL-1",
    "depends": ["base", "web"],
    "external_dependencies": {"python": []},
    "data": [
        "security/ir.model.access.csv",
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
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": [],
}
