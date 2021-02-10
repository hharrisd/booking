from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import BookingForm
from .models import Booking


def home(request):
    return render(request, 'bookingapp/home.html', {})

class BookingView(generic.ListView):
    model = Booking
    template_name = 'bookingapp/home.html'
    context_object_name = 'booking_list'


def booking_new(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bookingapp:home'))
    else:
        form = BookingForm()
    return render(request, 'bookingapp/booking_form.html', {'form': form})
