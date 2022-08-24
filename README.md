# Housing_market_modeling
Scrape data and analyse it for ML predictions

## Project

The project initially consist of scraping house prices from sold properties in the last 10 years from the website "Domain real state". The data will have the address, state, prince, type of housing, and date sold.

## Motivation

As the Australian house market rises, the affoarbility of house becomes a hot topic between young people, which are trying to get into the market. My motivation for this project was develop some of my data and coding skills by gathering and analysing housing prices across Victoria and potentially other states. 

## Issue1

Initially, the project was meant to create thousands of URL based on a list of postocode (postcode.csv). However, it would take too long. Therefore, the data will scrape based on user input. The input will be: suburb name, suburb postcode, state. 

There will be automation for the price range. Restricting the price range helps to scrape more results since the website only makes 50 pages available for each search regardless of how many results it will have.

## Issue 2

The columns names are being written into the csv file everytime a page is scraped. In addition, the script is breaking before all pages are scraped.

This was solved by adding if conditions with os.path.exist. This checks whether the file exist before appending the data.

## Issue 3

Some page are coming with empty content. For instance, when it is scraping for carnegie, pages 8, 9, 14, 15 fail. For murrumbeena, pages 2,3,4,8,9 and etc. 

This was solved by removing the user input to construct the page string and adding WebDriver wait object to guarantee any AJAX elements are fully rendered.