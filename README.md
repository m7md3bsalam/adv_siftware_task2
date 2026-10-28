# Doctor Appointment Booking System

Educational in-memory Python program for booking doctor appointments. A patient can view a doctor's available times, request a slot, and is limited to **N = 3** upcoming appointments. A doctor can accept or decline a pending request. Declined requests free the slot.

This is a software-engineering lab, not a production medical system.

**N = 3 is confirmed by the instructor.**

## Team

| Student ID | Student name | Branch | Pull request |
| --- | --- | --- | --- |
| 20240256 | Sayed Mamdouh | `sayed` | [#2](https://github.com/m7md3bsalam/adv_siftware_task2/pull/2) |
| 20242296 | Mohammed Abdelsalam | `mohammed` | [#1](https://github.com/m7md3bsalam/adv_siftware_task2/pull/1) |

Peer-review comments have been exchanged: Sayed reviewed [PR #1](https://github.com/m7md3bsalam/adv_siftware_task2/pull/1), and Mohammed commented on [PR #2](https://github.com/m7md3bsalam/adv_siftware_task2/pull/2).

Conflict Drill: **COMPLETE** — Performed and resolved jointly by Sayed Mamdouh (`sayed-conflict-drill`, [PR #3](https://github.com/m7md3bsalam/adv_siftware_task2/pull/3)) and Mohammed Abdelsalam (`conflict-drill-mohammed`, [PR #4](https://github.com/m7md3bsalam/adv_siftware_task2/pull/4)). Both team members pushed independent conflicting branches that edited the Conflict Drill status line in README.md alongside confirming N = 3; PR #3 was merged into `main`, creating a real merge conflict on PR #4. The team resolved the conflict collaboratively, preserving the confirmed N = 3 documentation across all project artifacts.

## GitHub Actions

The workflow in `.github/workflows/ci.yml` compiles the code, runs `python -m unittest -v`, and runs `python main.py` on pushes to any branch and on pull requests.

[![CI](https://github.com/m7md3bsalam/adv_siftware_task2/actions/workflows/ci.yml/badge.svg)](https://github.com/m7md3bsalam/adv_siftware_task2/actions/workflows/ci.yml)

The latest recorded GitHub Actions run on `main` after Sayed's merge passed.

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

The team PRs, peer-review activity, and Conflict Drill are recorded above.

1. N = 3 was confirmed by the instructor across requirements, use cases, implementation, and README.
2. Both team members opened branches and merged pull requests, linked in the team table above: Mohammed's [PR #1](https://github.com/m7md3bsalam/adv_siftware_task2/pull/1) and Sayed's [PR #2](https://github.com/m7md3bsalam/adv_siftware_task2/pull/2).
3. Both team members exchanged real review comments: Sayed reviewed PR #1, and Mohammed reviewed PR #2.
4. The Conflict Drill is COMPLETE: Sayed opened [PR #3](https://github.com/m7md3bsalam/adv_siftware_task2/pull/3) and Mohammed opened [PR #4](https://github.com/m7md3bsalam/adv_siftware_task2/pull/4) with conflicting edits. PR #3 was merged into `main`, the real merge conflict was reproduced on `conflict-drill-mohammed`, and resolved collaboratively by both team members.
