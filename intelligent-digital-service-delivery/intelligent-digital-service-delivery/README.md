# Intelligent Digital Service Delivery

A simple base project: citizens submit service requests; the system automatically
classifies them (department + priority) and lets staff track status.

## Run
```bash
pip install -r requirements.txt
python app.py        # open http://127.0.0.1:5000
```

## Structure
- `app.py` – Flask REST API + SQLite storage
- `classifier.py` – rule-based smart routing/priority (swap for ML/LLM later)
- `templates/index.html` – submit form + live request dashboard

## API
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/requests | Create request (auto-classified) |
| GET | /api/requests | List, high priority first |
| GET | /api/requests/<id> | Single request |
| PATCH | /api/requests/<id> | Update status |
| GET | /api/stats | Counts by category/status/priority |

## Ideas to extend
User login, email/SMS notifications, ML or LLM classifier, SLA timers, admin roles.
