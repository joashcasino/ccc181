# KopyaQ schema self-review (Week 4)

I put the ERD away for over an hour, then reviewed [schema.md](schema.md) and the [ERD](erd.png) against the six review questions, as if they were someone else's.

## 1. A double tap can put the same person in line twice

**Works well:** The `status` column has a CHECK that allows only the five statuses the app uses, and a default of `'waiting'`, so a new ticket can never start in a strange state.

**Problem:** Found with **question 4 (bad data)**. Kyla joins one-handed on a slow prepaid connection. If the page is slow and she taps *Get a ticket* twice, or joins again from a second tab, she gets two waiting tickets for the same service. The Week 3 double-submit guard is JavaScript, so it only works in the browser, and nothing in the schema stopped it. Ate Joy would call her twice and push everyone behind her back.

**Change:** Added a partial unique index `uq_tickets_one_active` on `tickets (user_id, service_id) WHERE status IN ('waiting', 'called')`. A customer can now have only one active ticket per service. Old tickets that are served, no-show or left do not count, so she can still join again next week. Added it to the constraints table in `schema.md`. The ERD is unchanged, because Chen notation has no symbol for a partial unique index. In Part 7, the join route must catch the `IntegrityError` and show "You already have a ticket for this service" instead of a generic error.

## 2. RESTRICT on users blocks a request to delete a customer's data

**Works well:** Both foreign keys use `ON DELETE RESTRICT`, so deleting a user or a service can never silently erase old tickets that FR-14 (who left before being served, per service, per day) needs.

**Problem:** Found with **question 5 (deletes)**. My requirements survey promised respondents they could ask to delete their data under the Data Privacy Act, and a KopyaQ customer could ask the same. With RESTRICT, a user who has tickets cannot be deleted at all. CASCADE would allow it, but it would also delete her tickets and break the shop's daily counts.

**Change:** Kept RESTRICT. If a customer asks to be removed, the staff will replace her name and email with placeholder values (for example "Deleted user" and `deleted-<id>@kopyaq.local`) instead of deleting the row. Her personal data is gone, but the anonymous tickets stay for FR-14. No column change was needed, because `email` is UNIQUE and the placeholder includes the id.

## 3. The role column had no requirement behind it

**Works well:** Splitting people into `users` removed the copies from Week 3, where every ticket repeated the customer's name and email. A person's email is now stored in one row (question 2, one fact in one place).

**Problem:** Found with **question 1 (coverage)**. `users.role` ('customer' or 'staff') is not used by any requirement in `docs/requirements.md`. FR-04 and FR-08 say "a staff member can", but nothing says only staff may do those things. Either the column was not needed, or a requirement was missing.

**Change:** The requirement was missing. Anyone who opens `/staff` today can call, serve or delete tickets, which is a real risk once the app runs in the shop. Added **FR-17 (Must, Later, Week 11):** *Only a signed-in staff member can open the staff dashboard and change tickets or services.* Kept the `role` column, because FR-17 needs it, and it is cheaper to have it now than to add it with a migration later.

## 4. No served time is stored

**Works well:** Every moment in time is a `timestamptz` set by the database (`created_at DEFAULT now()`, and `called_at` when Ate Joy calls), not text sent by the browser (question 6, types).

**Problem:** Found with **question 3 (facts, not results)**. When a ticket is marked served, the app keeps the status but not *when* it happened. That is a fact, and it is lost for good. Real served times would let the shop check whether each service's `minutes_per_page` (FR-06) is accurate.

**Change:** Kept the schema as it is. No requirement this week uses a served time, and the rule from question 1 is that every column must be there for a requirement. If a later week adds a requirement such as "a staff member can see the average time to serve a job, per service", I will add a nullable `served_at timestamptz` column with a new migration.