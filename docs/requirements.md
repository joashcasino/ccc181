# KopyaQ requirements

**Setting:** A small printing and photocopy shop near the MSU-IIT gate, Iligan City, busiest on weekday mornings before first classes
**People who wait:** MSU-IIT students who need documents printed, photocopied, bound or laminated (see Kyla in [docs/week3/personas.md](week3/personas.md))
**People who serve:** The shop owner-operator who runs the printers, copier and counter (see Ate Joy in [docs/week3/personas.md](week3/personas.md))

**Problem statement:** A student who needs a document printed before class needs a way to keep her place in line and know when it is her turn without crowding the counter, because the line has no clear order, people cut in, and she loses her spot whenever she steps out to buy food.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
|---|---|---|---|---|
| FR-01 | A customer can join the queue for a service by entering their name and email and choosing a service. | Must | **Yes** | Built (Week 3) |
| FR-02 | A customer can see their ticket number, status, and how many people are ahead of them, and the page updates by itself. | Must | **Yes** | Built (Week 3) |
| FR-03 ★ | A customer can enter the number of pages (1 to 1000) and mark the job as rush when joining. | Must | **Yes** | Built (Week 3) |
| FR-04 | A staff member can call the next waiting customer, and mark a called ticket as served or no-show. | Must | **Yes** | Built (Week 3) |
| FR-05 | A staff member can filter the dashboard by service. | Should | No | Built (Week 3) |
| FR-06 ★ | A staff member can see the estimated minutes of work waiting, computed from each ticket's pages and each service's minutes per page. | Should | **Yes** | Built (Week 3) |
| FR-07 | A customer can leave the queue before being served. | Must | **Yes** | Built (Week 3) |
| FR-08 | A staff member can add a service, change its name and minutes per page, and switch it off (for example, when the colored printer runs out of ink), and a switched-off service does not appear on the join form. | Must | **Yes** | This week |
| FR-09 ★ | A staff member can see which tickets are rush jobs, labelled on the dashboard. | Should | **Yes** | Built (Week 3) |
| FR-10 | A staff member can see the time each ticket joined on the dashboard, and a customer can see it on My place. | Should | **Yes** | This week |
| FR-11 | A staff member can delete a ticket that was created by mistake, after confirming. | Should | **Yes** | This week |
| FR-12 ★ | A staff member can mark a job as ready for pickup, and the customer sees "Ready for pickup" on My place. | Should | **Yes** | Later |
| FR-13 ★ | A customer can choose the paper size (Short, Long or A4) when joining. | Could | **Yes** | Later |
| FR-14 | A staff member can see how many customers left before being served, per service, per day. | Should | **Yes** | Later |
| FR-15 | A customer can switch the page to a larger text size. | Could | No | Later |
| FR-16 ★ | A staff member can mark each paper size (Short, Long, A4) as in stock or out of stock, and a customer can see which sizes are available before joining. | Should | **Yes** | Later |

FR-01 to FR-07 keep the IDs used in the Week 3 personas and report.

## Non-functional requirements

| ID | Requirement | Category | Priority |
|---|---|---|---|
| NFR-01 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two customers can never get the same ticket number, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | A customer can join the queue in under 60 seconds on a phone. | Usability | Should |
| NFR-04 | My place loads in under 2 seconds on slow prepaid mobile data. | Performance | Should |
| NFR-05 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-06 | No password or secret key is stored in the repository. | Security | Must |

## MVP

**MVP:** FR-01, FR-02, FR-03, FR-04, FR-07, FR-08, NFR-01, NFR-02, NFR-05, NFR-06.

This is the smallest version that still solves the problem: Kyla can join with her page count, step out, and come back when called, Ate Joy can serve people in the order they arrived, and the line survives a server restart so no one loses their place.

**Out of scope (Won't, this semester):**

- **Online payment (GCash or Maya):** customers pay in cash at the counter, and handling payments needs security work beyond this course.
- **Uploading files to print through the app:** students already hand over files by flash drive or Messenger, and storing their documents would raise privacy and storage problems.
- **SMS notifications:** each text costs money; My place already refreshes by itself.

## Feedback from the setting

| Who (role only, no full name) | What they said | What I changed |
|---|---|---|
| Student who prints near campus | "Maka indicate if naa pa bay stock for the different paper sizes, and if available ba si colored na option if magpa print kay what if hurot na ang ink." (Can the app show whether each paper size is still in stock, and whether colored printing is available, in case the ink has run out?) | Added FR-16 (Should): paper size stock shown to customers. Reworded FR-08 so switching off a service covers colored printing when the ink runs out. |
| Two more students who print near campus | Nothing missing and nothing wrong ("N/A" to both questions). | No change. |

**Most important features (3 students, 3 picks each):** FR-03 (pages and rush) was chosen by 2 of 3 students. FR-01, FR-02, FR-06, FR-07, FR-08, FR-10 and FR-13 were each chosen once. No one picked FR-04, FR-05, FR-09, FR-11, FR-12, FR-14 or FR-15. The staff-only features got few votes because all three respondents were students, so I kept them; a shop owner should check them in a later week.