# Healthcare Management System (Flask + SQLite)

A lightweight, ready-to-run web app for managing patients and appointments.

## Features
- Add, edit, delete **Patients** (name, age, gender, phone, address, medical history).
- Schedule and manage **Appointments** (date/time, doctor, notes, status).
- Dashboard with quick counts.
- SQLite database (auto-created on first run).
- Clean, responsive UI (Bootstrap CDN).
- Simple REST-style JSON endpoints for patients and appointments (read-only).

## Quick Start

```bash
python -m venv .venv
# Activate:
#   Windows: .venv\\Scripts\\activate
#   macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt

python app.py
# App will start at http://127.0.0.1:5000
```

## Notes
- The database file `healthcare.db` is created automatically on first run in the project folder.
- JSON APIs: `/api/patients`, `/api/appointments` (read-only).
