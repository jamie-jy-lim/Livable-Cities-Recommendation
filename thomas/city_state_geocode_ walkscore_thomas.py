#!/usr/bin/env python
# coding: utf-8

# ## Part 1 - Cleaning the excel file from Census Bureau to get the Top US City ranked by population 

# In[1]:


import pandas as pd

'''
written by Thomas
date: Oct 2, 2021

This is to get from file: #1 City ranked by population - SUB-IP-EST2019-ANNRNK.xlsx
to return a pd.DataFrame object

the .xlsx file is a data set from Census Bureau with atrributes: Rank, Geog. Area, City, State, and Populaitons
in each year 2010 - 2019

the DataFrame output cleaned the followings:
1. NaN
2. reference statements not relevant
3. columns data not relevant ('Census' and 'Estimates Base' from original excel is removed)
4. Added columns to get relevant city and state names from 'Geog. Area' column

Enjoy!
'''
# reading csv file from census
citypop = pd.read_excel('#1 City ranked by population - SUB-IP-EST2019-ANNRNK.xlsx', header = 2)

# extracting the columns
columns = pd.Series(citypop.columns)
columns2 = citypop.iloc[0]

for i in range(2, len(columns)):
    #print(i)
    columns[i] = columns2[i]

# changeing the colums names
citypop.set_axis(columns, axis='columns', inplace=True)

# drop irrelevant rows
citypop.drop([789,790,791,792,793],inplace=True)


# In[2]:


citypop


# In[3]:


# drop rows with all NaN
clean_citypop = citypop.dropna(how='all')

clean_citypop


# In[4]:


# drop irrelevant first row 
clean_citypop.drop([0], inplace=True)


# In[5]:


# drop irrelevant columns
final_citypop = clean_citypop.drop(columns=['Census','Estimates Base'])

final_citypop


# In[6]:


# make a copy to avoid alias issues
final_citypop2 = final_citypop.copy()


# In[7]:


# create a list of city names and state names 
lst = []
for i in final_citypop2['Geographic Area']:
    lst.append(i.split(','))
lst


# In[8]:


for i in lst:
    #print(i[1])
    # removing white spaces 
    i[0] = i[0].strip()
    i[1] = i[1].strip()
lst


# In[10]:


# as you can see, the suffix 'city' in the city name is uncommon and 
# is not needed in our data analysis, here the suffix 
# such as 'city', and a couple other suffix are removed

# below codes tries to find the interesting suffix other than 'city'
# finding non city names, add to a set called specialset
speciallst = []
for i in lst:
    if 'city' not in i[0]:
        speciallst.append(i[0])
print(speciallst)

# using regex below to search for suffix
import re

specialset = set()
for i in speciallst:
    #print(re.search(r'[a-z()]+$', i))
    
    if re.search(r'[a-z()]+$', i) != None:
        found = re.search(r'[a-z()]+$', i)
        specialset.add(i[found.start():found.end()])
print(specialset)


# In[11]:


# the above shows many suffix unwanted in our data analysis
# adding other suffix names we need to drop to set, removing overlapping names from set
specialset.add('CDP')
specialset.add('city')
specialset.add('Urban')
specialset.add('metro government (balance)')
specialset.add('consolidated government (balance)')
specialset.add('metropolitan government (balance)')
specialset.add('unified government (balance)')
specialset.add('government')
specialset.add('consolidated')
specialset.add('metropolitan')
specialset.add('urban')
specialset.add('urban')
specialset.add('unified')
specialset.add('metro')
specialset.remove('ounty')
specialset.remove('ity')

specialset
speciallist = list(specialset)
speciallist


# In[12]:


citystate = pd.DataFrame(lst)
citystate


# In[13]:


# creating a new column for city names
citystate['place_name'] = citystate.loc[:,0]
citystate


# In[14]:


citystate['place_definition'] = citystate['place_name'].copy()
citystate


# In[16]:


# cleaning the data based on the special set of suffix
for i in range(3):
    for i in list(specialset):
        print(i)
        bool = citystate['place_name'].str.contains(i)
        print(bool)
        print(True in bool)
        citystate['place_definition'][bool] = i
        # using map function and lambda to remove unwannted suffix
        citystate['place_name'][bool] = citystate['place_name'][bool].map(lambda x: x.removesuffix(i).rstrip()) 


# In[17]:


# renaming the columns
citystate.rename(columns={0: "geographic_area", 1: "state"}, inplace=True)


# In[18]:


citystate


# In[19]:


citystate['place_name2'] = citystate['place_name'].copy()


# In[20]:


# More cleaning...

# Now cleaning states with special characters '-' and '/'
# the name before the special characters '-' and '/' refers  to city name
# after those characters refers to county name, we are dropping them here, 
# keeping only the city name

# we create a dictionary to do that

dict= {}

for i in list(citystate['place_name2']):
    if '-' in i:
        dict[i] = i.split('-')[0]
    elif '/' in i:
        dict[i] = i.split('/')[0]
dict


# In[21]:


# replace the names 
citystate['place_name2'].replace(dict, inplace=True)


# In[22]:


# droping irrelevant columns 
citystate.drop(columns=['place_name', 'geographic_area','place_definition'], inplace=True)


# In[23]:


# rename the columns
citystate.rename(columns={'place_name2':'place_name'}, inplace=True)


# In[24]:


# create a state abbr columns from state names
citystate['state_abbr'] = citystate['state'].copy()


# In[25]:


# read a excel table with state and state abbreviations information from the epa.gov website
state_abbr = pd.read_excel('State and County Codes.xls').dropna()
state_abbr


# In[26]:


# renaming the column names
state_abbr.rename(columns=state_abbr.loc[1], inplace=True)


