# AI Journal

This journal records the actual assistance, reviews, commands, and results from this implementation session. No team-member checks, GitHub Actions results, pull requests, or human reviews are claimed unless they happened.

## What AI assistance was used for

Cursor Grok 4.6 was used in this workspace to:

- inspect the empty folder and toolchain
- choose a beginner-friendly in-memory design
- write the required Markdown deliverables, `main.py`, `test_main.py`, `.gitignore`, and a CI workflow
- run local compile/tests/demo
- initialize Git when possible

No official starter template was used. The instructor stated that no template is required.

## Repository inspection

- The workspace `advsoft_task` contained no project files.
- It was not a Git repository.
- At initial implementation, no assigned value of N was found, so **N = 3** was documented as provisional. It was subsequently confirmed with the instructor, as noted under Remaining limitations.
- `python` (Microsoft Store alias) was not installed. `C:\msys64\ucrt64\bin\python.exe` reported **Python 3.14.8**.
- Git **2.45.1** was available.
- `gh` was not installed. The Cursor origin MCP namespace was in an error state, and `mcp_auth` did not complete within 30 seconds, so no GitHub repository was created from this session.
- `git init -b main` succeeded. The first `git commit` failed because `user.name` and `user.email` are not set. Git config was not changed (assignment rule). A later local commit used a one-off `git -c` identity so the work could be recorded without writing `~/.gitconfig`.

## Reviews after each stage

### After writing `main.py` and `test_main.py`

Checked that class names, statuses, N, occupancy, and upcoming-count rules matched the planned documents. No mistake was observed in that review.

### After writing requirements, use cases, candidate classes, and diagrams

Traced R1–R7 through UC1–UC4, the class table, the class diagram, the sequence diagram, and the Python methods. Confirmed:

- R1–R7 IDs are preserved.
- N = 3 is used in requirements, use cases, diagrams, code, and tests.
- Sequence diagram `alt/else` paths match `BookingError` and status transitions.
- Failed validation does not create an appointment.

No mistake was observed in that review.

### After running automated checks

Commands and results are listed below. All three local checks succeeded. No failing test was observed, so no test-failure correction was required.

### AI-generated mistakes discovered

No AI-generated functional mistake was found during the reviews and local runs in this session. This journal does not invent mistakes.

One documentation caution remains: `requirements.txt` contains the assignment requirements (as requested) and is **not** a pip dependency file. That is intentional, not a silent bug.

## Requirements and design decisions that were checked

- Functional: R1 view availability, R2 book slot, R3 accept/decline, R4 limit N = 3.
- Upcoming policy: PENDING and ACCEPTED with `slot.start > now`.
- DECLINED frees the slot and does not count toward N.
- Past slots cannot be booked; past PENDING/ACCEPTED do not count as upcoming.
- Duplicate occupancy of the same doctor slot is rejected.
- R5: demo does not print medical note contents; unauthorized role is denied.
- R6: unit test asserts availability lookup duration &lt; 2 seconds on sample data.
- R7: documented as a CLI limitation, not a fake mobile app.

## Diagram consistency

- Use case actors: Patient, Doctor.
- Classes in the class diagram exist in `main.py` with the same responsibilities.
- Sequence diagram participants are Patient, BookingSystem, and Doctor, with TimeSlot/Appointment behavior inside the system.
- Accept/decline happens after a successful PENDING booking, not after a rejected booking.

## Tests that were run (actual results)

Working directory: `c:\Users\mohammed\OneDrive\Desktop\advsoft_task`  
Interpreter: `C:\msys64\ucrt64\bin\python.exe`

1. `python --version` → **Python 3.14.8**
2. `python -m py_compile main.py test_main.py` → **exit code 0**
3. `python -m unittest -v` → **12 tests, OK, 0.001s, exit code 0**
4. `python main.py` → **exit code 0**, output captured below

GitHub Actions was **not** verified (no remote yet). No pull request URL exists yet.

## Remaining limitations

- N = 3 was subsequently confirmed with the instructor; the requirements, use cases, implementation, and README now record that confirmation.
- Team branches and PRs were subsequently created and merged: Mohammed's [PR #1](https://github.com/m7md3bsalam/adv_siftware_task2/pull/1) and Sayed's [PR #2](https://github.com/m7md3bsalam/adv_siftware_task2/pull/2). Sayed reviewed PR #1, and Mohammed left a comment on PR #2.
- The real two-person Conflict Drill is not yet complete. Mohammed's local README draft is on `conflict-drill-mohammed`; Sayed's independent conflicting edit and joint resolution remain outstanding.
- GitHub Actions was subsequently verified: the latest recorded run on `main` after Sayed's merge succeeded.
- R5, R6, and R7 are only partly demonstrated in an educational CLI program.

## Actual output of `python main.py`

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
