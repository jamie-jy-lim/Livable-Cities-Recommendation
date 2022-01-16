#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import pandas library
import pandas as pd


# In[2]:


# read parkscore csv into dataframe
df = pd.read_csv('ParkScore_2021.csv')

# get the columns needed
df=df[['City','ParkScore']]


# In[3]:


# get city name from parkscore dataframe and store into city list
city = [df['City'][i].split(',')[0] for i in range(len(df))]

# loop over the city list to modify city names
for j in range(len(city)):
    if '/' in city[j]:
        idx = city[j].index('/')
        city[j] = city[j][:idx]
    if city[j] == 'Boise':
        city[j] = 'Boise City'
# get state name from parkscore dataframe and store into state list
state = [df['City'][i].split(',')[1].strip() for i in range(len(df))]

# update the City column with modified city names
df['City'] = city

# add State column to the dataframe
df['State'] = state

# standardize column names
df = df.rename(columns={'City': 'city','State':'state_abbr','ParkScore':'park_score'})

# remove rows with null value in parkscore 
df.dropna(inplace = True)


# In[4]:


# read AQI csv as dataframe
df2 = pd.read_csv('aqi_scraped_tina.csv')


# In[5]:


pd.set_option('display.max_rows', 500)

# merge parkscore dataframe and AQI dataframe based on city and state abbreviation to get a new dataframe
df3 = df2.merge(df, left_on =['city_name','state_abbr'], right_on = ['city','state_abbr'],how='left')


# In[6]:


# remove repeated city column
del df3['city']


# In[7]:


# new dataframe output as csv
df3.to_csv('aqi+park_score_tina.csv',index=False)