# In[27]:


# droping irrelevant columns 
state_abbr.drop(['State Code','County Name','County Code'], axis = 1, inplace=True)


# In[28]:


# reset index valeus
state_abbr.reset_index(drop=True, inplace = True)


# In[29]:


# making the string of state names uppper case using apply method
state_abbr['State Name'] = state_abbr['State Name'].apply(str.upper)


# In[30]:


state_abbr


# In[31]:


# making citystate's state abbr names upper case for matching with state_abbr's state names
citystate['state_abbr'] = citystate['state_abbr'].apply(str.upper)


# In[32]:


# replacing them with the state abbreviations
citystate['state_abbr'].replace(list(state_abbr['State Name']), list(state_abbr['State Abbr']), inplace=True)


# In[33]:


#  choosing only 3 columns column names
citystate = citystate[['state','state_abbr','place_name']]


# In[34]:


citystate


# In[35]:


citystate.rename(columns={'state':'state_name'}, inplace=True)


# In[37]:


## finally output the clean DataFrame to csv , index=False to make sure the output is format is correct
citystate.to_csv('final_citystate.csv', index=False)


# # Getting Coordinates

# In[38]:


# getting coordinates
import requests
import json


# In[39]:


# reading from the previous cleaned csv file
clean = pd.read_csv('final_citystate.csv').head(100)


# In[40]:


clean


# In[57]:


# 
# cityset = set(clean.iloc[0:100]['place_name'])


# In[41]:


# for looping purpose, create a list of city names and a list of state abbr from the DataFrame
placeslist = list(clean['place_name'])
stateslist = list(clean['state_abbr'])


# In[42]:


# get walk score, transit score, and bike score
import requests
import json
import pandas

# define a function walkscore with 3 parameters as inputs
# do the api requests and read json file
# return a set of 3 scores: walk score, transit score

def walkscore(lat, lon, address):
    url = "https://api.walkscore.com/score?format=json&address=" + address +  "&lat=" + str(lat) + "&lon=" + str(lon) + "&transit=1&bike=1&wsapikey=5078a7bec1506ab08bebed7139c28529"
    print(url) # print the url to confirm it is correct
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    
    
    data = json.loads(response.content.decode('utf-8'))
    # print(data['items'][0])
    # print('')
    print(data)
    if int(data['status']) != 1:
        walk_score = int()
        bike_score = int()
        transit_score = int()
    else:
        # using try except to avoid key error 
        # in case the values are not in the json file
        try:
            walk_score = data['walkscore']
        except KeyError:
            walk_score = int()
        try:
            transit_score = data['transit']['score']
        except KeyError:
            transit_score = int()
        try:
            bike_score = data['bike']['score']
        except KeyError:
            bike_score = int()
      
    return (walk_score, transit_score, bike_score)


# print(walkscore(lat, lon, address))


# In[43]:


# getting coordinates from MapQuest Geocoding API

# create a dictionary 

geocode_dict = {}
for i in range(len(placeslist)):
    geourl = 'http://open.mapquestapi.com/geocoding/v1/address?key=ZqMvpEnRKmMVJ0ZvDIPukXUd2o7b4xXu&location='+placeslist[i]+ ',' + stateslist[i]+',USA'
    print(geourl)
    
    response = requests.get(geourl, headers={'Content-Type': 'application/json'})
    print(response.status_code) 
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
#         print(data)
        geocode_dict[placeslist[i]] = data['results'][0]['locations'][0]['latLng']
#         []'matchCodes']['bbox']['point']


# In[44]:


geocode_dict 


# In[45]:


# create dataframe from dictionary 
geocode_df = pd.DataFrame.from_dict(geocode_dict, orient='index')


# In[46]:


geocode_df.reset_index(inplace=True)


# In[47]:


geocode_df.rename(columns={'index':'city_name'}, inplace=True)


# In[48]:


geocode_df['state_name'] = clean['state_name'].copy()
geocode_df['state_abbr'] = clean['state_abbr'].copy()


# In[49]:


geocode_df = geocode_df[['city_name', 'state_name', 'state_abbr', 'lat', 'lng']]


# In[50]:


# write the DataFrame to a csv file
geocode_df.to_csv('final_city_state_geocode.csv', index=False)


# In[51]:


geocode_df


# ## Getting Walkscore

# In[52]:


# create a walkscore dictionary
# get the coordinates and city names from the geocode_df for the walkscore function

walkscore_dict = {}
for index,row in geocode_df.iterrows():
    print(row[3], row[4],row[0])
    walkscore_dict[row[0]] = walkscore(row[3], row[4],row[0])


# In[53]:


walkscore_dict


# In[54]:


walkscore_df2 = pd.DataFrame.from_dict(walkscore_dict, orient='index')


# In[55]:


walkscore_df2.reset_index(inplace=True)
walkscore_df2.columns = ['city_name','walk_score','transit_score','bike_score']


# In[56]:


walkscore_df2


# In[57]:


walkscore_df2['state_name'] = clean['state_name'].copy()
walkscore_df2['state_abbr']  = clean['state_abbr'].copy()


# In[58]:


walkscore_df2 = walkscore_df2[['city_name', 'state_name','state_abbr','walk_score','bike_score']]


# In[59]:


walkscore_df2


# In[60]:


# replace 0 with np.nan for easy removing later
import numpy as np
walkscore_df2.replace(0, np.nan, inplace=True)


# In[61]:


walkscore_df2


# In[62]:


walkscore_df2.shape


# In[63]:


walkscore_df2.dropna().shape


# In[64]:


# write walkscore_df2 to a csv file, setting index = False 
walkscore_df2.to_csv('final_walkscore_thomas.csv', index=False)

