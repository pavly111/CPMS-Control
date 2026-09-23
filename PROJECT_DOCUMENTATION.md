# CPMS Control — Full Project Documentation

## 1. Project name and purpose

CPMS Control is a full-stack prison management system designed to help manage prison operations, inmate records, prison logistics, healthcare, staff scheduling, disciplinary actions, visits, transfers, and predictive analytics.

The project combines:

- a FastAPI backend for the business logic and database access
- a React + Vite frontend for the management dashboard
- SQLite as the main database engine
- AI-powered risk and overcrowding prediction modules
- role-based access for admins, managers, and officers

The system is structured to simulate a real prison administration platform where users can manage prison infrastructure and inmate operations from a single application.

---

## 2. Project overview

This application is built around prison administration workflows. It supports:

- prison and block/cell management
- inmate registration and release tracking
- legal case and sentence tracking
- staff and officer administration
- shift assignment and scheduling
- incident reporting and response
- disciplinary record management
- visit scheduling and visitor management
- medical visits and doctor management
- transfer requests between prisons
- pending inmate processing
- AI-generated risk and overcrowding predictions

The project is organized into separate layers to keep the application maintainable:

- frontend: user interface and navigation
- backend: API endpoints, authentication, business logic
- database: schema, migration, and seed scripts
- ai_service: trained ML models and training artifacts

---

## 3. Tech stack

### Backend

- Python 3
- FastAPI
- SQLModel
- SQLite
- Pydantic
- pwdlib (password hashing)
- Uvicorn

### Frontend

- React 19
- Vite
- React Router DOM
- Recharts
- Lucide React
- ESLint

### AI / analytics

- scikit-learn pipelines saved as joblib models
- pandas
- numpy
- joblib

### Database and migration tools

- SQLite
- SQL migration scripts in the database folder
- initialization and seed automation through Python scripts

---

## 4. High-level architecture

The application follows a classic layered design:

1. Frontend layer
   - React application renders screens and interacts with REST APIs.
   - Routing is handled using React Router.
   - Role-based dashboards and forms are defined under src/pages.

2. API layer
   - FastAPI app exposes REST routes grouped by domain.
   - Each route is attached to a router under backend/routers.
   - Business rules and database operations are implemented in these modules.

3. Data layer
   - SQLite database stores system data.
   - Schema and seed scripts are defined in database/schemas and database/seeds.
   - Database initialization runs automatically on backend startup through create_db_and_tables.

4. AI layer
   - risk prediction and overcrowding forecast models are loaded from ai_service/models.
   - The backend uses these models to provide prison and inmate predictions.

---

## 5. Root directory structure

```text
CPMS-Control/
├── ai_service/
│   ├── models/
│   └── training/
├── backend/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── __init__.py
│   ├── check_release.py
│   ├── database.py
│   ├── email_service.py
│   ├── main.py
│   └── oauth.py
├── database/
│   ├── migrations/
│   ├── schemas/
│   ├── seeds/
│   ├── initialize.py
│   └── migrate.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── .env
├── readme.md
├── requirements.txt
├── run.bat
├── run.sh
├── setup.bat
├── setup.sh
└── prison.db
```

---

## 6. Backend architecture

### Main application file

The backend entry point is:

- backend/main.py

This file:

- creates the FastAPI app
- sets up CORS
- defines a startup lifecycle using lifespan
- ensures database tables are created
- runs the release checker on startup
- starts a background task that periodically checks inmate releases every 3600 seconds
- includes all API routers

### Database connection

The database connection is managed in:

- backend/database.py

Key responsibilities:

- defines the SQLite database URL
- creates the SQLModel engine
- exposes SessionDep for dependency injection
- runs the project initialization script when the app starts

### Authentication and authorization

The authentication logic is handled in:

- backend/oauth.py

This file defines:

- password hashing and verification
- login identity lookup for admin and officer users
- basic role detection (admin, manager, officer)
- current-user dependency injection via OAuth2PasswordBearer

The user login API is defined in:

- backend/routers/authentication.py

It exposes endpoints for:

- login/token
- create_admin
- create_officer
- users/me

---

## 7. Backend routers and features

The project has domain-based routers in backend/routers.

### 7.1 Prison-related modules

- prison.py
- block.py
- cell.py

Responsibilities:

- create and manage prison records
- manage prison type/security settings
- manage blocks within prisons
- manage cells and capacity information
- get prison summaries and nested block/cell reports

### 7.2 Inmate management

- inmate.py
- pending_inmate.py
- legal_case.py

Responsibilities:

- register inmates
- manage active/inactive/released statuses
- process incoming pending inmates
- assign inmates to prisons and cells
- record legal cases and sentence durations
- release inmates automatically based on sentence completion

