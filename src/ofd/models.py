from django.db import models
from durationfield.db.models.fields.duration import DurationField
import datetime

class Country(models.Model):
    id=models.AutoField(primary_key=True)
    iso_code2 = models.CharField(max_length=2, blank=True, default="",
            verbose_name="ISO 2")
    iso_code3 = models.CharField(max_length=3, blank=True, default="",
            verbose_name="ISO 3")
    un_m49 = models.IntegerField(blank=True, null=True, verbose_name="UN M.49 Numeric Code")
    name=models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="Country Name",
        help_text="Country or territory")
    class Meta:
        verbose_name='Country'
        verbose_name_plural='Countries'
        ordering=['iso_code2','name',]
        managed=True
    def __str__(self):
        if self.iso_code2:
            rv = "{}: {}".format(self.iso_code2, self.name)
        else:
            rv = "__: {}".format(self.name)
        return rv

class Aircraft(models.Model):
    """
    Aircraft, as described by ICAO DOC 8643 - Aircraft Type Designators
    http://www.icao.int/publications/DOC8643/
    """
    CATEGORY_CHOICES = (
        ('A','Amphibian'),
        ('G','Gyrocopter'),
        ('H','Helicopter'),
        ('L','Landplane'),
        ('S','SeaPlane'),
        ('T','Tilt-wing'),
        ('U','Unknown'),
    )
    ENGINE_CHOICES = (
        ('E','Electric'),
        ('J','Jet'),
        ('T','Turboprop'),
        ('P','Piston'),
        ('U','Unknown'),
    )
    id=models.AutoField(primary_key=True)
    manufacturer=models.CharField(
        default="", blank=True,
        max_length=64,
        verbose_name="Manufacturer",
        help_text="The name of the manufacturer.")
    model=models.CharField(
        max_length=32,
        default="", blank=True,
        verbose_name="Model Name",
        help_text="The model name of the aircraft.")
    designator=models.CharField(
        max_length=8,
        verbose_name="Aircraft Code",
        help_text="Type designator.")
    category=models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='U',
        verbose_name="Category",
        help_text="Category of aircraft")
    engine_type=models.CharField(
        max_length=1,
        choices=ENGINE_CHOICES,
        default='U',
        verbose_name="Engine Type",
        help_text="Type of engine.")
    # engine_count=models.IntegerField(
    #     default="", blank=True,
    #     verbose_name="Engines",
    #     help_text="Number of Engines"
    # )
    def __str__(self):
        rv = "{}: {}".format(self.designator, self.model)
        return rv
    class Meta:
        verbose_name='Aircraft'
        verbose_name_plural='Aircraft'
        ordering=['designator',]
        managed=True

class Airport(models.Model):
    """Airports. As of January 2012, the OpenFlights Airports Database
    contains 6977 airports spanning the globe."""
    DST_CHOICES = (
        ('E', 'Europe'),
        ('A', 'US/Canada'),
        ('S', 'South America'),
        ('O', 'Australia'),
        ('Z', 'New Zealand'),
        ('N', 'None'),
        ('U', 'Unknown'),
    )
    id=models.AutoField(
        primary_key=True,
        verbose_name="Airport ID",
        help_text="Unique OpenFlights identifier for this airport.")
    name=models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="Name",
        help_text="Name of airport. May or may not contain the City name.")
    city=models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="City",
        help_text="Main city served by airport. May be spelled differently from Name.")
    country=models.ForeignKey(Country, blank=True, null=True)
    iata=models.CharField(
        max_length=3,
        blank=True,
        default="",
        verbose_name="IATA/FAA",
        help_text="3-letter FAA code if located in USA, 3-letter IATA code, for all others. Blank if not assigned.")
    icao=models.CharField(
        max_length=4,
        blank=True,
        default="",
        verbose_name="ICAO",
        help_text="4-letter ICAO code. Blank if not assigned.")
    latitude=models.DecimalField(
        max_digits=11,
        decimal_places=6,
        verbose_name="Latitude",
        help_text="Decimal degrees, usually to six significant digits. Negative is South, positive is North.")
    longitude=models.DecimalField(
        max_digits=11,
        decimal_places=6,
        verbose_name="Longitude",
        help_text="Decimal degrees, usually to six significant digits. Negative is West, positive is East.")
    altitude=models.IntegerField(
        verbose_name="Altitude",
        help_text="In feet.")
    timezone=models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Time Zone",
        help_text="Hours offset from UTC. Fractional hours are expressed as decimals, eg. India is 5.5.")
    dst=models.CharField(
        max_length=2,
        choices=DST_CHOICES,
        default='U',
        verbose_name="DST",
        help_text="Daylight savings time.")
    tz_db=models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="TZ Database Time Zone",
        help_text="Timezone in 'tz' (Olson) format, eg., 'America/Los_Angeles'.")
    def has_iata_faa(self):
        if not self.iata:
            rv = False
        else:
            rv=True
        return rv
    has_iata_faa.short_description="Has IATA Code"
    def has_icao(self):
        if not self.icao:
            rv = False
        else:
            rv=True
        return rv
    has_icao.short_description="Has ICAO Code"
    class Meta:
        verbose_name='Airport'
        verbose_name_plural='Airports'
        ordering=['iata',]
        managed=True
    def __str__(self):
        if self.iata:
            rv = "{}: {}".format(self.iata, self.name)
        else:
            rv = "___: {}".format(self.name)
        return rv

