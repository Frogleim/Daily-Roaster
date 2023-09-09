import re
import time
from util import files_reader, image_downloader, driver_provider
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import os

current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
data_directory = os.path.join(parent_directory, 'roster_scraper\\images')
print(data_directory)


class URLScraper:
    def __init__(self, county_name=None):
        self.driver = driver_provider.create_firefox_driver()
        self.inmates_data = []
        self.website_file = files_reader.read_websites_json()
        self.jail_name = ''
        self.county_name = county_name

    def scrap_inmates_url(self):
        website_index = 0
        for websites_data in self.website_file['websites']:
            inmates_data = []
            self.jail_name = websites_data['data']['county_name']
            website_index += 1
            self.driver.get(websites_data['data']['first_page_url'])
            soup = BS(self.driver.page_source, "html.parser")
            content_div = soup.find_all("div", {'class': "column large-8 cell inmate_data"})
            for profiles_ids in content_div:
                all_a_elements = profiles_ids.find("a", class_="text2")['href']
                print(f'{websites_data["data"]["profiles_url"]}{all_a_elements}')

                d = {
                    'url': f'{websites_data["data"]["profiles_url"]}{all_a_elements}'

                }
                inmates_data.append(d)
            files_reader.save_daily_urls_json(self.jail_name, inmates_data)


class InmatesScraper:
    def __init__(self, county_name=None):
        self.driver = driver_provider.create_firefox_driver()
        self.data = files_reader.xpath_reader(county_name)

    def scrap_inmates_data(self):
        print(self.data)
        for profiles in self.data[0:2]:
            urls = files_reader.read_daily_urls_json(profiles['jail_name'])
            profiles_data = []
            for url in urls:
                self.driver.get(url['url'])
                for xpath in profiles['xpath']:
                    name = self.driver.find_element(By.XPATH, xpath["name"]).text
                    img_url = self.driver.find_element(By.XPATH, xpath['image_path']).get_attribute("src")
                    try:
                        age = self.driver.find_element(By.XPATH, xpath['age']).text
                    except Exception:
                        age = None
                    try:
                        gender = self.driver.find_element(By.XPATH, xpath['gender']).text
                    except Exception:
                        gender = None
                    try:
                        race = self.driver.find_element(By.XPATH, xpath['race']).text
                    except Exception:
                        race = None
                    try:
                        address = self.driver.find_element(By.XPATH, xpath['address']).text
                    except Exception:
                        address = None
                    try:
                        booking_date = self.driver.find_element(By.XPATH, xpath['booking_date']).text
                    except Exception:
                        booking_date = None
                    try:
                        charges = self.driver.find_element(By.XPATH, xpath['charges']).text
                    except Exception:
                        charges = None
                    try:
                        bond = self.driver.find_element(By.XPATH, xpath['bond']).text
                    except Exception:
                        bond = None
                    if "pna.gif" in img_url:
                        img_url = None
                    new_dir_name = f'{data_directory}\\daily_images\\images_{profiles["jail_name"]}'
                    # Check if the directory already exists
                    if not os.path.exists(new_dir_name):
                        # Create the directory
                        os.makedirs(new_dir_name)
                        print(f"Directory '{new_dir_name}' created successfully.")
                    else:
                        print(f"Directory '{new_dir_name}' already exists.")
                    dir_name = f'images_{profiles["jail_name"]}'
                    image_downloader.download_daily_image(name, address, img_url, dir_name, profiles["jail_name"])
                    profiles_dict = {
                        "name": name.title(),
                        "age": age,
                        "gender": gender,
                        "race": race,
                        "Address": address,
                        "booking_date": booking_date,
                        "charges": charges,
                        "bond": bond
                    }
                    profiles_data.append(profiles_dict)
                    print(profiles_data)
            files_reader.save_daily_json(profiles['jail_name'], profiles_data)


if __name__ == "__main__":
    url = "https://www.crosscountysheriff.org/roster.php?grp=40&grp=20"
    jail_name = 'Escambia County'
    print("Scraping URLs...")
    my_scraper = URLScraper()
    my_scraper.scrap_inmates_url()
    inmates_scraper = InmatesScraper()
    inmates_scraper.scrap_inmates_data()
