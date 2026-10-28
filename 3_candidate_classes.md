# Candidate Classes

Evidence is taken from the seven requirements and from UC1–UC4. The goal is a small set of domain classes that a student can implement and explain.

| Class | Evidence from requirements or use cases | Classification |
| --- | --- | --- |
| Patient | R1, R2, R4, R5; UC1, UC2, UC4. Actor who views availability, books, and is limited to N upcoming appointments. Holds medical notes that must stay private. | Explicit |
| Doctor | R1, R3; UC1, UC3. Actor who offers availability and accepts or declines requests. | Explicit |
| TimeSlot | R1, R2, R6. Days and times when a doctor is available; the unit a patient books. | Explicit |
| Appointment | R2, R3, R4; UC2, UC3, UC4. The booking request that can be pending, accepted, or declined. | Explicit |
| AppointmentStatus | R3; UC3. Needed to model accept/decline and whether a slot stays occupied. | Inferred |
| BookingSystem | UC1–UC4. Coordinates patients, doctors, offered slots, occupancy, and the N limit. The assignment needs a runnable controller even though the word "system" is the product, not a named domain noun. | Inferred |
| BookingError | Validation failures in UC2 alternative flows (unavailable slot, duplicate booking, N limit). | Inferred |
| Calendar | R1 mentions days and times. Python `datetime` already represents this; a separate Calendar class would duplicate TimeSlot. | Rejected |
| Database | No persistence requirement in R1–R7. An in-memory list is enough for the lab. | Rejected |
| UserAccount / LoginService | R5 requires authorized access to medical data, but this educational program is not a real identity platform. A role string on `get_medical_notes` is enough to discuss the idea. | Rejected |
| Payment | No payment requirement. | Rejected |
| Hospital / Clinic building | Not required to book a slot with a doctor. | Rejected |
| NotificationService | No requirement to email or SMS the patient. | Rejected |
| MobileApp / Screen | R7 is a usability constraint. A CLI lab program cannot honestly claim a mobile UI class. | Rejected |

## Selected implementation classes

`Patient`, `Doctor`, `TimeSlot`, `Appointment`, `AppointmentStatus`, `BookingSystem`, and `BookingError`.

These match `4_class_diagram.md` and `main.py`.
