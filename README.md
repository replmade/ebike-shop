# ebike-shop

Fictional electric bike store for a bug-fixing tutorial.

## Stack

- **Backend:** Django 5.2 + Django REST Framework + SQLite
- **Frontend:** React 18 + Vite 5 + React Router 6
- **Database:** SQLite (dev), PostgreSQL-compatible schema in `schema.sql`

## Quick Start

```bash
./setup.sh
```

Or manually:

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations api
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Admin: http://localhost:8000/admin/ (create superuser with `python manage.py createsuperuser`)

## Demo User

- Email: `demo@voltcycle.com`
- Password: `demo1234`

## Features

- Sign in / registration (token auth)
- Browse 3 ebike models with individual detail pages
- Browse replacement parts (batteries, chargers)
- Browse accessories (helmets, locks, racks)
- Shopping cart (add, update quantity, remove)
- Checkout with shipping form (no payment integration)