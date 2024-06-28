from bs4 import BeautifulSoup
import requests
import csv
import random
import re
from time import sleep

base_url = "https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&regionOsmIds=R435514&osm_value=Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&location=exact&currency=CZK"
start_page = 1
end_page = 77

csv_file_path = 'output_data.csv'
with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Name', 'Type', 'Area', 'Notes', 'Price'])

    for page in range(start_page, end_page + 1):
        url = f"{base_url}&page={page}"
        print("Fetching data from:", url)
        response = requests.get(url)
        print("Status code:", response.status_code)
        if response.status_code != 200:
            continue
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")

        listings = soup.find_all(class_="PropertyCard_propertyCard__moO_5")
        for listing in listings:
            name = listing.find(class_="PropertyCard_propertyCardAddress__hNqyR").getText(strip=True)
            type_ = listing.find(class_="FeaturesList_featuresListItem__RYf_f").getText(strip=True)
            area = re.sub(r'\D', '', listing.find_all(class_="FeaturesList_featuresListItem__RYf_f")[1].getText()) if len(
                listing.find_all(class_="FeaturesList_featuresListItem__RYf_f")) > 1 else 'N/A'
            note = listing.find(class_="mt-2 mt-md-3 mb-0 text-caption text-truncate-multiple").getText(
                strip=True) if listing.find(class_="mt-2 mt-md-3 mb-0 text-caption text-truncate-multiple") else 'N/A'
            price = re.sub(r'[^\d]', '', listing.find(class_="PropertyPrice_propertyPriceAmount__WdEE1").getText())

            writer.writerow([name, type_, area, note, price])

        sleep(random.randint(5, 15))

print("Data has been written to", csv_file_path)






