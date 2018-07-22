import csv

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "museum_website.settings")
django.setup()

from exhibitions.models import *

if __name__ == "__main__":
    with open('artwork_data.csv', newline='', encoding='utf-8') as art_csv:
        art_reader = csv.reader(art_csv)
        next(art_reader)

        e = Exhibition.objects.get(name="Art from Tate Museum")
        
        for row in art_reader:
            if int(row[0]) % 2 == 0:
                continue

            if Artwork.objects.filter(author=row[2]).count() > 70:
                continue

            if row[2] and row[5] and row[7] and row[9]:
                if row[5] == "[title not known]":
                    continue
                    
                if ',' in row[2]:
                    last_name = row[2].split(",")[0]
                    full_name = row[2].split(", ")[1] + " " + last_name

                if not Artwork.objects.filter(author=row[2], name=row[5], art_type=row[7], year=row[9], exhibition=e).exists():
                        print(row[0], row[2], row[5], row[9])
                        Artwork.objects.create(author=row[2], name=full_name, art_type=row[7], year=row[9], exhibition=e)
                