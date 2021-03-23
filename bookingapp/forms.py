from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Booking


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['day', 'time_slot', 'asset', 'user']
        exclude = ['user']
