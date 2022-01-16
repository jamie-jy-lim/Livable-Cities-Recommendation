"""

merge edu/job/safety data with city name data

"""

import pandas as pd 

# read score data
edu_score=pd.read_csv('edu_score_cleaned.csv')
job_score=pd.read_csv('job_score_cleaned.csv')
safety_score=pd.read_csv('safety_score_cleaned.csv')

# read city name data
city_df=pd.read_csv('city_cleaned_with_abbr.csv')


# merge edu_score to city name
merged_df=city_df.merge(edu_score, on=['city','state_abbr'], how='left')

# merge job_score 
merged_df=merged_df.merge(job_score, on=['city','state_abbr'], how='left')

# merge safety score
merged_df=merged_df.merge(safety_score, on=['city','state_abbr'], how='left')


# display final merged datafram
print(merged_df)


# save as csv file 
merged_df.to_csv('jamie.csv', index=False)
