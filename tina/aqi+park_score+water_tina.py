#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import pandas library
import pandas as pd


# In[2]:


# read sdg index csv into dataframe
df = pd.read_csv('2019USCitiesIndexResults.csv')

# get needed city, msa, and water violation percent columns
df = df[['maincity','msa','sdg6v1_waterviolation']]

# rename the columns
df = df.rename(columns={'maincity': 'city','sdg6v1_waterviolation':'water_violation_percent'})


# In[3]:


pd.set_option('display.max_rows', 500)

# store cities in a list
city = df['city']
# loop over the list to modify certain city names
for j in range(len(city)):
    if '/' in city[j]:
        idx = city[j].index('/')
        city[j] = city[j][:idx]
    if city[j] == 'Boise':
        city[j] = 'Boise City' 
    elif city[j] == 'Urban Honolulu':
        city[j] == 'Honolulu'

# extract the state abbreviation from msa and save into a list 
state_abbr = [df['msa'][i].split(',')[1].strip()[:2] for i in range(len(df))] 


# In[4]:


# use city and state abbreviation lists as two new columns for dataframe
df['city'] = city
df['state_abbr'] = state_abbr


# In[5]:


# read csv of previously merged data into a new dataframe 
df2 = pd.read_csv('aqi+park_score_tina.csv')
# rename city and state column for merge use later
df2.rename(columns = {'city_name':'city','state_name':'state'},inplace = True)


# In[6]:


# merge two dataframes to get the final one, keep the null by using left join
df3 = df2.merge(df, on =['city','state_abbr'],how='left')
# drop unneeded msa column
df3.drop(columns=['msa'],inplace = True)


# In[7]:


# output as csv
df3.to_csv('tina.csv',index=False)

