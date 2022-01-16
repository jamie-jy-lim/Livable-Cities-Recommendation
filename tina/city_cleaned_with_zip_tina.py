#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import needed libraries
import pandas as pd
import numpy as np


# In[2]:


# read city csv into dataframe
df = pd.read_csv('final_city_state_geocode_thomas.csv')

# get city and state info into a list for matching zipcode later
city = [[df['city_name'][i], df['state_name'][i]] for i in range(len(df))]


# In[3]:


# get the zipcode dataframe
df_zip = pd.read_csv('uszips.csv')


# In[4]:


# filter out useful columns
df_zip = df_zip[['city','state_name','zip','state_id']]
# modify type zipcode column for further modification 
df_zip['zip'] = df_zip['zip'].astype(str)


# In[5]:


# create list holder for zipcode correction
# because some zipcode, e.g. 00601, are recorded as "601"
# this section is to correct the zipcode without 0 in the beginning
zip_correct = []

# loop over zipcode datagrame to get zipcode into the list
for n in range(len(df_zip)):
    z = df_zip['zip'][n]
    # to include 0's in the beginning of zipcode if those 0's are truncated
    if len(z) < 5:
        zip_correct.append('0'*(5-len(z))+z)
    else:
        zip_correct.append(z)
# get the correct zipcode back to the zipcode dataframe
df_zip['zip'] = zip_correct


# In[6]:


# create list holder for state abbreviation
state_abbr = []
# loop over zipcode dataframe to get state abbreviation into the list
for n in range(len(df_zip)):
    s = df_zip['state_id'][n]
    state_abbr.append(s)
# get unique state abbreviation name
myset = set(state_abbr)
state_abbr = list(myset)


# In[7]:


# create list holder for zipcode
zip = []
for j in range(len(city)):
    # retrieve corresponding zipcode for city and state in our previous city list
    ziplist = list(df_zip.loc[(df_zip['city'] == city[j][0]) & (df_zip['state_name'] == city[j][1])].zip)
    # if matched value is found, return one of the zipcode (because there could be multiple zipcodes for one city)
    if len(ziplist)!= 0:
        zipcode = ziplist[3]
    # if no matched value, record as NULL
    else:
        zipcode = pd.NA
    zip.append(zipcode)
    
    
# add zipcode column with corresponding zipcode to our primary dataframe
df['zipcode'] = zip


# In[8]:


# check city with null zipcode
df[df['zipcode'].isnull()]


# In[9]:


# create list holder for state abbreviation
states_abbr = []
for k in range(len(city)):
    # retrive corresponding abbreviation for state in our previous city list
    abbr_lst = list(df_zip.loc[df_zip['state_name'] == city[k][1]].state_id)
    # if matched value is found, return one of the abbreviation (because there are repeated abbr rows for one city)
    if len(abbr_lst)!= 0:
        abbr = abbr_lst[0]
    # if no matched value, record as NULL
    else:
        abbr = pd.NA
    states_abbr.append(abbr)
    
# add state abbreviation column with corresponding abbreviation to our primary dataframe
df['state_abbr'] = states_abbr


# In[10]:


# manually input zipcode for city with null value in zipcode column
null_zip = ['96813','55104','93102','33701','27102','83702']
fill = pd.DataFrame(index =df.index[df.isnull().any(axis=1)], data= null_zip, columns=['zipcode'])

# fill zipcode for those cities in the primary dataframe
df.fillna(fill,inplace = True)


# In[11]:


# output as csv
df.to_csv('city_cleaned_with_zip_tina.csv',index=False)

