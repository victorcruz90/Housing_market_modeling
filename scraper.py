from datetime import date, timedelta
import itertools
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re

#Scraper object that get the values from website and store into a dataframe.
class Scraper:
    
    def __init__(self, url):
        #Create the scraper object with some options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.headless = True
        self.driver = webdriver.Chrome(service = Service('/Users/victorcruzdefaria/Downloads/chromedriver'), options=self.options)
        self.driver.get(url)

    def get_details(self):

        #get the prices, address and date sold and add to a list
        prices = [x.text for x in self.driver.find_elements(By.CLASS_NAME, 'css-9hd67m')]
        full_address = [x.text for x in self.driver.find_elements(By.CLASS_NAME, 'css-bqbbuf')]
        date_sold = [x.text for x in self.driver.find_elements(By.CLASS_NAME, 'css-1nj9ymt')]
        housing_type = [x.text for x in self.driver.find_elements(By.CLASS_NAME, 'css-693528')]
        
        
        #get the size info i.e. # of beds, # of baths, #number of parking
        #CHALLENGE: sometimes the size of the house/unit comes after the above metrics, used regex in list comprehension to remove all the strings starting with 3 digits
        layout_info = [x.text for x in self.driver.find_elements(By.CLASS_NAME, 'css-1ie6g1l') if not re.search(r"[m]", x.text)]
        
        #Group the layout_info into groups of 3
        splitedSize = 3
        layout_info = [layout_info[x:x+splitedSize] for x in range(0, len(layout_info), splitedSize)]
        
        #Group the data together and store into a panda dataframe
        data = [[e for x in grp for e in (x if isinstance(x, list) else [x])] for grp in zip(full_address,housing_type, date_sold, layout_info, prices, )]
        df = pd.DataFrame(data, columns=['address','housing_type', 'sold_date', 'n_beds','n_bath','n_garage', 'prices'])

        #DATA WRANGLING: Cleaning the data for better modeling in the future (ML). We also convert the data to desired formats
        #separate suburb, state, postcode and address into different columns (NEEDS OPTIMISATION)
        df[['address', 'suburb']] = df['address'].str.split(',', expand=True)
        df[['empty','suburb', 'state', 'postcode']] = df['suburb'].str.split(' ', n=3, expand=True)
        df['suburb'] = df['suburb'].str.strip()
        df['state'] = df['state'].astype('category')
        df.drop(labels=['empty'],axis=1, inplace=True)

        #appartment type usually come as Appartment/unit/flat. this function removes /unit/flat
        df['housing_type'] = df['housing_type'].str.split('/').apply(lambda x: x[0].strip()).astype('category')

        #filter the sold_date results to just the date (eg. 10/aug/2022). Convert from object to datetime64
        df['sold_date'] = df['sold_date'].str.split().apply(lambda x : '/'.join(x[-3:]).lower())
        df['sold_date'] = pd.to_datetime(df['sold_date'], dayfirst=True, format="%d/%b/%Y")

        #number of bedroms usually come as 1\nBed. This function removes the \nBed. This applies for n_bath and n_garage
        for i in ['n_beds', 'n_bath', 'n_garage']:
            df[i] = df[i].str.split().apply(lambda x: x[0]).astype('int')

        #remove $ and , from prices
        df['prices'] = df['prices'].apply(lambda x: re.sub('[^0-9]+','', x)).astype('int')
        
        return df

        