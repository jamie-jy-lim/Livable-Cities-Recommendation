"""
Safety score 

web scraped from https://wallethub.com/edu/safest-cities-in-america/41926

** This script may not run if your IP is blocked from the web site.
(Output csv file is also provided in the folder just in case)
"""

# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd 


httpString ='https://wallethub.com/edu/safest-cities-in-america/41926'
print(httpString)
page = requests.get(httpString)

# Scraping
# Parse the page
soup = BeautifulSoup(page.content, 'html.parser')
# Find the required tag
table = soup.find(class_="cardhub-edu-table-div sortable-main-1")

x=table.find('tbody')
y=x.find_all('tr')


score_data=[]

# find and append city & score data 
for i in y:
    rank=i.find_next('td')
    city=rank.find_next('td')
    safety_score=city.find_next('td')
    score_data.append([city.text, safety_score.text])
    
    
# convert list into a dataframe 
safety_score=pd.DataFrame(score_data, columns=['city','safety_score'])


# display entire dataframe 
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(safety_score)

# save as csv file
safety_score.to_csv('safety_score.csv', index=False)
