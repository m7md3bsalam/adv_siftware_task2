# Class Diagram

The diagram matches `3_candidate_classes.md` and `main.py`.

**N = 3** is stored as `BookingSystem.max_upcoming` (default `MAX_UPCOMING_APPOINTMENTS`).

Slot occupancy and the upcoming count use `Appointment.occupies_slot()` and `Appointment.counts_as_upcoming(now)`:

- PENDING and ACCEPTED occupy a slot.
- Only PENDING or ACCEPTED appointments whose slot start is after `now` count toward N.
- DECLINED frees the slot and does not count toward N.

```mermaid
classDiagram
    class Patient {
        +str patient_id
        +str name
        -str medical_notes
        +get_medical_notes(requester_role) str
    }

    class Doctor {
        +str doctor_id
        +str name
        +str specialty
    }

    class TimeSlot {
        +datetime start
        +int duration_minutes
        +end datetime
        +is_upcoming(now) bool
        +label() str
    }

    class AppointmentStatus {
        <<enumeration>>
        PENDING
        ACCEPTED
        DECLINED
    }

    class Appointment {
        +str appointment_id
        +Patient patient
        +Doctor doctor
        +TimeSlot slot
        +AppointmentStatus status
        +occupies_slot() bool
        +counts_as_upcoming(now) bool
    }

    class BookingError {
        +message
    }

    class BookingSystem {
        +int max_upcoming
        +add_patient(patient)
        +add_doctor(doctor)
        +offer_slot(doctor_id, slot)
        +view_available_slots(doctor_id, now) list
        +count_upcoming_appointments(patient_id, now) int
        +book_appointment(patient_id, doctor_id, slot, now) Appointment
        +accept_appointment(doctor_id, appointment_id) Appointment
        +decline_appointment(doctor_id, appointment_id) Appointment
    }

    BookingSystem "1" --> "*" Patient : registers
    BookingSystem "1" --> "*" Doctor : registers
    BookingSystem "1" --> "*" Appointment : records
    BookingSystem "1" --> "*" TimeSlot : offers per doctor
    BookingSystem ..> BookingError : raises
    Patient "1" --> "*" Appointment : requests
    Doctor "1" --> "*" Appointment : reviews
    Appointment --> TimeSlot : scheduled at
    Appointment --> AppointmentStatus : has
```
