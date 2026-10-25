"""KopyaQ: a queue system for a printing and photocopy shop near MSU-IIT.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import math

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

def find_ticket(ticket_id):
    """Return the ticket with this number, or None."""
    return next((t for t in TICKETS if t["number"] == ticket_id), None)


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


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]

    # ★ FR-06: estimated work left, from pages and each service's speed
    per_page = {s["id"]: s["minutes_per_page"] for s in SERVICES}
    waiting = [t for t in queue if t["status"] == "waiting"]
    est_minutes = math.ceil(sum(t["pages"] * per_page[t["service_id"]] for t in waiting))

    names = {s["id"]: s["name"] for s in SERVICES}
    return render_template("staff.html", queue=queue, services=SERVICES, names=names,
                           selected=service_id, waiting_count=len(waiting),
                           est_minutes=est_minutes)


@app.post("/staff/call-next")
def call_next():
    service_id = request.form.get("service_id", type=int)
    waiting = [t for t in TICKETS if t["status"] == "waiting"
               and (not service_id or t["service_id"] == service_id)]
    if waiting:
        t = waiting[0]
        t["status"] = "called"
        flash(f"Called ticket #{t['number']} ({t['name']}).", "info")
    else:
        flash("No one is waiting.", "warning")
    return redirect(url_for("staff_dashboard", service_id=service_id))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = find_ticket(ticket_id)
    if t is None or new_status is None:
        abort(404)
    t["status"] = new_status
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard",
                            service_id=request.form.get("service_id", type=int)))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    ahead = sum(1 for x in TICKETS
                if x["service_id"] == t["service_id"]
                and x["status"] == "waiting" and x["number"] < t["number"])
    return {"status": t["status"], "ahead": ahead}


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    if t["status"] in ("waiting", "called"):
        t["status"] = "left"
        flash(f"You left the queue. Ticket #{ticket_id} is cancelled.", "info")
    return redirect(url_for("index"))


@app.route("/hello")

def hello():
    # The plain-string version from the Routes slide.
    return "Hello from KopyaQ!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
