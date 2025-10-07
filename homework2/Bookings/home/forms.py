from django import forms

from .models import Booking, Movie, Seat


class BookingForm(forms.ModelForm):
    """Form used by the seat booking page; limits seats to available ones."""

    class Meta:
        model = Booking
        fields = ['movie', 'seat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movie'].queryset = Movie.objects.order_by('title')  # show movies alphabetically
        self.fields['seat'].queryset = Seat.objects.filter(booking_status=False).order_by('seat_number')  # only free seats
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_seat(self):
        seat = self.cleaned_data['seat']
        if seat.booking_status:
            raise forms.ValidationError('That seat has already been booked. Please choose another.')
        return seat
