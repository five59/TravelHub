from django.db import models

class Country(models.Model):
    id=models.AutoField(primary_key=True)
    iso_code=models.CharField(
        max_length=2,
        verbose_name="Country ISO Code (2-letter)"
    )
    name=models.CharField(
        max_length=128,
        blank=True,
        default="",
        verbose_name="Country Name",
        help_text="Country or territory")
    class Meta:
        verbose_name='Country'
        verbose_name_plural='Countries'
        ordering=['iso_code',]
        managed=True
    def __unicode__(self):
        return self.name

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
        max_length=64,
        verbose_name="Manufacturer",
        help_text="The name of the manufacturer.")
    model=models.CharField(
        max_length=32,
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
    engine_count=models.IntegerField(
        verbose_name="Engines",
        help_text="Number of Engines"
    )
    class Meta:
        verbose_name='Aircraft'
        verbose_name_plural='Aircraft'
        ordering=['designator',]
        managed=True
    def __unicode__(self):
        return self.code

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
    country=models.ForeignKey(Country)
    iata_faa=models.CharField(
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
        if not self.iata_faa:
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
        ordering=['iata_faa',]
        managed=True
    def __unicode__(self):
        return self.name

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
    country=models.ForeignKey(Country)
    is_active=models.BooleanField(
        default=False,
        verbose_name="Is Active",
        help_text="Whether the airline is or has until recently been operational. This field is not reliable.")
    class Meta:
        verbose_name='Airline'
        verbose_name_plural='Airlines'
        ordering=['iata',]
        managed=True
    def __unicode__(self):
        return self.name

class Route(models.Model):
    """As of January 2012, the OpenFlights/Airline Route Mapper Route Database contains 59036 routes between 3209 airports on 531 airlines spanning the globe."""
    id=models.AutoField(
        primary_key=True)
    airline=models.ForeignKey(
        Airline)
    airport_from=models.ForeignKey(
        Airport,
        related_name="airport_from_rel")
    airport_to=models.ForeignKey(
        Airport,
        related_name="airport_to_rel")
    is_codeshare=models.BooleanField(
        default=False,
        verbose_name="Is Codeshare",
        help_text="Is this flight is a codeshare (that is, not operated by Airline, but another carrier).")
    stops=models.IntegerField(
        default=0,
        verbose_name="Stops",
        help_text="Number of stops on this flight. 0=nonstop."
    )
    equipment=models.ManyToManyField(Aircraft)
    class Meta:
        verbose_name='Route'
        verbose_name_plural='Routes'
        ordering=['airline','airport_from','airport_to']
        managed=True
    def __unicode__(self):
        return u'%s (%s-%s)' % (['airline','airport_from','airport_to'])
