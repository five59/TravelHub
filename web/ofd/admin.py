from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from ofd.models import *
from ofd.filters import *

class AirportResource(resources.ModelResource):
    class Meta:
        model = Airport
class AirportAdmin(ImportExportModelAdmin):
    list_display=['name','iata','icao','city', 'country',]
    list_filter=['dst', AirportHasIcaoFilter, AirportHasIataFaaFilter, 'country', ]
    search_fields=['iata','icao','city',]

class AirlineResource(resources.ModelResource):
    class Meta:
        model = Airline
class AirlineAdmin(ImportExportModelAdmin):
    list_display=['name','alias','iata','icao','callsign','country', ]
    list_filter=['is_active', AirlineHasIcaoFilter, AirlineHasIataFaaFilter, 'country']
    search_fields=['iata','icao','country','name','callsign']

class AircraftResource(resources.ModelResource):
    class Meta:
        model = Aircraft
class AircraftAdmin(ImportExportModelAdmin):
    list_display=['designator','manufacturer','model','category','engine_type',]
    list_filter=['engine_type','category',]
    search_fields=['manufacturer','model','designator']

class CountryResource(resources.ModelResource):
    class Meta:
        model = Country
class CountryAdmin(ImportExportModelAdmin):
    list_display = ['name','iso_code2','iso_code3',]
    search_fields = ['name','iso_code2','iso_code3',]


class FlightNumberInline(admin.TabularInline):
    model = FlightNumber

class FlightNumberResource(resources.ModelResource):
    id = fields.Field(column_name="id")
    class Meta:
        model = FlightNumber
    def dehydrate_id(self, id):
        return "%s" % (uuid.uuid4())
class FlightNumberAdmin(ImportExportModelAdmin):
    pass

class FlightResource(resources.ModelResource):
    # airport_from = fields.Field(
    #     column_name="airport_from", attribute="airport_from",
    #     widget=ForeignKeyWidget(Airport, 'iata'))
    # airport_to = fields.Field(
    #     column_name="airport_to_iata", attribute="airport_to",
    #     widget=ForeignKeyWidget(Airport, 'iata'))
#    flight_duration = fields.Field(column_name="flight_duration", attribute)
    operator = fields.Field(
        column_name="operator", attribute="operator",
        widget=ForeignKeyWidget(Airline, 'iata'))
    equipment = fields.Field(
        column_name="equipment_name", attribute="equipment",
        widget=ForeignKeyWidget(Aircraft, 'designator'))
    class Meta:
        model = Flight
        fields = ('operator','equipment')

    class Meta:
        fields = ('author',)

    # def dehydrate_airport_from(self, airport_from):
    #     rv = Airport.objects.get(iata=airport_from)
    #     return rv
    # def airport_to.clean(self, airport_to):
    #     rv = Airport.objects.get(iso_code2=airport_to)
    #     return rv
    # def flight_duration.clean(self, flight_duration):
    #     rv = self.calculate_flight_duration()
    #     return rv
    def dehydrate_operator(self, operator):
        rv = Airline.objects.get(iata=operator)
        return rv
    # def equipment.clean(self, equipment):
    #     rv = Aircraft.objects.get(designator=equipment)
    #     return rv

class FlightAdmin(ImportExportModelAdmin):
    list_display = ['get_flightnumber',
        'airport_from', 'departs_local',
        'airport_to', 'arrives_local',
        'operator','equipment',
        'flight_duration', 'get_daysummary',
        'valid_from','valid_to',]
    inlines = (FlightNumberInline, )

class AllianceResource(resources.ModelResource):
    id = fields.Field(column_name="id")
    class Meta:
        model = Alliance
    def dehydrate_id(self, id):
        return "%s" % (uuid.uuid4())
class AllianceAdmin(ImportExportModelAdmin):
    list_display = ['name','get_num_members', ]
    filter_horizontal = ['airlines', ]

admin.site.register(Alliance, AllianceAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Flight, FlightAdmin)
