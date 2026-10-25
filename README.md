# KopyaQ

KopyaQ is a queue system for a printing and photocopy shop near MSU-IIT. Students join the line from their phone, see their place and estimated wait, and come back when called, while staff manage the line from a dashboard. The staff dashboard has no login yet; that comes in a later week. The staff dashboard has no login yet; that comes in a later week.


## How to run

```bash
py -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Then open http://127.0.0.1:5000

## Project structure

```
├── app.py              # routes and sample data (services, tickets)
├── requirements.txt
├── .gitignore
├── templates/          # Jinja2 pages
└── static/             # CSS and JavaScript
```

## Services

- Print (black and white)
- Print (colored)
- Photocopy
- Binding / lamination

Tickets are stored in a Python list for now. They move to PostgreSQL in Week 4.