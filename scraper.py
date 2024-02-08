import argparse
import csv
import json
import sys
from time import sleep

import undetected_chromedriver as uc

from locators import MainLocators, DetailLocators

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--name",
                        "-n",
                        metavar="name",
                        type=str,
                        help="name to search"
                        )
arg_parser.add_argument("--headless",
                        action=argparse.BooleanOptionalAction,
                        help="execute headless mode"
                        )
args = arg_parser.parse_args()
name = args.name or "john"
headless = args.headless


coptions = uc.ChromeOptions()
if headless:
    coptions.add_argument("--headless")


CHROME_TARGET_VERSION = 113
URL_SEARCH = f'https://www.whitepages.com/name/{name.title()}?fs=1&searchedName={name.lower()}'

URL_BASE =  "https://www.whitepages.com"
field_names = set([
                    "name" ,
                    "alias",
                    "age",
                    "location",
                    "address",
                    "properties",
                    "criminal_record",
                    ])


class Scraper():
    """scraper for whitepages"""
    def __init__(self, url): 
        self.url = url
        self.driver = uc.Chrome(
                                version_main = CHROME_TARGET_VERSION,
                                options=coptions)
        self.driver.get(url)
        sleep(3)
        self.total_pages = self.find_element(MainLocators.TOTAL_PAGES)
        self.state_urls = [tag.get_attribute("href") for tag in self.driver.find_elements(*MainLocators.STATES)]
        
        
    def find_element(self, locator):
        """search text element in driver"""
        try:
            text = self.driver.find_element(*locator).text
        except Exception as error:
            text = "-"
            pass
        return text

    def to_csv(self, contents):
        """export all data to csv"""
        with open(f'{name}.csv', "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)    
            writer.writeheader()
            writer.writerows(contents)

    def extract_url_details(self):
        """extract all the details uris of all pages in every state"""
        detail_urls = []
        for state_url in self.state_urls:
            self.driver.get(state_url)
            sleep(0.3)
            for page in range(1, int(self.total_pages)):
                self.driver.get(f'{state_url}&page={page}')
                details = self.driver.find_elements(*MainLocators.VIEW_DETAILS)
                for detail in details:
                    uri = detail.get_attribute("href")
                    print(f'uri: {uri}')
                    detail_urls.append(uri)
                return detail_urls

    def extract_details(self, uris):
        """extract all the details from uris"""
        persons = []
        for uri in uris:
            self.driver.get(f'{URL_BASE}{uri}')
            sleep(1.5)
            person = {
                "name" : self.find_element(DetailLocators.NAME),
                "alias" : self.find_element(DetailLocators.ALIAS).replace("(", "").replace(")", ""),
                "age" : self.find_element(DetailLocators.AGE),
                "location" : self.find_element(DetailLocators.LOCATION),
                "address" : self.find_element(DetailLocators.ADDRESS),
                "properties" : self.find_element(DetailLocators.PROPERTIES),
                "criminal_record" : self.find_element(DetailLocators.CRIMINAL_RECORD),
                }
            for num, element in enumerate(self.driver.find_elements(*DetailLocators.RELATED), 1):
                key = f'related_{num}'
                person[key] = element.text
                
            for num, element in enumerate(self.driver.find_elements(*DetailLocators.PHONES), 1):
                key = f'phone_{num}'
                person[key] = element.text

            field_names.update(person.keys())
            if person["name"].lower().count("whitepages"):
                continue
            print(person)
            persons.append(person)
        return persons

    def browse_pages(self):
        detail_urls = self.extract_url_details()
        persons = self.extract_details(detail_urls) 
        self.to_csv(persons)

    
def main():
    scraper = Scraper(URL_SEARCH)
    scraper.browse_pages()
    #scraper.interceptor()

if __name__ == "__main__":
    main()
