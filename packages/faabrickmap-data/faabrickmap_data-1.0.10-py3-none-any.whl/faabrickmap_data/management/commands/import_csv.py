from django.core.management.base import BaseCommand, CommandError
from faabrickmap_data.models import Societe
import csv, time
from geopy.geocoders import Nominatim

class Command(BaseCommand):
    help = 'Import society list via CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    def handle(self, *args, **options):
        nb = 0
        for row in csv.reader(open(options['csv_file'], 'rt')):
            time.sleep(0.5)
            # limit field size
            # strip to x letters because database field is limited to that size
            name = row[0][:min(len(row[0]), 250)]
            logo = row[1][:min(len(row[1]), 250)]
            activity = row[2][:min(len(row[2]), 250)]
            siren = row[3][:min(len(row[3]), 15)]
            address = row[4][:min(len(row[4]), 250)]
            postcode = row[5][:min(len(row[5]), 5)]
            city = row[6][:min(len(row[6]), 30)]
            website = row[7][:min(len(row[7]), 250)]
            mail = row[8][:min(len(row[8]), 50)]
            phone = row[9][:min(len(row[9]), 20)]

            geolocator = Nominatim(user_agent="Faabrick-Cherdet")
            location = geolocator.geocode(address + ',' + postcode + ',' +city)

            if postcode[:2] == "20":
                if postcode[:3] == "201":
                    dpt="2A"
                else:
                    dpt="2B"
            elif postcode[:2] == "97":
                dpt=postcode[:3]
            else:
                dpt=postcode[:2]

            if not location:
                lat=None
                lng=None
                self.stdout.write("coordonées non trouvées pour la société " + name+ " : " + address + ', ' + postcode + ' ' + city)
            else:
                lat=str(location.latitude)
                lng=str(location.longitude)
            societe = Societe(
                name=name,
                logo=logo,
                activity_id=activity,
                siren=siren,
                address=address,
                postcode=postcode,
                city=city,
                website=website,
                mail=mail,
                phone=phone,
                lat=lat,
                lng=lng,
                dpt=dpt
            )
            societe.save()
            nb += 1

        self.stdout.write(self.style.SUCCESS(str(nb) + ' society imported successfully'))

