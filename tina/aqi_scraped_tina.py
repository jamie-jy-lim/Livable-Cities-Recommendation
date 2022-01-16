#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import needed libraries
import pandas as pd
import requests
import json


# In[2]:


# read into cleaned city csv into dataframe
df=pd.read_csv('city_cleaned_with_zip_tina.csv')


# In[3]:


# create list holder for AQI(air quality index) to be scraped
AQI = []

# loop over dataframe to get corresponding zipcode
for i in range(len(df['zipcode'])):
    zipcode = df['zipcode'][i]
    # use retrieved zipcode to connect to API 
    url = 'https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=%s&distance=25&API_KEY=99B69A18-6CF9-4276-AAF0-88E3FAEBB345' % zipcode
    # get air quality index of PM 2.5 of each city from the API site
    response = requests.get(url, headers = {'Content-Type':'application/json'})
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        # scrape AQI into the AQI list if there exists
        if len(data)>=2:
            AQI.append(data[1]['AQI'])
        # record as null if no AQI found
        else:
            AQI.append(pd.NA)
# data scraped on Oct 8, 9:37pm            


# In[4]:


# add AQI column to the primary dataframe
df['aqi_pm2.5'] = AQI

# output as csv
df.to_csv('aqi_scraped_tina.csv',index=False)

