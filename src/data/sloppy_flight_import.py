from ofd.models import *
import csv, io, sys
from datetime import datetime, time
import time

fh = open("./data/flight_test1.txt","r")

al_dl = Airline.objects.get(iata="DL")
al_kl = Airline.objects.get(iata="KL")
al_af = Airline.objects.get(iata="AF")

def convert_to_time(val):
    # expects a 5-character string, eg 00:00
    h = int("{}{}".format(val[0],val[1]))
    m = int("{}{}".format(val[3],val[4]))
    return datetime.time(hour=h, minute=m)

for line in csv.reader(fh, dialect="excel-tab"):
    print("--> Read {} {}".format(line[0], line[18]))

    try:
        obj_airport_from = Airport.objects.get(iata=line[0])
    except:
        print("FROM Airport {} not found.".format(line[0]))

    try:
        obj_airport_to = Airport.objects.get(iata=line[18])
    except:
        print("TO Airport {} not found.".format(line[18]))

    try:
        obj_operator = Airline.objects.get(iata=line[14])
    except:
        print("Airline {} not found.".format(line[14]))

    def clean_int(val):
        try:
            if val > 0:
                return val
            else:
                return 0
        except:
            return 0

    def clean_bool(val):
        if val:
            return val
        else:
            return False

    obj_equipment, ok = Aircraft.objects.get_or_create(designator=line[15])

    obj, created = Flight.objects.get_or_create(
        airport_from=obj_airport_from,
        airport_to=obj_airport_to,
        operator=obj_operator,
        equipment=obj_equipment,
        arrives_day_offset=clean_int(line[13]),
        departs_local = datetime.strptime(line[11], '%H:%M'),
        arrives_local = datetime.strptime(line[12], '%H:%M'),
        valid_from=datetime.strptime(line[2], '%Y-%m-%d'),
        valid_to=datetime.strptime(line[3], '%Y-%m-%d'),
        dow_1Su=clean_bool(line[4]),
        dow_2Mo=clean_bool(line[5]),
        dow_3Tu=clean_bool(line[6]),
        dow_4We=clean_bool(line[7]),
        dow_5Th=clean_bool(line[8]),
        dow_6Fr=clean_bool(line[9]),
        dow_7Sa=clean_bool(line[10]),
    )
    obj.save()
    if clean_int(line[16]):
        fl = FlightNumber(
            flight=obj,
            airline=al_dl,
            number=line[16]
        )
        fl.save()
    if clean_int(line[17]):
        fl = FlightNumber(
            flight=obj,
            airline=al_kl,
            number=line[17]
        )
        fl.save()
    if clean_int(line[18]):
        fl = FlightNumber(
            flight=obj,
            airline=al_af,
            number=line[1]
        )
        fl.save()
