from django.db import models


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

    def __str__(self):
        return self.name


class Booking(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