### 7.3 Staff and workforce

- staff.py

Responsibilities:

- manage prison staff/officers
- return staff by prison
- create and query officers

### 7.4 Shift and staffing control

- shift.py

Responsibilities:

- create shifts
- view shift schedules by prison, block, or officer
- manage shift removal and assignment workflow

### 7.5 Incidents and discipline

- incidents.py
- disciplinary.py

Responsibilities:

- log prison incidents
- relate incidents to inmates and officers
- filter incidents by prison, block, officer, or inmate
- record disciplinary actions and durations
- track who imposed the discipline and why

### 7.6 Visits and visitor system

- visit.py

Responsibilities:

- create and manage visitor records
- manage visit time slots
- schedule inmate visits
- retrieve available dates and times
- update and delete visit entries

### 7.7 Healthcare module

- doctor.py
- medical_visit.py

Responsibilities:

- add doctors to prisons
- track medical visits for inmates
- query visits by inmate, prison, or doctor

### 7.8 Transfers

- transfer.py

Responsibilities:

- create inmate transfer requests
- manage approval and rejection of transfer requests
- retrieve transfers by prison or transfer ID
- update assigned prison and status after approval

### 7.9 Machine learning endpoints

- machine_learning.py

Responsibilities:

- expose inmate risk predictions
- expose prison overcrowding forecasts
- refresh ML prediction tables for a single prison or all prisons

### 7.10 Authentication

- authentication.py

Responsibilities:

- log in as admin, manager, or officer
- create system users
- return authenticated user metadata

---

## 8. Data models

The project uses SQLModel table models and Pydantic schemas.

### Core model files in backend/models

- inmate.py
- inmates_risk.py
- legal_case.py
- pending_inmate.py
- prison.py
- shift.py
- transfer.py
- visit.py

### Schema files in backend/schemas

These define request and response payloads for FastAPI validation, including:

- block.py
- cell.py
- disciplinary.py
- doctor.py
- incidents.py
- inmate.py
- legal_case.py
- login.py
- medical_visit.py
- ML.py
- pending_inmate.py
- prison.py
- shift.py
- staff.py
- transfer.py
- visit.py

The schema layer keeps API input consistent and ensures request validation.

---

## 9. Database design

The database is initialized using SQLite and the scripts under database/.

### Initialization process

The script:

- database/initialize.py

does the following:

1. connects to prison.db
2. runs all SQL schema files in database/schemas
3. runs database/migrate.py
4. runs all seed files in database/seeds
5. prevents repeated execution for seed files using a seeds tracking table

### Schema files

The schema files are named in order:

- 001_super_admin.sql
- 002_prison.sql
- 003_block.sql
- 004_cell.sql
- 005_inmate.sql
- 006_legal_case.sql
- 007_visitor.sql
- 008_visit.sql
- 009_doctor.sql
- 010_health_visit.sql
- 011_incident.sql
- 012_incident_involvement.sql
- 013_disciplinary_log.sql
- 014_transfer.sql
- 015_officer.sql
- 016_shift.sql
- 017_migrations_and_seeds.sql
- 018_pending_inmate.sql

### Seed files

The seed files mirror the same domain order, for example:

- 001_super_admin.sql
- 002_prison.sql
- 003_block.sql
- 004_cell.sql
- 005_inmate.sql
- 006_legal_case.sql
- 007_visitor.sql
- 008_visit.sql
- 009_doctor.sql
- 010_health_visit.sql
- 011_incident.sql
- 012_incident_involvement.sql
- 013_disciplinary_log.sql
- 014_transfer.sql
- 015_officer.sql
- 016_shift.sql
- 018_pending_inmate.sql

### Core database entities

The project manages a wide range of data models, including:

- super_admin
- prison
- block
- cell
- inmate
- pending_inmate
- legal_case
- visitor
- visit
- doctor
- health_visit
- incident
- incident_involvement
- disciplinary_log
- transfer
- officer
- shift
- seeds
- migrations

### Automatic release logic

The backend automatically checks whether prisoners have completed their sentences and releases them if appropriate.

This happens in:

- backend/main.py

The logic:

- runs account release updates on application startup
- periodically loops every hour
- clears pending transfers and old incident references for released inmates
- updates inmate or pending inmate status to Released
- clears prison and cell assignments

---

## 10. AI and predictive components

The project includes ML-based prediction systems for:

- inmate risk assessment
- prison overcrowding prediction

### Risk prediction module

Files:

- backend/services/risk_predictor.py
- ai_service/models/risk_behavior_pipeline.pkl
- ai_service/models/recidivism_score_pipeline.pkl

This module:

