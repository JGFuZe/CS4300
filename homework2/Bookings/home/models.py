from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes


    # Define default String to return the name for representing the Model object
    def __str__(self):
        return self.title
    

class Seat(models.Model):
    seat_number = models.CharField(max_length=10)
    booking_status = models.BooleanField(default=False)  # True if booked, False if available

    def __str__(self):
        return self.seat_number
    

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.movie.title} - Seat {self.seat.seat_number}"