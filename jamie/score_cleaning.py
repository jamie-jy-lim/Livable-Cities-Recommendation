"""
clean the score dataframe

separate and make new columns for city and state abbreviations
"""

import pandas as pd


# read score data
edu_score=pd.read_csv('edu_score.csv')
job_score=pd.read_csv('job_score.csv')
safety_score=pd.read_csv('safety_score.csv')



# clean edu score data 

# separate cities from states 
edu_score['cities']=edu_score['city'].str.split(', ', expand=True)[0]
edu_score['states']=edu_score['city'].str.split(', ', expand=True)[1]

# drop the uncleaned city column
edu_score=edu_score.drop(columns=['city'])


# separate main city and state abbreviation
edu_score['city']=edu_score['cities'].str.split('-', expand=True)[0]
edu_score['state_abbr']=edu_score['states'].str.split('-', expand=True)[0]


# drop the cities, states columns
edu_score=edu_score.drop(columns=['cities','states'])


# display 
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(edu_score)


# save as csv file 
edu_score.to_csv('edu_score_cleaned.csv', index=False)



# clean job score data 
# separate and make columns for city and state abbreviation 

job_score['state_abbr']=job_score['city'].str.split(', ', expand=True)[1]
job_score['city']=job_score['city'].str.split(', ', expand=True)[0]


# display
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(job_score)


# save as csv file 
job_score.to_csv('job_score_cleaned.csv', index=False)




# clean safety score data 
# separate and make columns for city and state abbreviation 

safety_score['state_abbr']=safety_score['city'].str.split(', ', expand=True)[1]
safety_score['city']=safety_score['city'].str.split(', ', expand=True)[0]


# display
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(safety_score)


# save as csv file 
safety_score.to_csv('safety_score_cleaned.csv', index=False)
