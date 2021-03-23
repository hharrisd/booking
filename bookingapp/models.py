from urllib import request

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category


class Asset(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, unique=True)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.description


class Profile(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    slot = models.CharField(max_length=1, unique=True)
    check_in = models.TimeField()
    check_out = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_timeslot', fields=['check_in', 'check_out'])
        ]

    def clean(self):
        cleaned_data = super().clean()
        validation_error_list = []

        """ Validate that time slot has at least 1 hour of duration """
        if self.check_out.hour - self.check_in.hour < 1:
            validation_error_list.append(
                ValidationError(_('A time slot must have at least 1 hour of duration'), code='invalid'))
        """ Checks if check in is not earlier than 7 AM """
        if self.check_in.hour < timezone.localtime().strptime('07:00', '%H:%M').hour:
            validation_error_list.append(
                ValidationError({'check_in': _('Check in cannot be earlier than 07:00')}, code='invalid'))
        """ Checks if check out is not later than 19:00 """
        if self.check_out.hour > timezone.localtime().strptime('19:00', '%H:%M').hour:
            validation_error_list.append(
                ValidationError({'check_in': _('Check out cannot be later than 19:00')}, code='invalid'))

        if validation_error_list:
            raise ValidationError(validation_error_list)

        return cleaned_data

    def __str__(self):
        return f'Slot {self.slot}: {self.check_in.strftime("%H:%M")} to {self.check_out.strftime("%H:%M")}'


class Booking(models.Model):
    day = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_booking', fields=['day', 'time_slot', 'asset'])
        ]

    def clean(self):
        now = timezone.now()

        if self.day < now.date():
            raise ValidationError({'day': _('A booking cannot be made in the past')})

    def __str__(self):
        return f'{self.asset.description}, booked to {self.user.username}, ' \
               f'on {self.day.strftime("%x")}, ' \
               f'from {self.time_slot.check_in.strftime("%H:%M")} ' \
               f'to {self.time_slot.check_out.strftime("%H:%M")}'

    def get_absolute_url(self):
        return reverse('bookingapp:booking_detail', args=[self.id])

    def comming_booking(self):
        now = timezone.now().date()
        return self.day > now
