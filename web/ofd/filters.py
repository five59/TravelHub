from django.contrib import admin
from ofd.models import *

class AirportHasIcaoFilter(admin.SimpleListFilter):
    title = u'ICAO Code'
    parameter_name = 'check_icao'
    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Assigned'),
            ('No', 'Unassigned'),
        )
    def queryset(self,request,queryset):
        if self.value() == 'No':
            return queryset.filter(icao__exact='')
        if self.value() == 'Yes':
            return queryset.exclude(icao__exact='')

class AirportHasIataFaaFilter(admin.SimpleListFilter):
    title = u'IATA/FAA Code'
    parameter_name = 'check_iata_faa'
    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Assigned'),
            ('No', 'Unassigned'),
        )
    def queryset(self,request,queryset):
        if self.value() == 'No':
            return queryset.filter(iata_faa__exact='')
        if self.value() == 'Yes':
            return queryset.exclude(iata_faa__exact='')

class AirlineHasIcaoFilter(admin.SimpleListFilter):
    title = u'ICAO Code'
    parameter_name = 'check_icao'
    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Assigned'),
            ('No', 'Unassigned'),
        )
    def queryset(self,request,queryset):
        if self.value() == 'No':
            return queryset.filter(icao__exact='')
        if self.value() == 'Yes':
            return queryset.exclude(icao__exact='')

class AirlineHasIataFaaFilter(admin.SimpleListFilter):
    title = u'IATA Code'
    parameter_name = 'check_iata_faa'
    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Assigned'),
            ('No', 'Unassigned'),
        )
    def queryset(self,request,queryset):
        if self.value() == 'No':
            return queryset.filter(iata__exact='')
        if self.value() == 'Yes':
            return queryset.exclude(iata__exact='')