- loads multiple trained ML models
- extracts inmate profile features from the database
- calculates age, prison, incident counts, disciplinary durations, sentence duration, etc.
- predicts inmate risk level and recidivism score
- stores predictions in inmates_risk table

Risk levels included:

- High
- Medium
- Low

### Overcrowding prediction module

Files:

- backend/services/overcrowding_predict.py
- ai_service/models/overcrowding.pkl

This module:

- calculates prison occupancy features like capacity, occupancy rate, admissions, transfer activity, and sentence remaining duration
- applies custom feature engineering to match the training pipeline
- predicts whether a prison may become overcrowded in the near future
- stores the predicted occupancy values in the overcrowding table

### API routes for ML

The routes are exposed by:

- backend/routers/machine_learning.py

Endpoints include:

- /ML/risk
- /ML/overcrowding
- /ML/machine_learning_refresh/{prison_id}
- /ML/machine_learning_refresh

These endpoints let the frontend fetch prediction summaries and trigger recalculation of model output.

---

## 11. Frontend application structure

The frontend is located in:

- frontend/src/

### Main app shell

- frontend/src/App.jsx

This file defines the app routes and navigation:

- /login
- /visit-request
- /dashboard/superadmin
- /dashboard/manager
- /dashboard/officer
- /prisons
- /prisons/add
- /prisons/:id
- /inmates
- /inmates/add
- /inmates/:id
- /officers
- /transfers
- /visits
- /visits/slots
- /incidents
- /disciplinary
- /healthcare
- /shifts
- /ml

### Frontend pages by domain

- auth/
  - Login screen

- dashboard/
  - SuperAdminDashboard
  - ManagerDashboard
  - OfficerDashboard

- prisons/
  - MyPrison
  - PrisonsList
  - PrisonDetail
  - PrisonForm

- inmates/
  - InmatesList
  - InmateDetail
  - InmateForm
  - InmateAssignForm

- officers/
  - OfficersList
  - OfficerForm

- transfers/
  - TransfersList
  - TransferForm

- visits/
  - VisitsList
  - VisitSlots

- incidents/
  - IncidentsList
  - IncidentDetail
  - IncidentForm

- disciplinary/
  - DisciplinaryList
  - DisciplinaryForm

- healthcare/
  - HealthcareOverview
  - DoctorForm
  - MedicalVisitForm

- shifts/
  - ShiftsList

- ml/
  - MLPredictions

- public/
  - PublicVisitRequest

### Styling

The frontend uses:

- CSS modules and custom styles under frontend/src/styles and frontend/src/pages
- a global app layout component for dashboard shell and navigation
- React context providers for things like toast notifications

---

## 12. Role model and access control

The system supports multiple roles:

### Admin

- super administrator
- manages overall system setup
- creates admin users
- oversees prison operations at the system level

### Manager

- prison manager
- has prison-specific management access
- typically tied to a prison via manager_id

### Officer

- security or operational staff member
- assigned to a prison
- can create incident records, shifts, and other operational actions

Login behavior is implemented in backend/oauth.py:

- super_admin lookup is checked first
- officer lookup is checked second
- if the officer is the manager of a prison, the returned role is manager
- otherwise the role is officer

The login route returns:

- access_token
- token_type
- role
- name
- prison_id

---

## 13. Core business workflows

### 13.1 Prison creation and structure

A prison record includes:

- name
- type
- security level
- location
- manager_id
- facility flags for hospital, workshops, agricultural ward, visitation hall
- visitation hall capacity

Prisons contain blocks, and blocks contain cells. This structure supports physical prison management and capacity planning.

### 13.2 Inmate lifecycle

The inmate lifecycle includes:

- pending inmate admission
- assignment to prison and cell
- legal case creation
- sentence tracking
- transfers
- disciplinary events
- incident involvement
- release after sentence expiration

### 13.3 Transfer system

Transfer requests allow inmates to move between prisons subject to approval.

Typical states include:

- Pending
- Approved
- Rejected

The transfer process is recorded with source and destination prison information and approval dates.

### 13.4 Visits scheduling

The system records:

- visitors
- visit slots
- actual visit events
- visitor availability and visit dates

This supports both public and internal scheduling workflows.

### 13.5 Healthcare tracking

The healthcare part of the system tracks:

- doctors assigned to prison facilities
- medical visits for inmates
- doctor and prison relation

### 13.6 Discipline and incident tracking

The system records:

- incident type and location
- inmate involvement
- officer involvement
- imposed disciplinary actions
- duration of consequences

---

## 14. Setup and run instructions

### Quick setup with scripts

The project provides automated scripts in the root directory:

#### macOS/Linux

```bash
./setup.sh
./run.sh
```

#### Windows

```cmd
setup.bat
run.bat
```

