# BizTrack (Django + HTMX)

Now includes:
- **Designer UI refresh** (Bootswatch + icons + sidebar layout)
- **Dashboard analytics** (charts using Chart.js)
- **User levels** via Groups + restricted views:
  - Employees: **My Attendance** + **My Expense Claims**
  - HR: attendance upload + month view
  - Finance: expense approve/paid + petty cash
  - Inventory: assets module

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Create default groups
python manage.py setup_roles

python manage.py runserver
```

### IMPORTANT: Link User ↔ Employee
For “My Attendance” to work:
Admin → Employees → set `user` field to the matching Django User.

## Employee flows
- Attendance: `Attendance` menu redirects employees to **My Attendance**
- Expenses: employees use **My Expense Claims** and submit claims (status auto set to Submitted)

## HR/Finance flows
- HR: Attendance Upload + Month view
- Finance: Expenses list (all), approve, mark paid; plus petty cash module
