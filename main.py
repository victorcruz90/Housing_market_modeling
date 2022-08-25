from email.mime import base
from scraper import Scraper
import pandas as pd
import time
import random
import os
from page_variable import base_url

def main():
    path = './data/housing_data.csv'

    for page in range(1,51):
        try:
            scraper = Scraper(base_url + f'{page}').get_details()

            if scraper.empty:
                raise Exception
            else:
                print(f'Page {page} : Success')
                if not os.path.exists(path):
                    scraper.to_csv(path, mode='a',index=False)
                else:
                    scraper.to_csv(path, mode='a',index=False, header=False)
        except Exception:
            print(f'Page {page} : Fail')
            

        time.sleep(random.randint(1,10))

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end-start)