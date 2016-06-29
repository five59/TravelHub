from .models import *

def fix_airport_country(country_str, iso_code2):
    try:
        aps = Airport.objects.filter(country_str__contains=country_str)
    except:
        print("No listings were found.")

    try:
        c = Country.objects.get(iso_code2=iso_code2)
    except:
        print("That country was not found.")

    print("There are {} listings found for {}.".format(aps.count(), c.name))
    for a in aps:
        a.country = c
        a.save()
    
