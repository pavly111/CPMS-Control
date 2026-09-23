# CPMS Control — Prison Management System

A full-stack prison management system for handling inmate records, prison logistics, healthcare, staff scheduling, disciplinary actions, visits, transfers, and AI-powered predictive analytics.

🔗 **Live Demo:** [https://cpms-control-1.onrender.com](https://cpms-control-1.onrender.com)

> Note: the backend runs on a free hosting tier and may take 20–30 seconds to wake up on the first request after a period of inactivity.

## Features

- **Prison & facility management** — prisons, blocks, cells, capacity tracking
- **Inmate lifecycle** — registration, legal case tracking, sentencing, automated release on sentence completion
- **Staff & scheduling** — officer management, shift assignment
- **Incidents & discipline** — incident logging, disciplinary action tracking
- **Visits system** — public visit request portal, visitor management, time-slot scheduling, email notifications on request/approval/rejection
- **Healthcare tracking** — doctor assignments, medical visit records
- **Transfers** — inter-prison transfer requests with approval workflow
- **AI-powered predictions** — inmate risk assessment and recidivism scoring, prison overcrowding forecasting
- **Role-based dashboards** — tailored views for Admins, Managers, and Officers

## Tech Stack

**Backend:** FastAPI · SQLModel · SQLite · Python
**Frontend:** React 19 · Vite · React Router · Recharts
**AI/ML:** scikit-learn · pandas · numpy · joblib
**Email:** Brevo API
**Hosting:** Render (backend + frontend)

## Getting Started Locally

### Prerequisites
- Python 3.10+
- Node.js 18+

### Setup

```bash
# Clone the repo
git clone https://github.com/pavly111/CPMS-Control.git
cd CPMS-Control

# Backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python database/initialize.py

cd backend
uvicorn main:app --reload
```

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

- Backend: http://127.0.0.1:8000
- Frontend: http://localhost:5173
- API docs: http://127.0.0.1:8000/docs

### Environment Variables

Create a `.env` file in the project root for email notifications (optional — the app runs fine without it, emails just won't send):

```env
BREVO_API_KEY=your_brevo_api_key
MAIL_FROM=your_verified_sender@example.com
MAIL_FROM_NAME=CPMS
```

## Project Structure

```
CPMS-Control/
├── ai_service/       # ML models and training notebooks
├── backend/          # FastAPI application
├── database/         # Schema, seed data, and migrations
├── frontend/         # React + Vite dashboard
└── requirements.txt
```

## License

This project was built for educational purposes.
