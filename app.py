"""KopyaQ: a queue system for a printing and photocopy shop near MSU-IIT.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import math
import os
from datetime import timedelta, timezone
from decimal import Decimal, InvalidOperation

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Service, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

PH_TIME = timezone(timedelta(hours=8))

@app.template_filter("local")
def local_time(value):
    """Show a UTC time from the database in Philippine time, e.g. Oct 26, 08:01 AM."""
    if not value:
        return ""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p")


SEED_SERVICES = [
    ("Print (black and white)", "0.2"),
    ("Print (colored)", "0.5"),
    ("Photocopy", "0.1"),
    ("Binding / lamination", "3"),
]


@app.cli.command("seed")
def seed():
    """Add the shop's services. Safe to run more than once."""
    added = 0
    for name, minutes in SEED_SERVICES:
        exists = db.session.scalar(db.select(Service).where(Service.name == name))
        if exists is None:
            db.session.add(Service(name=name, minutes_per_page=Decimal(minutes)))
            added += 1
    db.session.commit()
    print(f"Seed done: {added} added, {len(SEED_SERVICES) - added} already there.")

def all_services():
    """Every service, A to Z. Used by the join form and the staff pages."""
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()


def active_services():
    """Services customers can join right now, A to Z (FR-08)."""
    return db.session.scalars(
        db.select(Service).where(Service.active.is_(True)).order_by(Service.name)
    ).all()


def people_ahead(t):
    """How many tickets for the same service are waiting and joined before t."""
    return db.session.scalar(
        db.select(func.count(Ticket.id)).where(
            Ticket.service_id == t.service_id,
            Ticket.status == "waiting",
            Ticket.created_at < t.created_at,
        )
    )


@app.route("/")

def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    return render_template("join.html", services=active_services(), form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    pages = form.get("pages", type=int)
    is_rush = form.get("rush") == "yes"
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    elif len(name) > 80:
        errors["name"] = "Your name must be 80 characters or fewer."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    elif len(email) > 120:
        errors["email"] = "Your email must be 120 characters or fewer."
    if service is None or not service.active:
        errors["service_id"] = "Choose a service."
    if pages is None or not 1 <= pages <= 1000:
        errors["pages"] = "Enter the number of pages, from 1 to 1000."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=active_services(), form=form, errors=errors), 400

    # A returning student reuses her account and gets a new ticket
    user = db.session.scalar(db.select(User).filter_by(email=email))
    if user is None:
        user = User(name=name, email=email)

    ticket = Ticket(user=user, service=service, pages=pages, is_rush=is_rush)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("You already have a ticket for this service. Check My place instead of joining again.",
              "warning")
        return render_template("join.html", services=active_services(), form=form, errors={}), 409

    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    query = (
        db.select(Ticket)
        .where(Ticket.status.in_(["waiting", "called"]))
        .order_by(Ticket.created_at)
    )
    if service_id:
        query = query.where(Ticket.service_id == service_id)
    queue = db.session.scalars(query).all()

    # ★ FR-06: estimated work left, computed from pages and each service's speed, never stored
    waiting = [t for t in queue if t.status == "waiting"]
    est_minutes = math.ceil(sum(t.pages * t.service.minutes_per_page for t in waiting))

    services = all_services()
    names = {s.id: s.name for s in services}
    return render_template("staff.html", queue=queue, services=services, names=names,
                           selected=service_id, waiting_count=len(waiting),
                           est_minutes=est_minutes)


@app.post("/staff/call-next")
def call_next():
    service_id = request.form.get("service_id", type=int)
    # Week 3 usability test: don't call another student for a service while
    # someone for that service is still at the counter
    busy = db.select(Ticket.service_id).where(Ticket.status == "called")
    query = (
        db.select(Ticket)
        .where(Ticket.status == "waiting", Ticket.service_id.not_in(busy))
        .order_by(Ticket.created_at)
        .limit(1)
    )
    if service_id:
        query = query.where(Ticket.service_id == service_id)
    t = db.session.scalar(query)
    if t is None:
        flash("No one can be called right now. Either no one is waiting, or the person "
              "already called must be served or marked no-show first.", "warning")
    else:
        t.status = "called"
        t.called_at = func.now()
        db.session.commit()
        flash(f"Called ticket #{t.id} ({t.user.name}).", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))

ACTIONS = {"call": "called", "serve": "served", "no-show": "no-show"}
ALLOWED_FROM = {
    "call": ("waiting",),
    "serve": ("waiting", "called"),
    "no-show": ("waiting", "called"),
}


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = ACTIONS.get(action)
    if new_status is None:
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)
    if t.status not in ALLOWED_FROM[action]:
        flash(f"Ticket #{t.id} is already {t.status}.", "warning")
    else:
        t.status = new_status
        if new_status == "called":
            t.called_at = func.now()
        db.session.commit()
        flash(f"Ticket #{t.id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard",
                            service_id=request.form.get("service_id", type=int)))

@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard",
                            service_id=request.form.get("service_id", type=int)))


def read_service_form(form):
    """Clean and check the Manage services form. Returns (name, minutes, error)."""
    name = form.get("name", "").strip()
    try:
        minutes = Decimal(form.get("minutes_per_page", "").strip()).quantize(Decimal("0.01"))
    except InvalidOperation:
        minutes = None
    if not name or len(name) > 60:
        return name, minutes, "Enter a service name of up to 60 characters."
    if minutes is None or minutes.is_nan() or not 0 < minutes < 1000:
        return name, minutes, "Minutes per page must be a number from 0.01 to 999.99."
    return name, minutes, None


@app.get("/staff/services")
def services_list():
    return render_template("services.html", services=all_services())


@app.post("/staff/services")
def service_create():
    name, minutes, error = read_service_form(request.form)
    if error:
        flash(error, "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name, minutes_per_page=minutes))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(f'A service named "{name}" already exists.', "danger")
        return redirect(url_for("services_list"))
    flash(f"Added {name}.", "success")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/edit")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    name, minutes, error = read_service_form(request.form)
    if error:
        flash(error, "danger")
        return redirect(url_for("services_list"))
    s.name = name
    s.minutes_per_page = minutes
    s.active = request.form.get("active") == "on"  # an unticked box is not sent at all
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(f'A service named "{name}" already exists.', "danger")
        return redirect(url_for("services_list"))
    flash(f"Saved {name}.", "success")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    name = s.name
    if s.tickets:
        flash(f"{name} has {len(s.tickets)} ticket(s), so it can't be deleted. "
              "Switch it off instead to hide it from the join form.", "danger")
        return redirect(url_for("services_list"))
    db.session.delete(s)
    db.session.commit()
    flash(f"Deleted {name}.", "warning")
    return redirect(url_for("services_list"))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template("ticket.html", ticket=t, service=t.service, ahead=people_ahead(t))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return {"status": t.status, "ahead": people_ahead(t)}


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.status == "waiting":
        t.status = "left"  # soft delete: the row stays for FR-14 reports
        db.session.commit()
    flash("You left the queue.", "info")
    return redirect(url_for("index"))


@app.route("/hello")

def hello():
    # The plain-string version from the Routes slide.
    return "Hello from KopyaQ!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
