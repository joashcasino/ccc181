# Week 3 Self-Review: KopyaQ Wireframes

I reviewed each screen at both phone and laptop width against my two personas, Kyla (student waiting) and Ate Joy (shop owner), and their "Because …, my interface must …" rules.

---

## 1. Join the queue

> **Works well:** The form is one short column with labels above each field and one full-width "Get a ticket" button at the bottom. Kyla can see what to do in under 5 seconds, which follows her rule 4 (the form must be short).
>
> **Problem:** On the phone, I first placed Service and Pages side by side. The dropdown was too narrow, so "Choose a service" was cut off, and the arrow sat on the left where people do not expect it. The Pages placeholder "e.g. 1 - 2" also looked like a range, when the field takes one number. These break **match with the real world** and **error prevention**: Kyla could misread what to enter.
>
> **Change:** Stacked Service and Pages full width on the phone, moved the dropdown arrow to the right, renamed "Services:" to "Service:", and changed the placeholder to "e.g. 25". On the laptop, I made all inputs the same width and 40 px tall so they are easy to read and click.

---

## 2. My place

> **Works well:** The ticket number (#14) is the largest element on the card, and the status is written as a word ("Waiting") inside a badge, not shown only by color.
>
> **Problem:** In the first version, "6 people ahead of you" was the smallest text on the card, even though Kyla's rule 1 says the number *and* position must be the biggest things on the screen. The "Leave the queue" button was solid black and attached to the bottom of the card, which made it look like the main action. Kyla could tap it by accident while walking. These break **visibility of system status** and **error prevention**.
>
> **Change:** Made the position large and bold and moved it directly under the ticket number, with the status right below it. Changed "Leave the queue" to an outlined button, moved it outside the card, and added a 24 px gap. Added a small "Updates automatically" note so Kyla knows she does not need to refresh (her rule 3).
>
> **Known problem I am keeping for now:** If Kyla closes the tab, she has no easy way back to her ticket without remembering her number and typing `/queue/14`. This breaks **recognition rather than recall**. I am keeping it this week because the app has no sessions yet. Later, I will remember her ticket in the browser and show a "My ticket #14" link in the navbar after she joins.

---

## 3. Staff dashboard

> **Works well:** "Call Next" is the largest button and sits at the top of the screen, so Ate Joy can press it quickly with paper in her hands (her rule 1). Rush tickets have a clear "RUSH" label (her rule 4), and every status is written in words (her rule 2).
>
> **Problem:** In the first draft, every row was identical, the Actions column was empty, and no filter looked selected, so Ate Joy could not tell which service she was viewing. On the phone, a six-column table with buttons does not fit in 402 px. On the laptop, the navbar underlined "Join the queue" instead of "Staff". These break **visibility of system status** and **consistency**.
>
> **Change:** Added Serve and No-show buttons to every row, used realistic tickets with different services and one rush job, and showed the "All" filter as selected. On the phone, the table scrolls sideways inside its own box with a "Scroll sideways for actions" hint, instead of breaking the page. On the laptop, the table uses the full width with larger text for reading at arm's length, and the navbar now underlines "Staff".

---

## Scope decision found during review

While reviewing Kyla's scenario, I noticed the app has no step for sending the file to print. In real print shops near campus, students hand over a flash drive or send the file through Messenger at the counter. KopyaQ manages the line, not the files. I added **file upload** as a *Won't have (this time)* requirement, because storing students' documents would add privacy risk under RA 10173 and is outside the MVP.
