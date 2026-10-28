# Doctor Appointment Booking System

Educational in-memory Python program for booking doctor appointments. A patient can view a doctor's available times, request a slot, and is limited to **N = 3** upcoming appointments. A doctor can accept or decline a pending request. Declined requests free the slot.

This is a software-engineering lab, not a production medical system.

**N is provisional (N = 3).** It was not found in the workspace or instructor files. Confirm it against the instructor's assigned team value before submission.

## Team

Replace the TBD values with the real team information. Do not invent IDs, names, or pull request links.

| Student ID | Student name | Branch | Pull request |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

Conflict Drill: UNCLAIMED

## GitHub Actions

The workflow in `.github/workflows/ci.yml` compiles the code, runs `python -m unittest -v`, and runs `python main.py` on pushes to any branch and on pull requests.

[![CI](https://github.com/m7md3bsalam/adv_siftware_task2/actions/workflows/ci.yml/badge.svg)](https://github.com/m7md3bsalam/adv_siftware_task2/actions/workflows/ci.yml)

The first GitHub Actions run will start after the initial push. All checks passed locally before publishing.

## How to run

Python 3.10+ is enough. There are **no third-party packages**.

`requirements.txt` lists the assignment requirements (R1–R7). It is **not** a pip file. Do not run `pip install -r requirements.txt`.

```bash
python main.py
python -m unittest -v
python -m py_compile main.py test_main.py
```

On this machine the working interpreter was `C:\msys64\ucrt64\bin\python.exe` because the `python` Store alias was not installed.

## Architecture and design

- `BookingSystem` is the in-memory controller.
- `Patient`, `Doctor`, `TimeSlot`, and `Appointment` are the domain objects.
- Appointment status is `PENDING`, `ACCEPTED`, or `DECLINED`.
- Availability is an offered slot whose start time is in the future and that is not occupied by a PENDING or ACCEPTED appointment.
- Upcoming appointments counted toward N are PENDING or ACCEPTED slots that start after the current clock.
- Design documents: `1_requirements.md`, `2_use_cases.md`, `3_candidate_classes.md`, `4_class_diagram.md`, `5_sequence_diagram.md`.

## Scope and limitations

- No database, web framework, or real login system.
- R5 is modeled with a private notes field and a simple role check. That is not hospital-grade security.
- R6 is checked on this small in-memory data set (under 2 seconds). It is not a production SLA.
- R7 is not implemented as a mobile UI. The program is a command-line demonstration.
- Docker is not included (required only for a five-member team when the assignment asks for it).

## Actual output of `python main.py`

Captured locally after a successful run:

```
Doctor Appointment Booking System — demonstration
Clock: 2026-10-28 09:00
N (max upcoming appointments per patient): 3
Doctor: Dr. Sara Ahmed (Family Medicine)

R1 — available slots for Dr. Sara Ahmed:
  - 2026-10-29 10:00–10:30
  - 2026-10-29 10:30–11:00
  - 2026-10-29 11:00–11:30
  - 2026-10-29 14:00–14:30

R2 — Omar books three available slots:
  A001: Omar Hassan with Dr. Sara Ahmed at 2026-10-29 10:00–10:30 [PENDING]
  A002: Omar Hassan with Dr. Sara Ahmed at 2026-10-29 10:30–11:00 [PENDING]
  A003: Omar Hassan with Dr. Sara Ahmed at 2026-10-29 11:00–11:30 [PENDING]
  Omar upcoming count: 3

R4 — Omar tries to book a fourth upcoming appointment:
  Rejected: A patient may have at most 3 upcoming appointments.

R2 — Lina tries to book Omar's occupied 10:00 slot:
  Rejected: That time slot is already booked.

R3 — doctor decisions:
  Accepted A001: Omar Hassan with Dr. Sara Ahmed at 2026-10-29 10:00–10:30 [ACCEPTED]
  Declined A002: Omar Hassan with Dr. Sara Ahmed at 2026-10-29 10:30–11:00 [DECLINED]
  Omar upcoming count after decline: 2

Available slots after the decline (10:30 should be free):
  - 2026-10-29 10:30–11:00
  - 2026-10-29 14:00–14:30

R2 — Lina books the freed 10:30 slot:
  A004: Lina Nasser with Dr. Sara Ahmed at 2026-10-29 10:30–11:00 [PENDING]

R5 — educational privacy check (medical notes are not printed in this demo):
  Unauthorized requester was denied access to medical notes.
  Authorized staff can retrieve notes (36 characters). Contents not displayed.

Final appointments:
  A001: Omar Hassan with Dr. Sara Ahmed at 2026-10-29 10:00–10:30 [ACCEPTED]
  A002: Omar Hassan with Dr. Sara Ahmed at 2026-10-29 10:30–11:00 [DECLINED]
  A003: Omar Hassan with Dr. Sara Ahmed at 2026-10-29 11:00–11:30 [PENDING]
  A004: Lina Nasser with Dr. Sara Ahmed at 2026-10-29 10:30–11:00 [PENDING]

Demo finished. Pending and accepted future appointments occupy slots.
Declined appointments do not occupy slots and do not count toward N.
```

## Team GitHub workflow (must be done by real team members)

The assignment expects each member to use their own branch and pull request, review a teammate's PR with a real comment, and complete a Conflict Drill. Those steps are **not** simulated here.

1. Confirm N with the instructor if needed.
2. Fill in the team table with real student IDs, names, branches, and PR links.
3. Create a public GitHub repository (suggested name: `doctor-appointment-booking-system`).
4. Push this project.
5. Each member opens their own branch and pull request.
6. Each member leaves a real review comment on a teammate's PR.
7. Complete the Conflict Drill with real PRs, then replace `UNCLAIMED` with the participating names.
