from scraper import Scraper
import pandas as pd
import time
import random
import os


def main():   
    suburb_name = str(input("Suburb: "))
    state = str(input("State (e.g vic, nsw...): "))
    suburb_post = str(input("Enter postcode (XXXX): "))
    price = str(input("Price range (as XXXX-XXXXXX): "))
    # page = str(input("Page number: "))
    # price_ranges = ['0-400000','400000-500000','500000-600000','600000-700000', '700000-800000', '800000-900000', '900000-1000000','1000000-2000000', '2000000-3000000' ]

    path = './data/raw/housing_data.csv'
    i = 1
    index = 0

    while True:
        try:

            PAGE_URL = f'https://www.domain.com.au/sold-listings/{suburb_name}-{state}-{suburb_post}/?price={price}&excludepricewithheld=1&page={i}'

            scraper = Scraper(PAGE_URL)
            time.sleep(10)
            scraped_data = scraper.get_details()
            

            if scraped_data.empty:
                raise Exception
            else:
                print(f'Page {i}: Success')
                if not os.path.exists(path):
                    scraped_data.to_csv('./data/housing_data.csv', mode='a',index=False)
                else:
                    scraped_data.to_csv('./data/housing_data.csv', mode='a',index=False, header=False)
        except Exception:
            print(f'Page {i} : Fail')
        
        i += 1
        index +=1
    
    
        
if __name__ == '__main__':
    main()