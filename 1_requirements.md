# Requirements

This document preserves the original requirement wording and IDs for the Doctor Appointment Booking System.

**N = 3 is confirmed by the instructor.** The same confirmed value is used in the design, `main.py`, tests, and README.

## Functional requirements

### R1
A patient can view the days and times when a doctor is available.

Acceptance notes (do not change R1): the system returns the doctor's offered future slots that are not occupied by a PENDING or ACCEPTED appointment.

### R2
A patient can book an appointment during an available time slot.

Acceptance notes: booking an offered, future, unoccupied slot creates a PENDING appointment request. Unoffered, past, or occupied slots are rejected.

### R3
A doctor can accept or decline an appointment request.

Acceptance notes: only the assigned doctor may decide, and only while the appointment is PENDING. ACCEPTED keeps the slot occupied. DECLINED frees the slot.

### R4
A patient can have at most N upcoming appointments at any given time.

Acceptance notes: **N = 3** (confirmed by the instructor). Upcoming means PENDING or ACCEPTED with a slot start time strictly after the current clock. DECLINED and past appointments do not count.

## Non-functional requirements

### R5
Patient medical data shall be accessible only to authorized staff.

Educational scope: medical notes are stored privately on the patient object and are not printed in the demonstration. A simple role string check (`authorized_staff`) models the idea of authorization. This in-memory program is **not** a real authentication, encryption, or hospital access-control system.

### R6
Available appointment times shall be displayed within 2 seconds.

Educational scope: availability is computed from in-memory lists. A unit test checks that this lookup finishes in under 2 seconds on the demonstration data set. That check is not a measured production SLA.

### R7
The application shall be usable on mobile phone screens.

Educational scope: the submitted program is a command-line Python demonstration, not a mobile or responsive web UI. A production product would need a mobile-friendly interface. This limitation is documented rather than pretended to be fully implemented.
