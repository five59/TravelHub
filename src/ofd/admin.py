from django.contrib import admin
from ofd.models import *
from ofd.filters import *

class AirportAdmin(admin.ModelAdmin):
    list_display=['name','iata_faa','icao','city','country']
    list_filter=['dst', AirportHasIcaoFilter, AirportHasIataFaaFilter]
    search_fields=['iata_faa','icao','city','country',]

class AirlineAdmin(admin.ModelAdmin):
    list_display=['name','alias','iata','icao','callsign','country']
    list_filter=['is_active', AirlineHasIcaoFilter, AirlineHasIataFaaFilter, 'country']
    search_fields=['iata','icao','country','name','callsign']

class RouteAdmin(admin.ModelAdmin):
    pass

class AircraftAdmin(admin.ModelAdmin):
    list_display=['designator','manufacturer','model','category','engine_type','engine_count']
    list_filter=['engine_type','category',]
    search_fields=['manufacturer','model','designator']

class CountryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Airport, AirportAdmin)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Country, CountryAdmin)
