from django.db import migrations


def create_default_seats(apps, schema_editor):
    Seat = apps.get_model('home', 'Seat')
    seats = []
    for row in ['A', 'B', 'C', 'D', 'E', 'F']:
        for number in range(1, 11):
            seat_number = f'{row}{number}'
            seats.append(Seat(seat_number=seat_number))
    Seat.objects.bulk_create(seats, ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_booking_movie_alter_booking_seat_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_seats, migrations.RunPython.noop),
    ]
