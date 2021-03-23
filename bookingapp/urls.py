from django.urls import path
from .import views

app_name = 'bookingapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.BookingView.as_view(), name='index'),
    path('booking/<int:pk>', views.BookingDetail.as_view(), name='booking_detail'),
    path('booking/<int:pk>/update', views.BookingUpdate.as_view(), name='booking_update'),
    path('booking/new/', views.BookingCreate.as_view(), name='new')
]
