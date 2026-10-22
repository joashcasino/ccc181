# KopyaQ Personas

> \*\*Note on sources:\*\* For this activity our professor told us to skip the interview phase. Details marked \*(assumption)\* are based on my own experience as an MSU-IIT student who uses print shops near campus, not on formal interviews.

\---

## Kyla, the person waiting

> "I don't mind waiting. I just want to know if I still have time to buy lunch before it's my turn." \*(assumption)\*

|||
|-|-|
|**Photo or sketch**|Simple icon of a student with a backpack and a folder (no real person)|
|**Age, role and background**|20, 3rd-year engineering student at MSU-IIT, lives in a boarding house near campus, has back-to-back classes most days *(assumption)*|
|**Goals**|Print her lab report before her 10 AM class; know exactly when it is her turn; keep her place in line even if she steps out *(assumption)*|
|**Frustrations**|The line spills out the door with no clear order; people cut in by shouting at the counter; she cannot tell how long the wait is, so she sometimes leaves and loses her spot *(assumption)*|
|**Devices and context**|Budget Android phone on prepaid data, often low on battery; uses it one-handed while holding a folder or walking between buildings *(assumption)*|
|**Tech comfort**|High. Uses social media and school portals daily, but her mobile data is limited and slow|
|**Accessibility needs**|One hand busy, screen glare outdoors, slow mobile data|

### Scenario

It is 9:20 AM and Kyla has a lab report due at 10:00. She arrives at the print shop near the campus gate and sees about ten students crowding the counter. She scans the QR code on the door, picks "Print (black and white)," enters 25 pages, and gets ticket #14. The screen says 6 people are ahead of her. She walks to the carinderia next door to buy bread, checking her phone while she waits in line there. When the status changes to *Called*, she walks back, picks up her printout, and makes it to class on time.

### Top tasks in the app

|Task|Screen|Requirement ID|
|-|-|-|
|Join the queue for a black-and-white print|Join|FR-01|
|Enter page count and mark the job as rush|Join|FR-03|
|Check her number and how many are ahead|My place|FR-02|
|Leave the queue if she runs out of time|My place|FR-07|

### What this means for my interface

1. Because Kyla checks her phone one-handed while walking, her ticket number and position must be the biggest things on My place.
2. Because her prepaid data is slow, pages must load fast and use no large images.
3. Because she steps out of the shop while waiting, the status must update by itself without her refreshing.
4. Because she is in a hurry at the door, the join form must be short: name, email, service, pages, and rush only.

\---

## Ate Joy, the staff member

> "Everyone says 'Ate, ako na!' and I can't remember who came first." \*(assumption)\*

|||
|-|-|
|**Photo or sketch**|Simple icon of a shop counter with a printer (no real person)|
|**Age, role and background**|38, owner-operator of a small print and photocopy shop near the MSU-IIT gate; runs two printers and one copier with one helper *(assumption)*|
|**Goals**|Serve customers in the right order without arguments; group similar jobs so the printers keep running; know how much work is waiting *(assumption)*|
|**Frustrations**|Students crowd the counter and talk at the same time; she forgets who arrived first; large rush jobs arrive during peak hours and slow everyone down *(assumption)*|
|**Devices and context**|Shared shop desktop beside the printer; usually standing, hands full of paper, machines running loudly, constant interruptions *(assumption)*|
|**Tech comfort**|Medium. Comfortable with Facebook, Messenger and Word, but not used to admin dashboards|
|**Accessibility needs**|Reads the screen while standing at arm's length; noisy room, so sound alerts are useless; often interrupted mid-task|

### Scenario

It is 7:45 AM on a Monday, the busiest time before first classes. Ate Joy has the KopyaQ dashboard open on the shop desktop. Twelve tickets are waiting. She filters to "Binding / lamination" to see how many binding jobs are lined up, then switches back to all services. When the printer finishes a job, she hands the papers over, clicks *Serve* on that row, and presses *Call next*. The next student's phone shows *Called* and they walk up to the counter. A student who joined earlier never shows up, so she marks them *No-show* and moves on.

### Top tasks in the app

|Task|Screen|Requirement ID|
|-|-|-|
|Call the next customer|Staff dashboard|FR-04|
|Mark a ticket as served or no-show|Staff dashboard|FR-04|
|Filter the list by service|Staff dashboard|FR-05|
|See the estimated wait based on pages ahead|Staff dashboard|FR-06|

### What this means for my interface

1. Because Ate Joy is usually holding paper and gets interrupted, *Call next* must be one large button at the top of the dashboard.
2. Because she reads the screen standing at arm's length, the table text must be large and each status must be written in words, not shown only by color.
3. Because the shop is noisy, every change must be shown on screen, not signaled with sound.
4. Because rush jobs affect everyone's wait, rush tickets must be clearly labeled in the table.

