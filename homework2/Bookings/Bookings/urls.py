from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from home.views import (
    BookingHistoryView,
    BookingViewSet,
    SeatBookingView,
    MovieListView,
    RegisterView,
    MovieViewSet,
    SeatViewSet,
)

# --- DRF Router (API) ---
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'seats', SeatViewSet, basename='seat')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth (Django's built-in login/logout pages)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),

    # --- HTML Pages ---
    path('', MovieListView.as_view(), name='home'),                         # homepage shows movie list
    path('history/', BookingHistoryView.as_view(), name='booking-history'), # booking history page
    path('book/', SeatBookingView.as_view(), name='seat-booking'),          # seat reservation form


    # --- API ---
    path('api/', include(router.urls)),                                            # include the DRF router URLs
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')), # DRF login/logout
]
