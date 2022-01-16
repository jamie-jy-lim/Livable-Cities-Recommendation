# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 15:45:06 2021

@author: Yvette Zhang
"""

# In this script, we try to scrape the 'cost of living index' for selected cities

# Libraries: pandas, requests, beautifulsoup
# Source   : https://www.numbeo.com/cost-of-living/

import pandas as pd
import requests
from bs4 import BeautifulSoup

# use the requests library for page download:
http = 'https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+States'
page = requests.get(http)
soup = BeautifulSoup(page.content, 'html.parser')
# use '.find' function to locate the attribute of interest 'id="t2"'
# the data has been stored in a <table> using <tr> for row and <td> for one cell
data = soup.find('table', id="t2")
print(type(data))

rows = data.find_all('tr')
# create an empty list, and append the data(city name, cost of living index) in each row to the list using a for loop
mylist = []
for i in rows:
# use '.find_all' function to return a list of references 
# store the references into a list named table_data
    table_data = i.find_all('td')
# extract the data string from the references and store into a list named 'data'
    data = [j.text for j in table_data]
    if data != []:
# 'cost of living index' saved in list 'col', name of cities' saved in list 'city'
        col = data[2]
        location = data[1].split(', ')
        city = location[0]
        mylist.append([city, col])
print(mylist)

# display the data into the table 'df'
df = pd.DataFrame(mylist, columns = ['city', 'cost_of_living_score'])

# merge df with a csv file that contains all selected cities 
# using left outer join, so that we can keep the cities in the csv that do not have cost of living index
clean = pd.read_csv('city_cleaned_with_abbr.csv')
merge = clean.merge(df, on = 'city', how = 'left')
merge = merge.drop(['state','state_abbr'], axis=1)
# export the merged table to a csv 
merge.to_csv('yvette.csv', index =False)
