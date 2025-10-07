from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

# Get the User model
User = get_user_model()

# Movie model to represent movies in the system
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()    # Description of the movie
    release_date = models.DateField()   # Release date of the movie
    duration = models.IntegerField()    # Duration in minutes

    def __str__(self):
        return self.title
    
# Seat model to represent seats in the theater
class Seat(models.Model):
    seat_number = models.CharField(max_length=10)        # e.g., "A1", "B2"
    booking_status = models.BooleanField(default=False)  # True if booked, False if available

    def __str__(self):
        return self.seat_number

    
# Booking model to link users, movies, and seats
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='bookings') # Movie being booked
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')   # Seat being booked
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')   # User who made the booking
    booking_date = models.DateTimeField(auto_now_add=True)                              # Date and time of booking

    def __str__(self):
        return f'{self.movie.title} - Seat {self.seat.seat_number}'
