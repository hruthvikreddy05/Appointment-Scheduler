# Appointment-Scheduler
A lightweight, full-stack Appointment Scheduler application built with Python (FastAPI) and vanilla JavaScript. It enables users to book, view, and delete appointments in real time through an interactive web interface.
# 📅 Full-Stack Appointment Scheduler with Automated Email Reminders

A full-stack web application for scheduling appointments, persisting data in SQLite via SQLAlchemy ORM, and automatically dispatching email reminders 6 hours prior to appointment times using APScheduler and Gmail SMTP.

---

## 🏗️ System Architecture & Workflow

1. **Frontend (`index.html`)**: User submits booking info through an HTML interface. Asynchronous JavaScript (`fetch` API) handles communication without page reloads.
2. **Backend (`main.py`)**: FastAPI exposes REST endpoints (`GET`, `POST`, `DELETE`), enforcing structural validation via Pydantic.
3. **Database (`database.py` & `models.py`)**: SQLite (`appointments.db`) persists record entries managed through SQLAlchemy ORM.
4. **Background Service (`reminder_service.py`)**: APScheduler scans database entries periodically every 5 minutes.
5. **Notification System**: When an appointment occurs within the 6-hour window, Python establishes an encrypted TLS session with `smtp.gmail.com:587` to send an automated confirmation email.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (`fetch`) | User interface and asynchronous HTTP requests |
| **Backend** | Python, FastAPI, Uvicorn | Web API routing, execution, and server management |
| **Database** | SQLite, SQLAlchemy ORM | Local relational data persistence and schema mapping |
| **Validation** | Pydantic | Request body payload validation |
| **Scheduler** | APScheduler | Recurrent background execution tasks |
| **Email Transport** | `smtplib`, `python-dotenv` | Encrypted SMTP communication and safe credential handling |

---

## 📁 Project Structure

```text
Appointment_schedule/
│
├── main.py                # FastAPI routes and scheduler setup
├── database.py            # SQLite engine and session configuration
├── models.py              # SQLAlchemy database models
├── reminder_service.py    # Background email check and SMTP dispatcher
├── index.html             # HTML frontend interface
├── .env                   # Environment variables (credentials)
├── .gitignore             # Git exclusion directives
└── README.md              # Documentation
