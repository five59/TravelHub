# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('manufacturer', models.CharField(blank=True, default='', help_text='The name of the manufacturer.', max_length=64, verbose_name='Manufacturer')),
                ('model', models.CharField(blank=True, default='', help_text='The model name of the aircraft.', max_length=32, verbose_name='Model Name')),
                ('designator', models.CharField(help_text='Type designator.', max_length=8, verbose_name='Aircraft Code')),
                ('category', models.CharField(choices=[('A', 'Amphibian'), ('G', 'Gyrocopter'), ('H', 'Helicopter'), ('L', 'Landplane'), ('S', 'SeaPlane'), ('T', 'Tilt-wing'), ('U', 'Unknown')], default='U', help_text='Category of aircraft', max_length=1, verbose_name='Category')),
                ('engine_type', models.CharField(choices=[('E', 'Electric'), ('J', 'Jet'), ('T', 'Turboprop'), ('P', 'Piston'), ('U', 'Unknown')], default='U', help_text='Type of engine.', max_length=1, verbose_name='Engine Type')),
            ],
            options={
                'managed': True,
                'ordering': ['designator'],
                'verbose_name_plural': 'Aircraft',
                'verbose_name': 'Aircraft',
            },
        ),
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.AutoField(help_text='Unique OpenFlights identifier for this airline.', primary_key=True, serialize=False, verbose_name='Airline ID')),
                ('name', models.CharField(blank=True, default='', help_text='Name of airline.', max_length=128, verbose_name='Name')),
                ('alias', models.CharField(blank=True, default='', help_text='Alias of the airline.', max_length=128, verbose_name='Name')),
                ('iata', models.CharField(blank=True, default='', help_text='2-letter IATA code, if available.', max_length=2, verbose_name='IATA')),
                ('icao', models.CharField(blank=True, default='', help_text='3-letter IATA code, if available.', max_length=3, verbose_name='ICAO')),
                ('callsign', models.CharField(blank=True, default='', help_text='Airline callsign.', max_length=128, verbose_name='Callsign')),
                ('is_active', models.BooleanField(default=False, help_text='Whether the airline is or has until recently been operational. This field is not reliable.', verbose_name='Is Active')),
            ],
            options={
                'managed': True,
                'ordering': ['iata'],
                'verbose_name_plural': 'Airlines',
                'verbose_name': 'Airline',
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(help_text='Unique OpenFlights identifier for this airport.', primary_key=True, serialize=False, verbose_name='Airport ID')),
                ('name', models.CharField(blank=True, default='', help_text='Name of airport. May or may not contain the City name.', max_length=128, verbose_name='Name')),
                ('city', models.CharField(blank=True, default='', help_text='Main city served by airport. May be spelled differently from Name.', max_length=128, verbose_name='City')),
                ('iata', models.CharField(blank=True, default='', help_text='3-letter FAA code if located in USA, 3-letter IATA code, for all others. Blank if not assigned.', max_length=3, verbose_name='IATA/FAA')),
                ('icao', models.CharField(blank=True, default='', help_text='4-letter ICAO code. Blank if not assigned.', max_length=4, verbose_name='ICAO')),
                ('latitude', models.DecimalField(decimal_places=6, help_text='Decimal degrees, usually to six significant digits. Negative is South, positive is North.', max_digits=11, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=6, help_text='Decimal degrees, usually to six significant digits. Negative is West, positive is East.', max_digits=11, verbose_name='Longitude')),
                ('altitude', models.IntegerField(help_text='In feet.', verbose_name='Altitude')),
                ('timezone', models.DecimalField(decimal_places=2, help_text='Hours offset from UTC. Fractional hours are expressed as decimals, eg. India is 5.5.', max_digits=4, verbose_name='Time Zone')),
                ('dst', models.CharField(choices=[('E', 'Europe'), ('A', 'US/Canada'), ('S', 'South America'), ('O', 'Australia'), ('Z', 'New Zealand'), ('N', 'None'), ('U', 'Unknown')], default='U', help_text='Daylight savings time.', max_length=2, verbose_name='DST')),
                ('tz_db', models.CharField(blank=True, default='', help_text="Timezone in 'tz' (Olson) format, eg., 'America/Los_Angeles'.", max_length=128, verbose_name='TZ Database Time Zone')),
            ],
            options={
                'managed': True,
                'ordering': ['iata'],
                'verbose_name_plural': 'Airports',
                'verbose_name': 'Airport',
            },
        ),
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=64, verbose_name='Name')),
                ('airlines', models.ManyToManyField(to='ofd.Airline')),
            ],
            options={
                'verbose_name_plural': 'Alliances',
                'verbose_name': 'Alliance',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('iso_code2', models.CharField(blank=True, default='', max_length=2, verbose_name='ISO 2')),
                ('iso_code3', models.CharField(blank=True, default='', max_length=3, verbose_name='ISO 3')),
                ('un_m49', models.IntegerField(blank=True, null=True, verbose_name='UN M.49 Numeric Code')),
                ('name', models.CharField(blank=True, default='', help_text='Country or territory', max_length=128, verbose_name='Country Name')),
            ],
            options={
                'managed': True,
                'ordering': ['iso_code2', 'name'],
                'verbose_name_plural': 'Countries',
                'verbose_name': 'Country',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valid_from', models.DateField(blank=True, null=True, verbose_name='Valid From')),
                ('valid_to', models.DateField(blank=True, null=True, verbose_name='Valid To')),
                ('dow_1Su', models.BooleanField(default=True, verbose_name='Sun')),
                ('dow_2Mo', models.BooleanField(default=True, verbose_name='Mon')),
                ('dow_3Tu', models.BooleanField(default=True, verbose_name='Tue')),
                ('dow_4We', models.BooleanField(default=True, verbose_name='Wed')),
                ('dow_5Th', models.BooleanField(default=True, verbose_name='Thu')),
                ('dow_6Fr', models.BooleanField(default=True, verbose_name='Fri')),
                ('dow_7Sa', models.BooleanField(default=True, verbose_name='Sat')),
                ('departs_local', models.TimeField(blank=True, verbose_name='Departs')),
                ('flight_duration', models.DurationField(blank=True, editable=False, null=True)),
                ('arrives_local', models.TimeField(blank=True, verbose_name='Arrives')),
                ('arrives_day_offset', models.IntegerField(default=0, help_text='This is the number of dates earlier or later you arrive. For instance, if the flight lands at 2:00am, then this should be 1, because it is the next day.', verbose_name='Day Offset')),
                ('airport_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='airport_from_rel', to='ofd.Airport', verbose_name='From')),
                ('airport_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='airport_to_rel', to='ofd.Airport', verbose_name='To')),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ofd.Aircraft', verbose_name='Aircraft')),
                ('operator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ofd.Airline', verbose_name='Operated By')),
            ],
            options={
                'verbose_name_plural': 'Flights',
                'verbose_name': 'Flight',
            },
        ),
        migrations.CreateModel(
            name='FlightNumber',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ofd.Airline')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ofd.Flight')),
            ],
            options={
                'verbose_name_plural': 'Flight Numbers',
                'verbose_name': 'Flight Number',
            },
        ),
        migrations.AddField(
            model_name='airport',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ofd.Country'),
        ),
        migrations.AddField(
            model_name='airline',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ofd.Country', verbose_name='Country'),
        ),
    ]