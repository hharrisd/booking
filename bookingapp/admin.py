from django.contrib import admin
from .models import Asset, Category, Customer, Booking, TimeSlot

admin.site.register(TimeSlot)
admin.site.register(Asset)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Booking)
