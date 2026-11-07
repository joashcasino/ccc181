# KopyaQ validation (Week 4, Part 10)

KopyaQ checks the same rules in three layers. The browser gives quick feedback, Flask is the real gatekeeper, and PostgreSQL is the last line of defense. Every test below skips at least one layer on purpose.

## Browser layer

The join form (`templates/join.html`) matches the columns in `models.py`:

| Field | Attributes | Column it matches |
|---|---|---|
| Name | `required maxlength="80"` | `users.name varchar(80) NOT NULL` |
| Email | `type="email" required maxlength="120"` | `users.email varchar(120) NOT NULL` |
| Service | `required` | `tickets.service_id NOT NULL` |
| Pages | `type="number" min="1" max="1000" required` | `tickets.pages`, `ck_tickets_pages` |

The Manage services form (`templates/services.html`) uses `maxlength="60"` for the name and `min="0.01" max="999.99" step="0.01"` for minutes per page, matching `varchar(60)` and `numeric(5,2)` with `ck_services_minutes_per_page`.

These attributes only help honest users. curl skips them completely, which is what the Flask tests below do.

## Results

The ticket count was 5 before and 5 after each set of Flask tests, so no bad request saved anything (except the one before the fix in row 3).

| Rule | Layer | How I tested it | What happened |
|---|---|---|---|
| Name is required, email must contain @, service must exist | Flask | `curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=" -d "email=not-an-email" -d "service_id=999" -d "pages=5"` | `HTTP/1.1 400 BAD REQUEST`. The form came back with "Enter your name.", "Enter a valid email address." and "Choose a service." Ticket count stayed 5. |
| Name is at most 80 characters | Flask | Same request with a 200-character name (`$long = "a" * 200`, then `-d "name=$long"`) | `HTTP/1.1 400 BAD REQUEST` with "Your name must be 80 characters or fewer." Ticket count stayed 5. |
| A switched-off service cannot be joined (FR-08) | Flask | Switched off Print (colored) (`active = f`), then `curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "email=test@g.msuiit.edu.ph" -d "service_id=2" -d "pages=5"` | **Before the fix:** `HTTP/1.1 302 FOUND` and ticket #15 was saved. The service was hidden from the dropdown, but `join()` only checked `service is None`. **After adding `or not service.active`:** `HTTP/1.1 400 BAD REQUEST` with "Choose a service." Ticket count stayed 5. |
| Pages must be 1 to 1000 | Flask | `curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "email=test@g.msuiit.edu.ph" -d "service_id=1" -d "pages=5000"` | `HTTP/1.1 400 BAD REQUEST` with "Enter the number of pages, from 1 to 1000." This request saved nothing. |
| A ticket's service must exist | Database (FOREIGN KEY) | `INSERT INTO tickets (user_id, service_id, pages) VALUES (1, 999, 5);` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` / `DETAIL: Key (service_id)=(999) is not present in table "services".` |
| A ticket must have a page count | Database (NOT NULL) | `INSERT INTO tickets (user_id, service_id) VALUES (1, 1);` | `ERROR: null value in column "pages" of relation "tickets" violates not-null constraint` |
| Status is one of the five allowed values | Database (CHECK) | `UPDATE tickets SET status = 'lost' WHERE id = 6;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Pages must be 1 to 1000 | Database (CHECK) | `UPDATE tickets SET pages = 0 WHERE id = 6;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_pages"` |
| Minutes per page must be more than 0 | Database (CHECK) | `INSERT INTO services (name, minutes_per_page) VALUES ('Test', 0);` | `ERROR: new row for relation "services" violates check constraint "ck_services_minutes_per_page"` |
| Emails are stored in lowercase | Database (CHECK) | `INSERT INTO users (name, email) VALUES ('Shout', 'SHOUT@G.MSUIIT.EDU.PH');` | `ERROR: new row for relation "users" violates check constraint "ck_users_email_lowercase"` |
| One account per email | Database (UNIQUE) | `INSERT INTO users (name, email) VALUES ('Copy', 'ana@g.msuiit.edu.ph');` | `ERROR: duplicate key value violates unique constraint "users_email_key"` / `DETAIL: Key (email)=(ana@g.msuiit.edu.ph) already exists.` |
| A service with tickets cannot be deleted | Database (RESTRICT) | `DELETE FROM services WHERE id = 1;` | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` / `DETAIL: Key (id)=(1) is still referenced from table "tickets".` |
| One active ticket per customer per service (Part 3 self-review) | Database (partial UNIQUE index) | Ran `INSERT INTO tickets (user_id, service_id, pages) VALUES (4, 1, 5);` twice | The first insert worked (`INSERT 0 1`). The second failed: `ERROR: duplicate key value violates unique constraint "uq_tickets_one_active"` / `DETAIL: Key (user_id, service_id)=(4, 1) already exists.` |

## A good row and its defaults

```sql
INSERT INTO tickets (user_id, service_id, pages) VALUES (4, 3, 5) RETURNING id, status, is_rush, created_at;
```

```
 id | status  | is_rush |          created_at
----+---------+---------+------------------------------
 14 | waiting | f       | 2026-11-07 13:01:50.50643+00
```

The insert gave only three values. PostgreSQL filled in the rest: `status` defaulted to `waiting`, `is_rush` to `false`, and `created_at` to `now()`. The time is stored in UTC; it is 9:01 PM in Philippine time.

## No SQL in f-strings

```
git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"
```

Result: [run this in Git Bash and record the result here; it should print nothing]

All queries are built with `db.select(...)`, `db.session.get(...)` and `db.get_or_404(...)`, so SQLAlchemy sends user input separately from the SQL.

## What I learned

The most useful finding was row 3. Hiding a switched-off service from the dropdown looked like enough, but a hand-made request could still join it, and test 3 saved ticket #15. Only the server-side check (`or not service.active`) actually enforces FR-08. The browser layer is for convenience, not protection.