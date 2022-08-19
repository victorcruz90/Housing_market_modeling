from scraper import Scraper
import csv
import time
import random

def main():   
    suburb_name = str(input("Suburb: ")).lower
    state = str(input("State (e.g VIC, NSW...): ")).capitalize
    suburb_post = str(input("Enter postcode (XXXX): "))
    price = str(input("Price range (as XXXX-XXXXXX): "))


    page = 1
    while True:
        try:
            PAGE_URL = f'https://www.domain.com.au/sold-listings/{suburb_name}-{state}-{suburb_post}/?price={price}&excludepricewithheld=1&page={page}'
            scraped_data = Scraper(PAGE_URL).get_details().to_csv('/data/housing_data.csv', mode='a',index=False, date_format='sold_date')
            if scraped_data.empty:
                raise Exception
            else:
                print(f'Page {page}: Done')
        except Exception:
            print("Page Empty")
            break
        timeout = random.randrange(1,15)
        print(timeout)
        time.sleep(timeout)
        page += 1
    
    
    
        
if __name__ == '__main__':
    main()