# Industrial Machine and Sensor Complaint Management System

A Flask-based full-stack web application for managing industrial machine, sensor, equipment, electrical, mechanical, and supervisor-related complaints.

## Problem Statement

Large companies operate many machines, sensors, panels, and equipment. When faults happen, complaints are often delayed, assigned to the wrong team, or not tracked properly. This system allows employees to submit department-wise complaints with images/audio, while Admin and Operators track, accept, resolve, forward, and verify complaints.

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Jinja2 templates
- Backend: Python Flask
- Database: SQLite by default, MySQL/PostgreSQL possible through `DATABASE_URL`
- ORM: SQLAlchemy
- Authentication: Flask-Login
- File Storage: Local `static/uploads`
- Deployment: Railway with Gunicorn

## Features

### Public
- Home page with department cards
- Electrical, Mechanical, Supervisor complaint forms
- Photo upload
- Audio upload
- GSM alert simulation
- Success page with complaint ID

### Admin
- View all complaints
- Dashboard statistics
- Department-wise counts
- Pending, accepted, in-progress, resolved, rejected counts
- High/Critical priority count
- Average resolving time
- Filter complaints
- View details, image, audio, timers
- Forward complaints
- Update status
- Delete complaints

### Operators
- Department-specific dashboards
- View own department complaints only
- Accept complaint
- Start work
- Verify machine/sensor status
- Resolve complaint
- Add resolution notes
- Forward wrong complaints

### Simulated Machine/Sensor Verification
Each complaint stores:
- Power status: ON, LOW, OFF
- Fault status: Normal, Fault Detected, Under Repair, Resolved

A complaint can be resolved only when:
- Power status is ON
- Fault status is Resolved

## User Roles

| Role | Access |
|---|---|
| ADMIN | All complaints and all dashboards |
| OPERATOR - Electrical | Electrical complaints only |
| OPERATOR - Mechanical | Mechanical complaints only |
| OPERATOR - Supervisor | Supervisor complaints only |

## Default Login Credentials

| User | Email | Password |
|---|---|---|
| Admin | admin@company.com | admin123 |
| Electrical Operator | electrical@company.com | electrical123 |
| Mechanical Operator | mechanical@company.com | mechanical123 |
| Supervisor Operator | supervisor@company.com | supervisor123 |

## Folder Structure

```text
industrial-complaint-system/
├── app.py
├── config.py
├── requirements.txt
├── Procfile
├── README.md
├── models/
├── routes/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
└── instance/
```

## Database Schema

### User
- id
- name
- email
- password_hash
- role
- department
- created_at

### Complaint
- id
- complaint_id
- employee_name
- employee_id
- employee_phone
- department
- machine_name
- machine_id
- location
- problem_type
- description
- priority
- communication_preference
- photo_path
- audio_path
- status
- power_status
- fault_status
- accepted_by
- accepted_at
- resolved_at
- admin_remarks
- operator_remarks
- created_at
- updated_at

### ForwardHistory
- id
- complaint_id
- from_department
- to_department
- forwarded_by
- reason
- forwarded_at

### Machine
- id
- machine_name
- machine_id
- department
- location
- power_status
- fault_status
- updated_at

## Setup Instructions

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The database and default users are created automatically.

## Railway Deployment Steps

1. Push this project to GitHub.
2. Create a new Railway project.
3. Connect the GitHub repository.
4. Add environment variable:

```text
SECRET_KEY=your-production-secret-key
```

5. Railway will install dependencies from `requirements.txt`.
6. Railway will run the app using the `Procfile`:

```text
web: gunicorn app:app
```

7. Open the generated Railway domain.

## Optional Database Environment Variable

For SQLite, no extra database setup is required.

For external databases, set:

```text
DATABASE_URL=your-database-url
```

## Future Scope

- Real GSM module integration for SMS/call alerts
- IoT sensor integration for live power supply monitoring
- Real-time notifications using WebSockets
- Email/SMS alerts
- Mobile app integration
- Complaint SLA escalation
- PDF/Excel report export
- QR code machine scanning
