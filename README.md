# 🏕️ Summer Camp Sports & User Management System

An enterprise-grade full-stack web application built using **React 18 (Vite)**, **Python FastAPI**, and **Google Cloud Firestore Database**.

---

## 🏛️ 3-Tier Architecture Flow

The project follows a strict 3-tier decoupled architecture where **React NEVER connects to Firestore directly**. All database operations pass through the **FastAPI Backend API layer**.

```text
                    USER
                      ↓
               React Frontend
            (http://localhost:5173)
                      ↓
                 HTTP Request
                      ↓
               FastAPI Backend
            (http://localhost:8000)
                      ↓
            API Route (routes/users.py)
                      ↓
          Database Layer (firestore_crud.py)
                      ↓
        Firebase Admin SDK (firebase.py)
                      ↓
           Google Cloud Firestore
                      ↓
                Data returned
                      ↓
               FastAPI Response
                      ↓
           React Renders Component
```

---

## 📁 Directory Structure

```text
summer_camp_enrollment/
├── backend/                        # FastAPI Backend Application
│   ├── routes/                     # API Routers
│   │   ├── users.py                # GET /api/users & POST /api/users
│   │   ├── sports.py               # Sports Catalog CRUD
│   │   ├── enrollments.py          # Student Registrations
│   │   └── stats.py                # Dashboard Analytics
│   ├── firebase.py                 # Firebase Admin SDK & Firestore Connection
│   ├── firestore_crud.py           # Database Queries & Firestore CRUD Operations
│   ├── models_pydantic.py          # Pydantic v2 Request/Response Validation Schemas
│   ├── main.py                     # FastAPI Entrypoint & CORS Configuration
│   ├── seed.py                     # Default Data Generator
│   ├── requirements.txt            # Python Dependencies
│   ├── firebase_credentials.json   # Google Service Account Secret Key (do not commit secrets)
│   └── .env                        # Environment Configuration
│
├── frontend/                       # React 18 SPA (Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── UserManagement.jsx  # View, Add, Display Users UI Component
│   │   │   ├── AdminDashboard.jsx  # Sports & Enrollment CRUD Dashboard
│   │   │   ├── EnrollmentModal.jsx # 4-Field Student Registration Form
│   │   │   ├── SportsCatalog.jsx   # Filterable Sports Grid
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── api.js              # Frontend API Service Layer (fetch calls to FastAPI)
│   │   ├── App.jsx                 # Main Container with Tab Navigation
│   │   └── main.jsx                # React DOM Mount Entrypoint
│   ├── package.json                # React NPM Dependencies
│   ├── vite.config.js              # Vite Build Configuration
│   └── index.html                  # HTML Page Template
│
└── README.md                       # Comprehensive System Documentation
```

---

## 🚀 Local Development Setup & Testing

### 1️⃣ Start the FastAPI Backend Server
Open a terminal in the project root:

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server using Uvicorn
python main.py
```

- **Backend API Base URL**: `http://localhost:8000`
- **Interactive Swagger Documentation**: `http://localhost:8000/docs`
- **Users API Endpoints**:
  - `GET /api/users` ➔ Retrieve users from Firestore
  - `POST /api/users` ➔ Create a new user in Firestore

---

### 2️⃣ Start the React Frontend (Vite)
Open a second terminal window in the project root:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite Development Server
npm run dev
```

- **React Development UI**: `http://localhost:5173`

---

## 🧪 End-to-End Testing Verification

1. Start the FastAPI backend and open `http://localhost:8000/docs`.
2. Test `GET /api/users` ➔ Verify JSON array of users is retrieved from Firestore.
3. Test `POST /api/users` ➔ Add a new user (`name`, `email`, `age`, `role`) and verify `201 Created`.
4. Start the React frontend and open `http://localhost:5173`.
5. Click **Users Management** in the navigation bar.
6. Fill out the **Add New User** form and click **Create User in Firebase**.
7. Verify that the user appears instantly in the table on screen and is saved in **Google Cloud Firestore**!

---

## 🔒 Security & Best Practices

- **Zero Hardcoded Secrets**: Firebase credentials and CORS origins are configured via `backend/.env`.
- **CORS Enabled**: Allowed origins `http://localhost:5173`, `http://127.0.0.1:5173`, and `http://localhost:8000` are configured in `backend/main.py`.
- **Validation**: Pydantic models validate input fields (`email`, `age >= 1`, `name length`).
