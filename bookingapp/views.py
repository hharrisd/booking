from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView

from .forms import BookingForm
from .models import Booking


def home(request):
    return render(request, 'home.html', {})


def index(request):
    return render(request, 'bookingapp/booking_index.html', {})


class BookingView(generic.ListView):
    model = Booking
    template_name = 'bookingapp/booking_index.html'
    context_object_name = 'booking_list'

    def get_queryset(self):
        """
        Return bookings of the logged user
        :return: Booking List
        """
        return Booking.objects.filter(user=self.request.user.id).order_by('day')


class BookingCreate(LoginRequiredMixin, CreateView):
    model = Booking
    # fields = ['day', 'time_slot', 'asset']
    form_class = BookingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookingDetail(generic.DetailView):
    model = Booking
    template_name = 'bookingapp/booking_datail.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        else:
            return Booking.objects.none()


class BookingUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Booking
    form_class = BookingForm
