from django.urls import path
from .import views

app_name = 'bookingapp'

urlpatterns = [
    path('', views.home, name='home')
]
