from rest_framework import serializers
from .models import Booking, Movie, Seat


# Map Movie model fields to JSON for the API
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration']

# MovieSerializer End


# Map Seat model fields to JSON for the API
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'booking_status']

# SeatSerializer End


# Map Booking model fields to JSON while accepting FK IDs
class BookingSerializer(serializers.ModelSerializer):

    # Nested serializers for read-only representation
    movie = MovieSerializer(read_only=True)

    # Accept movie_id and seat_id for creating/updating bookings
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True,
    )

    # Nested Seat serializer for read-only representation
    seat = SeatSerializer(read_only=True)

    # Accept seat_id for creating/updating bookings
    seat_id = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        source='seat',
        write_only=True,
    )

    # Read-only user representation
    user = serializers.StringRelatedField(read_only=True)

    # Meta class to define model and fields
    class Meta:
        model = Booking
        fields = [
            'id',
            'movie',
            'movie_id',
            'seat',
            'seat_id',
            'user',
            'booking_date',
        ]
        read_only_fields = ['id', 'movie', 'seat', 'user', 'booking_date']

# BookingSerializer End

