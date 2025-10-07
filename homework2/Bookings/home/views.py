from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError

from .forms import BookingForm
from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer


# HTML views (template responses)
class MovieListView(generic.ListView):
    model = Movie  # queryset source for the page
    template_name = 'bookings/movie_list.html'  # which template to render
    context_object_name = 'movie_list'  # context key available in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # get default context
        context['movie_count'] = self.get_queryset().count()  # expose total count
        return context


class SeatListView(generic.ListView):
    model = Seat  # show all seats
    template_name = 'bookings/seat_booking.html'  # seat booking page
    context_object_name = 'seats'  # template uses this variable


class BookingHistoryView(LoginRequiredMixin, generic.ListView):
    model = Booking                                  # base queryset
    template_name = 'bookings/booking_history.html'  # history template
    context_object_name = 'booking_list'             # list exposed to template
    login_url = 'login'                              # redirect target when anonymous
    redirect_field_name = 'next'                     # preserve the page to return to

    # Only show bookings for the current user, most recent first
    def get_queryset(self):
        return (
            Booking.objects.select_related('movie', 'seat')  # avoid extra queries
            .filter(user=self.request.user)  # only this user's bookings
            .order_by('-booking_date')  # newest first
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # start with default context
        context['has_bookings'] = context['booking_list'].exists()  # toggle empty-state UI
        return context


class SeatBookingView(LoginRequiredMixin, generic.CreateView):
    model = Booking  # create Booking instances
    form_class = BookingForm  # filtered movie/seat choices
    template_name = 'bookings/seat_booking.html'  # seat booking form template
    success_url = reverse_lazy('booking-history')  # review history after booking

    def get_initial(self):
        initial = super().get_initial()
        movie_id = self.request.GET.get('movie') or self.request.POST.get('movie')
        if movie_id:
            initial['movie'] = movie_id  # preselect movie in the form
        return initial

    def form_valid(self, form):
        booking = form.save(commit=False)  # build object without saving
        booking.user = self.request.user  # track which user booked
        booking.save()  # persist booking

        seat = booking.seat
        if not seat.booking_status:
            seat.booking_status = True  # mark seat as taken
            seat.save(update_fields=['booking_status'])

        messages.success(
            self.request,
            f'Seat {seat.seat_number} booked for {booking.movie.title}.'
        )
        self.object = booking
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below and try again.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_seats'] = Seat.objects.filter(booking_status=False).count()  # show remaining seats
        form = context['form']

        selected_movie = None
        movie_value = form['movie'].value()
        if movie_value:
            selected_movie = Movie.objects.filter(pk=movie_value).first()
        context['selected_movie'] = selected_movie

        available_ids = set(form.fields['seat'].queryset.values_list('id', flat=True))
        selected_seat_id = form['seat'].value()
        seat_lookup = {seat.seat_number: seat for seat in Seat.objects.all()}
        seat_map = []
        for row_letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            row_seats = []
            for number in range(1, 11):
                seat_number = f'{row_letter}{number}'
                seat = seat_lookup.get(seat_number)
                if seat:
                    seat_id_str = str(seat.id)
                    row_seats.append({
                        'seat': seat,
                        'id': seat.id,
                        'label': seat_number,
                        'is_available': seat.id in available_ids,
                        'is_selected': selected_seat_id and seat_id_str == str(selected_seat_id),
                    })
            seat_map.append({'row': row_letter, 'seats': row_seats})
        context['seat_map'] = seat_map
        return context


class RegisterView(generic.CreateView):
    form_class = UserCreationForm  # default Django user creation form
    template_name = 'registration/register.html'  # registration page template
    success_url = reverse_lazy('login')  # send users to sign-in after registering


# REST API viewsets (JSON responses)
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('title')  # list/search source
    serializer_class = MovieSerializer                # serialize Movie objects
    permission_classes = [permissions.AllowAny]       # public API


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all().order_by('seat_number')  # order seats logically
    serializer_class = SeatSerializer                      # serialize Seat objects
    permission_classes = [permissions.AllowAny]            # public API
    http_method_names = ['get', 'head', 'options']         # seats are read-only via API


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('movie', 'seat', 'user').all()  # include related data
    serializer_class = BookingSerializer                                      # serialize Booking objects
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]              # read for all, write for authed users
    http_method_names = ['get', 'post', 'delete', 'head', 'options']          # bookings allow create/list/delete

    def perform_create(self, serializer):
        seat = serializer.validated_data['seat']  # seat chosen in the payload
        if seat.booking_status:
            raise ValidationError({'seat_id': 'That seat is already booked.'})

        booking = serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None  # stamp booking owner
        )
        seat.booking_status = True  # mark as reserved
        seat.save(update_fields=['booking_status'])
        return booking

    def perform_destroy(self, instance):
        seat = instance.seat
        instance.delete()
        seat.booking_status = False  # free up the seat
        seat.save(update_fields=['booking_status'])

    def get_queryset(self):
        base_qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return base_qs  # staff can see all bookings
        if user.is_authenticated:
            return base_qs.filter(user=user)  # regular users see their own
        return base_qs.none()  # anonymous users get no bookings
