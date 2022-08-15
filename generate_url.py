from scraper import Scraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class ResultsScraper(Scraper):
    # This class scrape the number of results available to
    # predict how many URL will be generated
    #TODO: LINK THE NUMBER OF RESULTS WITH PRICE RANGE
        #This will allow us to scrape as much old data as possible
    
    def __init__(self, url):
        #Inheritance from scraper.py to create similar scraper object
        super.__init__(url)

    def get_right_pages(self):
        #Use the Scraper
       search_summary = self.driver.find_element(By.CLASS_NAME, 'css-ekkwk0').text
       n_results = int(search_summary.split(' ', maxsplit=1)[0])

       if n_results%20 == 0:
            n_pages = n_results/20
       else:
            n_pages = (n_results//20)+1
       print(n_results, n_pages)
    #    return n_pages

    
def url_generator(number_pages, suburb_postcode=[]):
    url_list = []
    for x in suburb_postcode:
        for y in range(number_pages):
            x+= 1
            BASE_URL = f'https://www.domain.com.au/sold-listings/?postcode={x}&price=0-5000000&excludepricewithheld=1&page={y}'
            url_list.append(BASE_URL)
            print(BASE_URL)
    print (len(url_list))        

n_pages = ResultsScraper('https://www.domain.com.au/sold-listings/?postcode=3168&price=0-5000000&excludepricewithheld=1')
n_pages.get_right_pages()