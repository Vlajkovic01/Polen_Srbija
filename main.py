import time

import requests
import os.path as io
from datetime import date, timedelta
from colorama import Fore, Style


def main():
    if not io.isfile("locations.txt"):
        create_file()
    print("-------=[ POLEN U SRBIJI ]=-------")
    print("____________________________________")
    time.sleep(1)
    read_file()

    find_pollen_value(request_pollen())


def create_file():
    locations_list = request_locations()
    write_locations_to_file(locations_list)


def read_file():
    locations = open("locations.txt", "r", encoding="utf-8")
    for line in locations:
        print(line, end="")
    locations.close()


def write_locations_to_file(locations_list):
    file = open("locations.txt", "w", encoding="utf-8")
    for item in locations_list:
        file.write(f"{str(item['id'])} | {item['name']} - {item['description']}\n")
    file.close()


def find_pollen_value(pollen):
    for item in pollen:
        print(f"Za datum: {Fore.BLUE}{item['date']}{Style.RESET_ALL}")
        for inner_item in item['concentrations']:
            define_pollen_value(request_concentrations(inner_item)['value'],
                                request_allergen(request_concentrations(inner_item)))


def define_pollen_value(current_value, allergen):
    if current_value > allergen['margine_top']:
        return print(f"\tKoncentracija polena {allergen['localized_name']} ({allergen['name']}) je visoka!!!")
    elif allergen['margine_top'] >= current_value >= allergen['margine_bottom']:
        return print(f"\tKoncentracija polena {allergen['localized_name']} ({allergen['name']}) je srednja!")
    else:
        return print(f"\tKoncentracija polena {allergen['localized_name']} ({allergen['name']}) je niska.")


def request_concentrations(inner_item):
    concentrations = requests.get(f"http://polen.sepa.gov.rs/api/opendata/concentrations/{inner_item}")
    concentrations = concentrations.json()
    return concentrations


def request_allergen(concentrations):
    allergen = requests.get(f"http://polen.sepa.gov.rs/api/opendata/allergens/{concentrations['allergen']}")
    allergen = allergen.json()
    return allergen


def request_locations():
    locations_list = requests.get("http://polen.sepa.gov.rs/api/opendata/locations/")
    locations_list = locations_list.json()
    locations_list = sorted(locations_list, key=lambda k: k['id'])
    return locations_list


def request_pollen():
    location = input("Unesi broj mesta: ")

    pollen = requests.get(
        f"http://polen.sepa.gov.rs/api/opendata/pollens/?location={location}&date_after={define_date()}")
    pollen = pollen.json()
    pollen = pollen['results']
    return pollen


def define_date():
    days_num = input("Unesi broj dana: ")
    starting_date = date.today() - timedelta(6 + int(days_num))
    return starting_date


if __name__ == '__main__':
    main()
