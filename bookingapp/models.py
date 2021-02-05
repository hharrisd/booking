from django.db import models
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
    start_date = models.TimeField()
    end_date = models.TimeField()

    def __str__(self):
        return f'Slot {self.slot}: {self.start_date} to {self.end_date}'


class Booking(models.Model):
    day = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.asset.description} booked to {self.customer}, from {self.time_slot.start_date} to {self.time_slot.end_date}'