class Airline(models.Model):
    """As of January 2012, the OpenFlights Airlines Database contains 5888 airlines."""
    id=models.AutoField(
        primary_key=True,
        verbose_name="Airline ID",
        help_text="Unique OpenFlights identifier for this airline.")
    name=models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="Name",
        help_text="Name of airline.")
    alias=models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="Name",
        help_text="Alias of the airline.")
    iata=models.CharField(
        max_length=2,
        blank=True,
        default="",
        verbose_name="IATA",
        help_text="2-letter IATA code, if available.")
    icao=models.CharField(
        max_length=3,
        blank=True,
        default="",
        verbose_name="ICAO",
        help_text="3-letter IATA code, if available.")
    callsign=models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="Callsign",
        help_text="Airline callsign.")
    country=models.ForeignKey(Country, null=True, blank=True, verbose_name="Country")
    is_active=models.BooleanField(
        default=False,
        verbose_name="Is Active",
        help_text="Whether the airline is or has until recently been operational. This field is not reliable.")
    class Meta:
        verbose_name='Airline'
        verbose_name_plural='Airlines'
        ordering=['iata',]
        managed=True
    def __str__(self):
        if self.iata:
            rv = "{}: {}".format(self.iata, self.name)
        else:
            rv = "___: {}".format(self.name)
        return rv

class Alliance(models.Model):
    """( Alliance description)"""
    id=models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=64, default="", blank=True, verbose_name="Name")
    airlines = models.ManyToManyField(Airline)
    def get_num_members(self):
        rv = self.airlines.count()
        return rv
    get_num_members.short_description="Member Count"
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Alliance"
        verbose_name_plural = "Alliances"

class Flight(models.Model):
    id=models.AutoField(primary_key=True)
    valid_from = models.DateField(verbose_name="Valid From", null=True, blank=True)
    valid_to = models.DateField(verbose_name="Valid To", null=True, blank=True)

    dow_1Su = models.BooleanField(verbose_name="Sun", default=True)
    dow_2Mo = models.BooleanField(verbose_name="Mon", default=True)
    dow_3Tu = models.BooleanField(verbose_name="Tue", default=True)
    dow_4We = models.BooleanField(verbose_name="Wed", default=True)
    dow_5Th = models.BooleanField(verbose_name="Thu", default=True)
    dow_6Fr = models.BooleanField(verbose_name="Fri", default=True)
    dow_7Sa = models.BooleanField(verbose_name="Sat", default=True)

    airport_from=models.ForeignKey(Airport, related_name="airport_from_rel", verbose_name="From", null=True, blank=True)
    departs_local = models.TimeField(verbose_name="Departs", blank=True)
    flight_duration = models.DurationField(editable=False, blank=True, null=True)

    airport_to=models.ForeignKey(Airport, related_name="airport_to_rel", verbose_name="To", null=True, blank=True)
    arrives_local = models.TimeField(verbose_name="Arrives", blank=True)
    arrives_day_offset = models.IntegerField(default=0, verbose_name="Day Offset",
        help_text="This is the number of dates earlier or later you arrive. For instance, if the flight lands at 2:00am, then this should be 1, because it is the next day.")

    operator = models.ForeignKey(Airline, blank=True, verbose_name="Operated By")
    equipment=models.ForeignKey(Aircraft, blank=True, null=True, verbose_name="Aircraft")

    # TODO
    # def is_valid(date=now)


    def calculate_flight_duration(self):
        # Calculate delta in MINUTES
        delt = (
            ( self.arrives_local.hour - self.departs_local.hour )*60
            + ( self.arrives_local.minute - self.departs_local.minute)
            + self.arrives_day_offset * 1440
            + (self.airport_from.timezone - self.airport_to.timezone)*60
            )
        if delt < 0:
            delt += 1440
        hh,rem = divmod(delt,60)
        hh = int(hh)
        mm = int(rem)
        return datetime.timedelta(hours=hh, minutes=mm)


    def save(self, *args, **kwargs):
        # Calculate duration of flight.
        # TODO FIXME
        # self.flight_duration = self.calculate_flight_duration()
        super(Flight, self).save(*args, **kwargs)

    def get_daysummary(self):
        vals = [
            [self.dow_1Su,"Su"],
            [self.dow_2Mo,"Mo"],
            [self.dow_3Tu,"Tu"],
            [self.dow_4We,"We"],
            [self.dow_5Th,"Th"],
            [self.dow_6Fr,"Fr"],
            [self.dow_7Sa,"Sa"],
        ]
        rv = ""
        for v in vals:
            if v[0]:
                rv = rv + v[1]
            else:
                rv = rv + "--"
        return rv
    get_daysummary.short_description="Days"

    def get_flightnumber(self, with_ac=True):
        """ Returns the primary flight number based on the operating airline.
            Optional 'with_ac' parameter to return with airline code.
        """
        try:
            fn = FlightNumber.objects.get(flight=self, airline=self.operator)
            if with_ac:
                fn = "{} {:4}".format(fn.airline.iata, fn.number)
            else:
                fn = "{}".format(fn.number)
        except:
            fn = "{} to {}".format(self.airport_from,self.airport_to)
        return fn
    get_flightnumber.short_description="Flight Number"

    def __str__(self):
        return self.get_flightnumber()
    class Meta:
        verbose_name = "Flight"
        verbose_name_plural = "Flights"


class FlightNumber(models.Model):
    id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(Flight)
    airline = models.ForeignKey(Airline)
    number = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return "{} {:4}".format(self.airline.iata, self.number)
    class Meta:
        verbose_name = "Flight Number"
        verbose_name_plural = "Flight Numbers"
