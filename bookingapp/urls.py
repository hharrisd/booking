from django.urls import path
from .import views

app_name = 'bookingapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.BookingView.as_view(), name='index'),
    path('booking/new/', views.booking_new, name='new')
]
