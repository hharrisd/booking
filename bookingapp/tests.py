from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import TimeSlot


class TimeSlotModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        checkin = datetime.strptime('06:00', '%H:%M').time()
        checkout = datetime.strptime('06:30', '%H:%M').time()
        TimeSlot.objects.create(slot='A', check_in=checkin, check_out=checkout)

    def test_create_timeslot_time_format(self):
        """"
        Checks if time slot has the proper time format: '%H:%M
        """
        timeslot = TimeSlot.objects.get(id=1)
        self.assertEquals(str(timeslot), 'Slot A: 06:00 to 07:00')

    def test_time_diference(self):
        """
        Checks if time difference between checkin and checkout is at least 1 hour
        """
        # timeslot = TimeSlot.objects.get(id=1)
        # diff = timeslot.check_out.hour - timeslot.check_in.hour
        checkin = datetime.strptime('09:00', '%H:%M').time()
        checkout = datetime.strptime('09:00', '%H:%M').time()
        self.assertRaises(ValidationError, TimeSlot, slot='A', check_in=checkin, check_out=checkout)

    def test_range_hour(self):
        """
        Checks if checking is not earlier than 7 AM
        """
        checkin = datetime.strptime('06:00', '%H:%M').time()
        checkout = datetime.strptime('08:30', '%H:%M').time()
        self.assertRaises(ValidationError, TimeSlot, slot='A', check_in=checkin, check_out=checkout)
