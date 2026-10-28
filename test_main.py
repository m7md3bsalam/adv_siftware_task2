"""Unit tests for the Doctor Appointment Booking System."""

from __future__ import annotations

import time
import unittest
from datetime import datetime, timedelta

from main import (
    MAX_UPCOMING_APPOINTMENTS,
    AppointmentStatus,
    BookingError,
    BookingSystem,
    Doctor,
    Patient,
    TimeSlot,
)


class BookingSystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 10, 28, 9, 0, 0)
        self.system = BookingSystem(max_upcoming=MAX_UPCOMING_APPOINTMENTS)
        self.doctor = Doctor("D1", "Dr. Sara Ahmed")
        self.patient_a = Patient("P1", "Omar Hassan", _medical_notes="private")
        self.patient_b = Patient("P2", "Lina Nasser")
        self.system.add_doctor(self.doctor)
        self.system.add_patient(self.patient_a)
        self.system.add_patient(self.patient_b)
        self.slot_a = TimeSlot(datetime(2026, 10, 29, 10, 0, 0))
        self.slot_b = TimeSlot(datetime(2026, 10, 29, 10, 30, 0))
        self.slot_c = TimeSlot(datetime(2026, 10, 29, 11, 0, 0))
        self.slot_d = TimeSlot(datetime(2026, 10, 29, 14, 0, 0))
        for slot in (self.slot_a, self.slot_b, self.slot_c, self.slot_d):
            self.system.offer_slot("D1", slot)

    def test_view_available_slots(self) -> None:
        slots = self.system.view_available_slots("D1", self.now)
        self.assertEqual(slots, [self.slot_a, self.slot_b, self.slot_c, self.slot_d])

    def test_availability_lookup_finishes_within_two_seconds(self) -> None:
        started = time.perf_counter()
        slots = self.system.view_available_slots("D1", self.now)
        elapsed = time.perf_counter() - started
        self.assertEqual(len(slots), 4)
        self.assertLess(elapsed, 2.0)

    def test_book_available_slot_successfully(self) -> None:
        appointment = self.system.book_appointment("P1", "D1", self.slot_a, self.now)
        self.assertEqual(appointment.status, AppointmentStatus.PENDING)
        self.assertEqual(appointment.patient.patient_id, "P1")
        remaining = self.system.view_available_slots("D1", self.now)
        self.assertNotIn(self.slot_a, remaining)

    def test_reject_already_booked_slot(self) -> None:
        self.system.book_appointment("P1", "D1", self.slot_a, self.now)
        with self.assertRaises(BookingError):
            self.system.book_appointment("P2", "D1", self.slot_a, self.now)

    def test_reject_unoffered_slot(self) -> None:
        unknown = TimeSlot(datetime(2026, 10, 29, 16, 0, 0))
        with self.assertRaises(BookingError):
            self.system.book_appointment("P1", "D1", unknown, self.now)

    def test_enforce_upcoming_appointment_limit(self) -> None:
        self.assertEqual(MAX_UPCOMING_APPOINTMENTS, 3)
        self.system.book_appointment("P1", "D1", self.slot_a, self.now)
        self.system.book_appointment("P1", "D1", self.slot_b, self.now)
        self.system.book_appointment("P1", "D1", self.slot_c, self.now)
        with self.assertRaises(BookingError):
            self.system.book_appointment("P1", "D1", self.slot_d, self.now)
        self.assertEqual(self.system.count_upcoming_appointments("P1", self.now), 3)

    def test_accept_appointment(self) -> None:
        appointment = self.system.book_appointment("P1", "D1", self.slot_a, self.now)
        accepted = self.system.accept_appointment("D1", appointment.appointment_id)
        self.assertEqual(accepted.status, AppointmentStatus.ACCEPTED)
        self.assertTrue(self.system._slot_is_occupied("D1", self.slot_a))
        self.assertNotIn(self.slot_a, self.system.view_available_slots("D1", self.now))

    def test_decline_appointment_frees_slot(self) -> None:
        appointment = self.system.book_appointment("P1", "D1", self.slot_a, self.now)
        declined = self.system.decline_appointment("D1", appointment.appointment_id)
        self.assertEqual(declined.status, AppointmentStatus.DECLINED)
        self.assertFalse(declined.occupies_slot())
        self.assertIn(self.slot_a, self.system.view_available_slots("D1", self.now))
        other = self.system.book_appointment("P2", "D1", self.slot_a, self.now)
        self.assertEqual(other.status, AppointmentStatus.PENDING)

    def test_cannot_accept_or_decline_non_pending(self) -> None:
        appointment = self.system.book_appointment("P1", "D1", self.slot_a, self.now)
        self.system.accept_appointment("D1", appointment.appointment_id)
        with self.assertRaises(BookingError):
            self.system.decline_appointment("D1", appointment.appointment_id)

    def test_past_appointments_do_not_count_as_upcoming(self) -> None:
        past_slot = TimeSlot(datetime(2026, 10, 27, 10, 0, 0))
        self.system.offer_slot("D1", past_slot)
        with self.assertRaises(BookingError):
            self.system.book_appointment("P1", "D1", past_slot, self.now)

        future = self.system.book_appointment("P1", "D1", self.slot_a, self.now)
        self.system.accept_appointment("D1", future.appointment_id)
        later = self.now + timedelta(days=3)
        self.assertEqual(self.system.count_upcoming_appointments("P1", later), 0)
        self.assertEqual(self.system.view_available_slots("D1", later), [])

    def test_declined_does_not_count_toward_n(self) -> None:
        first = self.system.book_appointment("P1", "D1", self.slot_a, self.now)
        self.system.book_appointment("P1", "D1", self.slot_b, self.now)
        self.system.book_appointment("P1", "D1", self.slot_c, self.now)
        self.system.decline_appointment("D1", first.appointment_id)
        fourth = self.system.book_appointment("P1", "D1", self.slot_d, self.now)
        self.assertEqual(fourth.status, AppointmentStatus.PENDING)
        self.assertEqual(self.system.count_upcoming_appointments("P1", self.now), 3)

    def test_medical_notes_require_authorized_staff(self) -> None:
        with self.assertRaises(PermissionError):
            self.patient_a.get_medical_notes("patient")
        self.assertEqual(self.patient_a.get_medical_notes("authorized_staff"), "private")


if __name__ == "__main__":
    unittest.main()
