from django.contrib import admin
from .models import Asset, Category, Profile, Booking, TimeSlot

admin.site.register(TimeSlot)
admin.site.register(Asset)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Booking)
