# 🏕️ Summer Camp Sports Enrollment System

A full-stack, web-based application built for customers (parents and students) to browse, filter, and enroll in various sports activities offered during a summer camp.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20JS-orange)

---

## 🧱 Tech Stack

- **Backend**: Python **FastAPI** (RESTful API architecture, Pydantic v2 schemas, auto-generated OpenAPI/Swagger docs).
- **Database Layer**: **SQLAlchemy 2.0 ORM** (defaulting to SQLite persistent file storage for zero-dependency local execution; fully compatible with MySQL / PostgreSQL via `DATABASE_URL` environment configuration).
- **Frontend UI**: Single-Page Application (SPA) with **HTML5**, **CSS3** (responsive grid/flex layouts, CSS variables, custom modals), and **Vanilla JavaScript** (ES6 Fetch API, real-time filters, digital pass generator, toast alerts).
- **Testing**: **Pytest** with FastAPI `TestClient`.

---

## ✨ Features & Navigation

### 1. ⚽ Sports Catalog & Real-Time Search
- Supports multiple sports activities across diverse categories (**Team Sports**, **Water Sports**, **Racket Sports**, **Combat & Fitness**, **Outdoor & Track**).
- Real-time search and filtering by:
  - Keyword (Title, instructor, description, or location)
  - Category
  - Participant Age
- Live capacity bar tracking total capacity vs enrolled count.

### 2. 📝 Interactive Enrollment & Strict Business Logic Validations
- Step-by-step enrollment registration form collecting participant details, parent contact, medical notes, T-shirt size, and payment plan choices.
- Enforces strict business validations:
  - **Age Restriction Check**: Rejects enrollment if participant's age is outside the sport's allowed age range.
  - **Capacity Safeguard**: Blocks registration when maximum capacity is reached.
  - **Duplicate Prevention**: Prevents registering the same student into the same sport twice.
  - **Data Integrity**: Validates email format, required inputs, and phone numbers via FastAPI/Pydantic schemas.

### 3. 🎫 Digital Enrollment Confirmation Pass
- Generates a unique **Enrollment Code** (e.g. `CAMP-2026-X89A2`).
- Provides a customer lookup portal (by parent email, phone, or enrollment code).
- Interactive, printable digital enrollment pass modal with QR code placeholder for camp check-in.
- Supports enrollment cancellation/withdrawal with immediate capacity release.

### 4. 📊 Administrative Dashboard
- Analytics metrics: Active Sports Count, Confirmed Campers, Total Revenue, Open Spots Remaining.
- CRUD operations for Sports: Create new sports, edit details/capacity, or soft delete/deactivate activities.
- Registrations Management: Table displaying all registrations with status filters (Confirmed/Cancelled) and detailed participant passes.

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/sports` | List sports activities (Filterable by `category`, `age`, `search`) |
| `GET` | `/api/sports/{id}` | Get detailed sport information |
| `POST` | `/api/sports` | Create a new sport activity (Admin) |
| `PUT` | `/api/sports/{id}` | Update sport activity details/capacity (Admin) |
| `DELETE` | `/api/sports/{id}` | Deactivate a sport activity (Admin) |
| `POST` | `/api/enrollments` | Submit a new enrollment with business logic checks |
| `GET` | `/api/enrollments` | Search enrollments (`email`, `phone`, `participant`, `status`) |
| `GET` | `/api/enrollments/{code}` | Retrieve single enrollment by enrollment code |
| `PUT` | `/api/enrollments/{id}/cancel` | Cancel an active enrollment |
| `GET` | `/api/stats` | Summary statistics for Admin Dashboard |
| `GET` | `/docs` | Interactive Swagger UI API Documentation |

---

## 🚀 Getting Started

### 1. Requirements
- Python 3.9+
- Packages listed in `requirements.txt`

### 2. Installation
```bash
# Clone or navigate to the project directory
cd C:\Users\Girish Kumar V\.gemini\antigravity\scratch\summer_camp_enrollment

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Server
```bash
python run.py
```
Or with Uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

Open your browser and navigate to:
- **Web Application Interface**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Database Configuration (Optional MySQL Setup)
By default, the system uses SQLite database (`summer_camp.db`).
To connect to an online MySQL database (e.g. `freesqldatabase.com` or local MySQL server), set the `DATABASE_URL` environment variable:

```bash
# Windows PowerShell
$env:DATABASE_URL="mysql+pymysql://username:password@host:3306/dbname"
python run.py
```

### 5. Running Automated Tests
```bash
python -m pytest -v
```
