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
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True,
    )
    seat = SeatSerializer(read_only=True)
    seat_id = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        source='seat',
        write_only=True,
    )
    user = serializers.StringRelatedField(read_only=True)

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

