# Sequence Diagram

This diagram shows the appointment-booking process used by `BookingSystem` in `main.py`. It includes availability checking, the N upcoming-appointment limit, duplicate/unavailable slot handling, appointment creation, and the doctor's accept or decline decision.

Participants match the class diagram: Patient, BookingSystem, Doctor, TimeSlot, and Appointment.

A successful booking is shown only after validation succeeds. Failed validation does not create an appointment.

```mermaid
sequenceDiagram
    actor Patient
    participant System as BookingSystem
    actor Doctor

    Patient->>System: view_available_slots(doctor_id, now)
    System->>System: keep future unoccupied TimeSlots
    System-->>Patient: available slots

    Patient->>System: book_appointment(patient_id, doctor_id, slot, now)

    alt slot not offered, in the past, or already occupied
        System-->>Patient: BookingError (no appointment created)
    else patient already has N upcoming appointments
        System-->>Patient: BookingError (limit N=3, no appointment created)
    else slot is free and upcoming count is below N
        System->>System: create Appointment PENDING
        System-->>Patient: PENDING appointment (slot now occupied)

        Doctor->>System: accept_appointment or decline_appointment

        alt doctor accepts a PENDING request
            System->>System: status = ACCEPTED
            System-->>Doctor: ACCEPTED appointment (slot remains occupied)
        else doctor declines a PENDING request
            System->>System: status = DECLINED
            System-->>Doctor: DECLINED appointment (slot freed)
            Note over Patient,System: Another patient may now book the freed slot
        else appointment is not PENDING
            System-->>Doctor: BookingError (status unchanged)
        end
    end
```
