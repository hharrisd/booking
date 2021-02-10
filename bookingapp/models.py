from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Asset(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    slot = models.CharField(max_length=1)
    check_in = models.TimeField()
    check_out = models.TimeField()

    def clean(self):
        """ Validate that time slot has at least 1 hour of duration """
        if self.check_out.hour - self.check_in.hour < 1:
            raise ValidationError(_('A time slot must have at least 1 hour of duration'))

    def __str__(self):
        return f'Slot {self.slot}: {self.check_in.strftime("%H:%M")} to {self.check_out.strftime("%H:%M")}'


class Booking(models.Model):
    day = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.asset.description}, booked to {self.customer}, ' \
               f'from {self.time_slot.check_in.strftime("%H:%M")} ' \
               f'to {self.time_slot.check_out.strftime("%H:%M")}'
