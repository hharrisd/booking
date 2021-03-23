from contextlib import contextmanager
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.test import TestCase
from django.utils import timezone

from .models import TimeSlot, Booking, Profile, Category, Asset
from .forms import BookingForm


class ValidationErrorTestMixin(object):

    @contextmanager
    def assertValidationErrors(self, fields):
        """
        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))


class TimeSlotModelTests(TestCase, ValidationErrorTestMixin):
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
        self.assertEquals(str(timeslot), 'Slot A: 06:00 to 06:30')

    def test_time_diference(self):
        """
        Checks if time difference between checkin and checkout is at least 1 hour
        """
        # timeslot = TimeSlot.objects.get(id=1)
        # diff = timeslot.check_out.hour - timeslot.check_in.hour
        checkin = datetime.strptime('09:00', '%H:%M').time()
        checkout = datetime.strptime('09:00', '%H:%M').time()
        time_slot = TimeSlot(slot='T', check_in=checkin, check_out=checkout)
        with self.assertValidationErrors([NON_FIELD_ERRORS]):
            time_slot.full_clean()

    def test_range_hour(self):
        """
        Checks if check in is not earlier than 7 AM
        and check out is not later than 19:00
        """
        checkin = datetime.strptime('06:00', '%H:%M').time()
        checkout = datetime.strptime('20:30', '%H:%M').time()
        time_slot = TimeSlot(slot='S', check_in=checkin, check_out=checkout)

        with self.assertValidationErrors(['__all__']):
            time_slot.full_clean()


def create_customer():
    """
    Creates a booking object
    :return: Customer object
    """
    test_user = User.objects.create_user(username='john', email='john@doe.com', password='123')

    customer_name = 'John Done'
    customer_address = 'Test Street 125'
    customer_birthday = datetime(1980, 12, 31)
    customer_email = 'test@test.com'
    Profile.objects.create(name=customer_name, address=customer_address, birthday=customer_birthday,
                                  email=customer_email, user=test_user)
    return test_user


def create_slot():
    check_in = datetime.strptime('09:00', '%H:%M').time()
    check_out = datetime.strptime('10:00', '%H:%M').time()
    return TimeSlot.objects.create(slot='T', check_in=check_in, check_out=check_out)


# def create_booking(days):
#     """
#     Creates a booking object
#     :param days: creation date difference in days
#     :return: Booking object
#     """
#     day = timezone.now() + timedelta(days=days)
#
#
#     test_customer = create_customer()
#     test_category = Category.objects.create(category='Testing')
#     test_asset = Asset.objects.create(category=test_category, description='Test Asset', comment='An asset to test')
#     test_time_slot = create_slot()
#     return Booking.objects.create(day=day, time_slot=test_time_slot, asset=test_asset, customer=test_customer)


class BookingFormTests(TestCase):
    def test_booking_in_past_time(self):
        """
        Checks that a booking is not made in past time
        """

        day = timezone.now() + timedelta(days=-10)

        test_customer = create_customer()
        test_category = Category.objects.create(category='Testing')
        test_asset = Asset.objects.create(category=test_category, description='Test Asset', comment='An asset to test')
        test_time_slot = create_slot()
        # return Booking.objects.create(day=day, time_slot=test_time_slot, asset=test_asset, customer=test_customer)
        booking_form = BookingForm(
            data={
                'day': day,
                'time_slot': test_time_slot,
                'asset': test_asset,
                'user': test_customer
            })

        self.assertEqual(
            booking_form.errors["day"], ["A booking cannot be made in the past"]
        )

    def test_unique_booking_constraint(self):
        day = timezone.now() + timedelta(days=2)

        test_customer = create_customer()
        test_category = Category.objects.create(category='Testing')
        test_asset = Asset.objects.create(category=test_category, description='Test Asset', comment='An asset to test')
        test_time_slot = create_slot()
        try:
            booking_form1 = Booking.objects.create(day=day, time_slot=test_time_slot, asset=test_asset, customer=test_customer)

            booking_form2 = Booking.objects.create(day=day, time_slot=test_time_slot, asset=test_asset, customer=test_customer)
        except Exception as e:
            print(e)
