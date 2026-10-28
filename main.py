"""Doctor Appointment Booking System (educational in-memory implementation).

N (MAX_UPCOMING_APPOINTMENTS) = 3 is confirmed by the instructor.

Upcoming appointment policy
---------------------------
An appointment counts as upcoming only when BOTH are true:
  1. status is PENDING or ACCEPTED
  2. the slot start time is strictly after the current clock (`now`)

DECLINED appointments never count as upcoming and do not occupy a slot.
Past PENDING/ACCEPTED appointments do not count as upcoming.

Slot occupancy policy
---------------------
A doctor's time slot is occupied only by PENDING or ACCEPTED appointments.
A DECLINED appointment frees the slot so another patient may book it.

Status transitions
------------------
PENDING -> ACCEPTED (doctor accepts)
PENDING -> DECLINED (doctor declines)
No other transitions are allowed.

R5/R6/R7 notes
--------------
R5: medical notes are stored privately on Patient and are not printed by the
    demo. A simple role check exists for teaching purposes only; this is not
    real authentication or access control.
R6: availability is computed in memory. A unit test checks that the lookup
    finishes in under 2 seconds on this educational data set. That is not a
    production performance guarantee.
R7: this program is a command-line demonstration, not a mobile UI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


# N = 3 is confirmed by the instructor.
MAX_UPCOMING_APPOINTMENTS = 3


class AppointmentStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"


class BookingError(Exception):
    """Expected validation failure during booking or doctor decisions."""


@dataclass(frozen=True)
class TimeSlot:
    start: datetime
    duration_minutes: int = 30

    @property
    def end(self) -> datetime:
        return self.start + timedelta(minutes=self.duration_minutes)

    def is_upcoming(self, now: datetime) -> bool:
        return self.start > now

    def label(self) -> str:
        end_text = self.end.strftime("%H:%M")
        return f"{self.start.strftime('%Y-%m-%d %H:%M')}–{end_text}"


@dataclass
class Patient:
    patient_id: str
    name: str
    _medical_notes: str = field(default="", repr=False)

    def get_medical_notes(self, requester_role: str) -> str:
        """Educational privacy check only. Not real authorization."""
        if requester_role != "authorized_staff":
            raise PermissionError("Medical data is available only to authorized staff.")
        return self._medical_notes


@dataclass
class Doctor:
    doctor_id: str
    name: str
    specialty: str = "General"


@dataclass
class Appointment:
    appointment_id: str
    patient: Patient
    doctor: Doctor
    slot: TimeSlot
    status: AppointmentStatus = AppointmentStatus.PENDING

    def occupies_slot(self) -> bool:
        return self.status in (AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED)

    def counts_as_upcoming(self, now: datetime) -> bool:
        return self.occupies_slot() and self.slot.is_upcoming(now)


class BookingSystem:
    """In-memory clinic controller for viewing, booking, and reviewing appointments."""

    def __init__(self, max_upcoming: int = MAX_UPCOMING_APPOINTMENTS) -> None:
        self.max_upcoming = max_upcoming
        self.patients: dict[str, Patient] = {}
        self.doctors: dict[str, Doctor] = {}
        self.offered_slots: dict[str, list[TimeSlot]] = {}
        self.appointments: list[Appointment] = []
        self._next_appointment_number = 1

    def add_patient(self, patient: Patient) -> None:
        self.patients[patient.patient_id] = patient

    def add_doctor(self, doctor: Doctor) -> None:
        self.doctors[doctor.doctor_id] = doctor
        self.offered_slots.setdefault(doctor.doctor_id, [])

    def offer_slot(self, doctor_id: str, slot: TimeSlot) -> None:
        self._get_doctor(doctor_id)
        slots = self.offered_slots.setdefault(doctor_id, [])
        if slot in slots:
            raise BookingError("This availability slot is already offered.")
        slots.append(slot)
        slots.sort(key=lambda item: item.start)

    def view_available_slots(self, doctor_id: str, now: datetime) -> list[TimeSlot]:
        """R1 / R6: return future offered slots that are not occupied."""
        self._get_doctor(doctor_id)
        available: list[TimeSlot] = []
        for slot in self.offered_slots.get(doctor_id, []):
            if slot.is_upcoming(now) and not self._slot_is_occupied(doctor_id, slot):
                available.append(slot)
        return available

    def count_upcoming_appointments(self, patient_id: str, now: datetime) -> int:
        self._get_patient(patient_id)
        return sum(
            1
            for appointment in self.appointments
            if appointment.patient.patient_id == patient_id
            and appointment.counts_as_upcoming(now)
        )

    def book_appointment(
        self,
        patient_id: str,
        doctor_id: str,
        slot: TimeSlot,
        now: datetime,
    ) -> Appointment:
        """R2 / R4: create a PENDING request if the slot and upcoming limit allow it."""
        patient = self._get_patient(patient_id)
        doctor = self._get_doctor(doctor_id)

        if slot not in self.offered_slots.get(doctor_id, []):
            raise BookingError("That time is not offered by this doctor.")
        if not slot.is_upcoming(now):
            raise BookingError("Past time slots cannot be booked.")
        if self._slot_is_occupied(doctor_id, slot):
            raise BookingError("That time slot is already booked.")
        if self.count_upcoming_appointments(patient_id, now) >= self.max_upcoming:
            raise BookingError(
                f"A patient may have at most {self.max_upcoming} upcoming appointments."
            )

        appointment = Appointment(
            appointment_id=self._new_appointment_id(),
            patient=patient,
            doctor=doctor,
            slot=slot,
            status=AppointmentStatus.PENDING,
        )
        self.appointments.append(appointment)
        return appointment

    def accept_appointment(self, doctor_id: str, appointment_id: str) -> Appointment:
        """R3: doctor accepts a pending request."""
        appointment = self._get_appointment_for_doctor(doctor_id, appointment_id)
        if appointment.status != AppointmentStatus.PENDING:
            raise BookingError("Only pending appointment requests can be accepted.")
        appointment.status = AppointmentStatus.ACCEPTED
        return appointment

    def decline_appointment(self, doctor_id: str, appointment_id: str) -> Appointment:
        """R3: doctor declines a pending request and frees the slot."""
        appointment = self._get_appointment_for_doctor(doctor_id, appointment_id)
        if appointment.status != AppointmentStatus.PENDING:
            raise BookingError("Only pending appointment requests can be declined.")
        appointment.status = AppointmentStatus.DECLINED
        return appointment

    def _slot_is_occupied(self, doctor_id: str, slot: TimeSlot) -> bool:
        return any(
            appointment.doctor.doctor_id == doctor_id
            and appointment.slot == slot
            and appointment.occupies_slot()
            for appointment in self.appointments
        )

    def _get_patient(self, patient_id: str) -> Patient:
        try:
            return self.patients[patient_id]
        except KeyError as error:
            raise BookingError("Unknown patient.") from error

    def _get_doctor(self, doctor_id: str) -> Doctor:
        try:
            return self.doctors[doctor_id]
        except KeyError as error:
            raise BookingError("Unknown doctor.") from error

    def _get_appointment_for_doctor(self, doctor_id: str, appointment_id: str) -> Appointment:
        self._get_doctor(doctor_id)
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                if appointment.doctor.doctor_id != doctor_id:
                    raise BookingError("This appointment belongs to a different doctor.")
                return appointment
        raise BookingError("Unknown appointment.")

    def _new_appointment_id(self) -> str:
        appointment_id = f"A{self._next_appointment_number:03d}"
        self._next_appointment_number += 1
        return appointment_id


def _print_slots(title: str, slots: list[TimeSlot]) -> None:
    print(title)
    if not slots:
        print("  (none)")
        return
    for slot in slots:
        print(f"  - {slot.label()}")


def _print_appointment(prefix: str, appointment: Appointment) -> None:
    print(
        f"{prefix}{appointment.appointment_id}: "
        f"{appointment.patient.name} with {appointment.doctor.name} "
        f"at {appointment.slot.label()} [{appointment.status.value}]"
    )


def run_demo() -> None:
    """Deterministic demonstration of the principal booking workflow."""
    now = datetime(2026, 10, 28, 9, 0, 0)
    system = BookingSystem(max_upcoming=MAX_UPCOMING_APPOINTMENTS)

    doctor = Doctor("D1", "Dr. Sara Ahmed", "Family Medicine")
    patient_a = Patient("P1", "Omar Hassan", _medical_notes="Confidential: seasonal allergy notes")
    patient_b = Patient("P2", "Lina Nasser")
    system.add_doctor(doctor)
    system.add_patient(patient_a)
    system.add_patient(patient_b)

    day = datetime(2026, 10, 29, 10, 0, 0)
    slot_1000 = TimeSlot(day)
    slot_1030 = TimeSlot(day + timedelta(minutes=30))
    slot_1100 = TimeSlot(day + timedelta(hours=1))
    slot_1400 = TimeSlot(datetime(2026, 10, 29, 14, 0, 0))
    for slot in (slot_1000, slot_1030, slot_1100, slot_1400):
        system.offer_slot(doctor.doctor_id, slot)

    print("Doctor Appointment Booking System — demonstration")
    print(f"Clock: {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"N (max upcoming appointments per patient): {system.max_upcoming}")
    print(f"Doctor: {doctor.name} ({doctor.specialty})")
    print()

    _print_slots("R1 — available slots for Dr. Sara Ahmed:", system.view_available_slots("D1", now))
    print()

    first = system.book_appointment("P1", "D1", slot_1000, now)
    second = system.book_appointment("P1", "D1", slot_1030, now)
    third = system.book_appointment("P1", "D1", slot_1100, now)
    print("R2 — Omar books three available slots:")
    _print_appointment("  ", first)
    _print_appointment("  ", second)
    _print_appointment("  ", third)
    print(f"  Omar upcoming count: {system.count_upcoming_appointments('P1', now)}")
    print()

    print("R4 — Omar tries to book a fourth upcoming appointment:")
    try:
        system.book_appointment("P1", "D1", slot_1400, now)
        print("  ERROR: the limit should have been enforced.")
    except BookingError as error:
        print(f"  Rejected: {error}")
    print()

    print("R2 — Lina tries to book Omar's occupied 10:00 slot:")
    try:
        system.book_appointment("P2", "D1", slot_1000, now)
        print("  ERROR: double-booking should have been rejected.")
    except BookingError as error:
        print(f"  Rejected: {error}")
    print()

    system.accept_appointment("D1", first.appointment_id)
    system.decline_appointment("D1", second.appointment_id)
    print("R3 — doctor decisions:")
    _print_appointment("  Accepted ", first)
    _print_appointment("  Declined ", second)
    print(f"  Omar upcoming count after decline: {system.count_upcoming_appointments('P1', now)}")
    print()

    _print_slots(
        "Available slots after the decline (10:30 should be free):",
        system.view_available_slots("D1", now),
    )
    print()

    lina_booking = system.book_appointment("P2", "D1", slot_1030, now)
    print("R2 — Lina books the freed 10:30 slot:")
    _print_appointment("  ", lina_booking)
    print()

    print("R5 — educational privacy check (medical notes are not printed in this demo):")
    try:
        patient_a.get_medical_notes("patient")
        print("  ERROR: unauthorized access should have been denied.")
    except PermissionError:
        print("  Unauthorized requester was denied access to medical notes.")
    authorized_notes = patient_a.get_medical_notes("authorized_staff")
    print(f"  Authorized staff can retrieve notes ({len(authorized_notes)} characters). Contents not displayed.")
    print()

    print("Final appointments:")
    for appointment in system.appointments:
        _print_appointment("  ", appointment)
    print()
    print("Demo finished. Pending and accepted future appointments occupy slots.")
    print("Declined appointments do not occupy slots and do not count toward N.")


if __name__ == "__main__":
    run_demo()
