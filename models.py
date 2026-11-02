from datetime import datetime
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, false, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    role: Mapped[str] = mapped_column(String(20), default="customer", server_default="customer")

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="ck_users_name_not_blank"),
        CheckConstraint("email = lower(email)", name="ck_users_email_lowercase"),
        CheckConstraint("role IN ('customer', 'staff')", name="ck_users_role"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    minutes_per_page: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=1, server_default="1")

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint("minutes_per_page > 0", name="ck_services_minutes_per_page"),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="RESTRICT"))
    pages: Mapped[int]
    is_rush: Mapped[bool] = mapped_column(default=False, server_default=false())
    status: Mapped[str] = mapped_column(String(20), default="waiting", server_default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint("pages BETWEEN 1 AND 1000", name="ck_tickets_pages"),
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
        # Part 3 self-review, entry 1: one active ticket per customer per service
        Index(
            "uq_tickets_one_active",
            "user_id",
            "service_id",
            unique=True,
            postgresql_where=text("status IN ('waiting', 'called')"),
        ),
    )