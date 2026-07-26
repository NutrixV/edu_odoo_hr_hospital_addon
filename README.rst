HR Hospital
===========

Hospital automation module for Odoo 19: doctors, interns, patients,
diseases and patient visits.

Features
--------

* Doctors with qualification categories, mentors and intern lists.
* Patients with personal doctor history and quick visit creation.
* Hierarchical disease classifier (Ukrainian translation included).
* Visit workflow: planned / done / cancelled, with completed-visit
  protection rules.
* Printable PDF report per doctor and disease report wizard.
* Role-based security: Patient, Intern, Doctor, Manager and
  Administrator groups with record-level rules on visits.

Installation
------------

Add the repository to ``addons_path`` and install the module::

    python odoo-bin -c odoo.conf -d <db> -i hr_hospital_management

Configuration
-------------

Assign one of the *Hospital* groups to each user
(Settings > Users & Companies > Users):

* **Patient** — sees only own visits (linked via the patient's
  *System User* field).
* **Intern** — sees and edits own visits.
* **Doctor** — additionally sees and edits the visits of mentored
  interns.
* **Manager** — sees all visits and manages master data.
* **Administrator** — may delete any module data.

Tests
-----

Run the module test suite::

    python odoo-bin -c odoo.conf -d <db> -u hr_hospital_management --test-enable --stop-after-init

Changelog
---------

See ``changelog.rst``.

License
-------

LGPL-3 — see the ``LICENSE`` file.

Author
------

* Vitalii Sorokolit (support: support@example.com)
