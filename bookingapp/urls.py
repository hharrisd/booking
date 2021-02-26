from django.urls import path
from .import views

app_name = 'bookingapp'

urlpatterns = [
    path('', views.BookingView.as_view(), name='home'),
    path('booking/new/', views.booking_new, name='booking_form')
]
