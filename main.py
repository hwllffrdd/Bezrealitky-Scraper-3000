from bs4 import BeautifulSoup
import requests
import csv
import random
import re
from time import sleep

base_url = "https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&regionOsmIds=R435514&osm_value=Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&location=exact&currency=CZK"
start_page = 1
end_page = 78

all_names = []
all_types = []
all_areas = []
all_notes = []
all_prices = []

for page in range(start_page, end_page + 1):

    url = f"{base_url}&page={page}"
    print("Fetching data from:", url)
    response = requests.get(url)
    print("Status code:", response.status_code)
    if response.status_code != 200:
        continue
    response.encoding = 'utf-8'
    bezrealitky_page = response.text
    soup = BeautifulSoup(bezrealitky_page, "lxml")

    names = soup.find_all(class_="PropertyCard_propertyCardAddress__hNqyR")
    names_text = [name.getText() for name in names]
    all_names.extend(names_text)

    dispositions = soup.find_all(class_="FeaturesList_featuresListItem__RYf_f")
    dispositions_text1 = [disposition.getText() for disposition in dispositions]
    dispositions_text = [disposition.replace(" m²", "") for disposition in dispositions_text1]
    for disposition in dispositions_text:
        if "kk" in disposition or "+" in disposition or "Garsoniéra" in disposition:
            all_types.append(disposition)
        else:
            cleaned_area = re.sub(r'\D', '', disposition)
            all_areas.append(cleaned_area)

    notes = soup.find_all(class_="mt-2 mt-md-3 mb-0 text-caption text-truncate-multiple")
    notes_text = [note.getText() for note in notes]
    all_notes.extend(notes_text)

    prices = soup.find_all(class_="PropertyPrice_propertyPriceAmount__WdEE1")
    prices_text1 = [price.getText() for price in prices]
    prices_text2 = [price.replace("\xa0", "") for price in prices_text1]
    prices_text = [price.replace("Kč", "") for price in prices_text2]
    all_prices.extend(prices_text)

    sleep(random.randint(5, 15))


csv_file_path = 'output_data.csv'

print(all_names)

with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')

    writer.writerow(['Name', 'Type', 'Area', 'Notes', 'Price'])

    for name, type_, area, note, price in zip(all_names, all_types, all_areas, all_notes, all_prices):
        writer.writerow([name, type_, area, note, price])

print("Data has been written to", csv_file_path)










