from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Booking, Movie, Seat


# Tests for Movie model behavior
class MovieModelTest(TestCase):
    def test_str_returns_title(self):
        # Expect __str__ to mirror the movie title.
        movie = Movie.objects.create(                                         # create a sample movie
            title='Test Movie',
            description='A synopsis.',
            release_date=date(2024, 1, 1),
            duration=120,
        )
        self.assertEqual(str(movie), 'Test Movie')                             # string version should be title

# MovieModelTest End


# Tests that exercise the DRF booking endpoints
class BookingFlowAPITest(TestCase):
    def setUp(self):
        # Prep auth client, movie, and seat before each API test.
        self.user = get_user_model().objects.create_user(
            username='tester',
            email='tester@example.com',
            password='password123',
        )                                                                      # API caller
        self.movie = Movie.objects.create(
            title='API Film',
            description='Space adventure',
            release_date=date(2024, 5, 15),
            duration=110,
        )                                                                      # movie to book
        self.seat = Seat.objects.get(seat_number='A1')                         # seeded seat
        self.seat.booking_status = False                                       # ensure available
        self.seat.save(update_fields=['booking_status'])
        self.client = APIClient()                                              # DRF helper
        self.client.force_authenticate(self.user)                              # simulate login

    def test_booking_marks_seat_as_unavailable(self):
        # POST should create booking and lock the seat.
        payload = {'movie_id': self.movie.id, 'seat_id': self.seat.id}  # request body
        response = self.client.post(reverse('booking-list'), payload, format='json')
        self.assertEqual(response.status_code, 201)  # should be created
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)                              # seat now booked
        booking = Booking.objects.get(pk=response.data['id'])                  # fetch created booking
        self.assertEqual(booking.user, self.user)                              # user attached

    def test_cannot_book_same_seat_twice(self):
        # Second booking on same seat should fail with 400.
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)    # existing booking
        self.seat.booking_status = True                                             # seat taken
        self.seat.save(update_fields=['booking_status'])
        response = self.client.post(
            reverse('booking-list'),
            {'movie_id': self.movie.id, 'seat_id': self.seat.id},
            format='json',
        )                                                                          # try again
        self.assertEqual(response.status_code, 400)                                # expect bad request
        self.assertIn('seat_id', response.data)                                    # error keyed to seat

    def test_delete_booking_frees_seat(self):
        # DELETE should remove booking and reopen seat.
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)  # existing record
        self.seat.booking_status = True
        self.seat.save(update_fields=['booking_status'])
        response = self.client.delete(reverse('booking-detail', args=[booking.id])) # delete call
        self.assertEqual(response.status_code, 204)                                 # no content means success
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.booking_status)                                   # seat free again

# BookingFlowAPITest End


# Tests that validate the form-based booking view
class SeatBookingViewTest(TestCase):
    def setUp(self):
        # Prepare user login plus movie and seat for the form.
        self.user = get_user_model().objects.create_user(
            username='webuser',
            email='webuser@example.com',
            password='strongpass',
        )                                                                      # UI user
        self.movie = Movie.objects.create(
            title='Form Film',
            description='Drama',
            release_date=date(2024, 6, 1),
            duration=95,
        )                                                                      # movie option
        self.seat = Seat.objects.get(seat_number='B2')                         # seeded seat
        self.seat.booking_status = False                                       # make sure it is free
        self.seat.save(update_fields=['booking_status'])

    def test_requires_login(self):
        # Anonymous visitor should be redirected to login.
        response = self.client.get(reverse('seat-booking'))                    # no login
        self.assertEqual(response.status_code, 302)                            # expect redirect
        self.assertIn(reverse('login'), response.url)                          # destination is login page

    def test_successful_booking_updates_seat(self):
        # Posting the form while logged in should reserve seat.
        self.client.login(username='webuser', password='strongpass')           # simulate login
        response = self.client.post(
            reverse('seat-booking'),
            {'movie': self.movie.id, 'seat': self.seat.id},
            follow=True,
        )                                                                      # submit form
        self.assertEqual(response.status_code, 200)                            # landed on success page
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)                              # seat taken
        booking = Booking.objects.get(seat=self.seat)                          # pull booking
        self.assertEqual(booking.user, self.user)                              # owned by logged-in user

# SeatBookingViewTest End