### Manual setup

#### 1. Create Python virtual environment

```bash
python -m venv .venv
```

#### 2. Activate the environment

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```cmd
.venv\Scripts\activate
```

#### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create environment file

A .env file is expected with SMTP settings:

```env
MAIL_USERNAME=username
MAIL_PASSWORD=**********
MAIL_FROM=test@email.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

#### 5. Initialize database

```bash
python database/initialize.py
```

#### 6. Start backend

```bash
cd backend
uvicorn main:app --reload
```

#### 7. Start frontend

```bash
cd frontend
npm install
npm run dev
```

### Default application URLs

- Backend: http://127.0.0.1:8000
- Frontend: http://localhost:5173

---

## 15. Run scripts

### setup.sh

This script:

- checks that frontend and backend folders exist
- creates a local Python virtual environment if missing
- installs Python dependencies
- creates a .env file if not present
- verifies Node.js and npm availability
- installs frontend packages

### run.sh

This script:

- activates the virtual environment
- starts the backend with uvicorn on port 8000
- starts the Vite frontend in background mode
- runs the release checker script
- opens the app in the browser if supported
- shuts down both processes on exit

---

## 16. Security and authentication notes

The application currently uses a simplified auth implementation:

- it verifies password hashes using pwdlib
- it treats the token as a username or national ID value rather than a JWT
- it loads the user from the database on each request

This is a lightweight implementation suitable for a local project and demo environment, but it is not a production-grade JWT system.

---

## 17. Release and time-based automation

One important component of the system is the release checker:

- backend/check_release.py
- backend/main.py

This service automatically updates inmate and pending inmate statuses when their sentence period has ended.

The logic includes:

- checking each active inmate’s sentence duration
- comparing to the current date
- clearing pending transfers and incident involvement linked to released inmates
- clearing assigned cell and prison assignments
- updating records to Released

This is helpful for operational correctness and reduces manual administrative work.

---

## 18. AI-model lifecycle and assumptions

The ML pipeline is integrated in a practical way:

- models are loaded once at runtime
- prediction results are saved into SQL tables for later retrieval
- risk and overcrowding endpoints read from these saved predictions
- the project expects model files to exist under ai_service/models

If the model files are missing or not trained correctly, the system logs warnings and continues without crashing, though predictions will be unavailable.

---

## 19. Main dependencies from requirements.txt

The Python requirements include:

- fastapi
- uvicorn
- sqlmodel
- pandas
- numpy
- scikit-learn
- joblib
- python-dotenv
- pydantic
- email-validator
- pwdlib
- pymysql or related database-specific packages as needed

The project is clearly designed to run in a local or departmental environment, not necessarily a cloud-scale deployment.

---

## 20. Frontend and backend interaction pattern

The frontend communicates with the backend through HTTP requests to FastAPI endpoints.

Typical data flow:

1. User logs in from the frontend.
2. Backend validates credentials and returns role + prison context.
3. Frontend loads dashboards based on role.
4. Dashboards fetch data from relevant endpoints.
5. Business logic runs in the backend and queries SQLite.
6. AI endpoints provide classification and forecasting data.
7. The UI renders the results using charts and table-based screens.

---

## 21. Project strengths

This project is strong in several areas:

- complete prison domain coverage
- layered architecture with frontend/backend separation
- role-based access model
- full database initialization and migration flow
- strong reporting and overview features for prison operations
- ML integration for prediction and planning
- automated release handling

---

## 22. Potential improvement areas

Although the project is feature-rich, a few areas could be improved for serious production deployment:

- replace the simple token approach with real JWT-based auth
- harden validation and authorization by route
- add unit and integration tests
- improve database migration safety
- add deployment configuration for production environments
- separate environment configuration from local development settings
- add CI/CD pipeline
- improve error logging and observability

---

## 23. Summary

The CPMS Control project is a comprehensive prison administration and monitoring application designed for managing prison operations from a single system. It includes both operational management and predictive analytics, making it suitable for:

- prison administration offices
- prison managers and officers
- inmate tracking and legal compliance
- staff scheduling and incident handling
- healthcare and visits tracking
- future planning based on overcrowding and risk analysis

In short, this is a full-stack platform that combines enterprise-style operational workflows with machine learning support for prison management decisions.

---

## 24. Quick command cheat sheet

### Start the app

```bash
./run.sh
```

### Setup app

```bash
./setup.sh
```

### Backend only

```bash
cd backend
uvicorn main:app --reload
```

### Frontend only

```bash
cd frontend
npm run dev
```

### Initialize database

```bash
python database/initialize.py
```

---

This document serves as a high-level but comprehensive overview of the application architecture, workflows, features, and operational logic.
