"""KopyaQ: a queue system for a printing and photocopy shop near MSU-IIT.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable

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
@app.route("/")
def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    pages = form.get("pages", type=int)
    rush = form.get("rush") == "yes"

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."
    if pages is None or not 1 <= pages <= 1000:
        errors["pages"] = "Enter the number of pages, from 1 to 1000."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "email": email,
                    "service_id": service_id, "pages": pages, "rush": rush,
                    "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


@app.route("/queue/<int:ticket_id>")


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
