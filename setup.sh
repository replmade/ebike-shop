#!/usr/bin/env bash
# ebike-shop — quick start script

set -e

echo "=== Setting up backend ==="
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations api
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser --noinput || true
echo ""
echo "=== Backend ready ==="
echo "Start backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo ""

echo "=== Setting up frontend ==="
cd ../frontend
npm install
echo ""
echo "=== Frontend ready ==="
echo "Start frontend:  cd frontend && npm run dev"
echo ""
echo "Backend: http://localhost:8000  (admin at /admin/)"
echo "Frontend: http://localhost:5173"