from django import forms

from .models import Booking, Movie, Seat

# Form used by the seat booking page; limits seats to available ones
class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['movie', 'seat']

    # Customize form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # all movies ordered by title
        self.fields['movie'].queryset = Movie.objects.order_by('title')

        # only available seats ordered by seat number
        self.fields['seat'].queryset = Seat.objects.filter(booking_status=False).order_by('seat_number') 

        # Add Bootstrap classes to form fields for styling
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    # Custom validation to ensure the selected seat is still available
    def clean_seat(self):
        seat = self.cleaned_data['seat']
        
        # Check if the seat is already booked
        if seat.booking_status:
            raise forms.ValidationError('That seat has already been booked. Please choose another.')
        return seat
