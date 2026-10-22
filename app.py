"""KopyaQ: a queue system for a printing and photocopy shop near MSU-IIT.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, render_template

app = Flask(__name__)

# Sample data. Week 4 moves this into PostgreSQL.
SERVICES = [
    {"id": 1, "name": "Print (black and white)", "minutes_per_page": 0.2},
    {"id": 2, "name": "Print (colored)", "minutes_per_page": 0.5},
    {"id": 3, "name": "Photocopy", "minutes_per_page": 0.1},
    {"id": 4, "name": "Binding / lamination", "minutes_per_page": 3},
]

# Each ticket: number, name, email, service_id, pages, rush, status
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Ana", "email": "ana@g.msuiit.edu.ph", "service_id": 1,
     "pages": 25, "rush": False, "status": "waiting"},
    {"number": 2, "name": "Ben", "email": "ben@g.msuiit.edu.ph", "service_id": 2,
     "pages": 4, "rush": True, "status": "waiting"},
    {"number": 3, "name": "Cara", "email": "cara@g.msuiit.edu.ph", "service_id": 4,
     "pages": 1, "rush": False, "status": "waiting"},
]


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana",
                           tickets=[t["number"] for t in TICKETS])


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    return render_template("ticket.html", ticket_id=ticket_id)


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello from KopyaQ!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
