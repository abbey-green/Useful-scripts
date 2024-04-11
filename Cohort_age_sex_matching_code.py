#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd 
import numpy as np
from tqdm import tqdm
import random 


# In[2]:


df_alzd = pd.read_csv('df_alzd_ogu_and_metadata_071723.csv')
df_alzd = df_alzd.set_index('Unnamed: 0.1')

df_no_imp = pd.read_csv('df_no_cog_imp_ogu_and_metadata_071723.csv')
df_no_imp = df_no_imp.set_index('Unnamed: 0.1')


# In[6]:


already_matched = []


# In[7]:


# Create age and sex matched cohorts

matched_pids = []
year_gap = 3
n = 0 

for pid in tqdm(list(df_alzd.index)):
    # print(pid)
    age = df_alzd.at[pid, 'age_at_collection']
    age_aprox_plus = age + year_gap
    age_aprox_minus = age - year_gap
    sex = df_alzd.at[pid, 'sex']
    # print(age)
    # print(sex)
        

    ## Match age and sex to age and sex of pids in other cohort 
    match_pids_list = []
    for pid_2 in list(df_no_imp.index):
            if (pid_2 not in matched_pids) and (pid_2 not in already_matched):
            
                age_match = df_no_imp.at[pid_2, 'age_at_collection']
                sex_match = df_no_imp.at[pid_2, 'sex']

                # Loop through all pids to find ones that match age + sex 
                if age_match == age and sex_match == sex:
                    # print(age_match) 
                    # print(sex_match)
                    # print(age)
                    match_pids_list.append(pid_2)
    
                    # print(match_pids_list)
                            
# If no one is the exact age and gender match, expand the age range and add the pid if it has data
    if len(match_pids_list) < 1:
        match_pids_list_backup = []
        for pid_2 in list(df_no_imp.index):
            
            if (pid_2 not in matched_pids) and (pid_2 not in already_matched):
                age_match = df_no_imp.at[pid_2, 'age_at_collection']
                sex_match = df_no_imp.at[pid_2, 'sex']

                if age <= age_match <= age_aprox_plus and sex_match == sex or age_aprox_minus <= age_match <= age and sex_match == sex:
                    # print(age_aprox_minus)
                    # print(pid_2)
                    match_pids_list_backup.append(pid_2)
            
        if len(match_pids_list_backup) >= 1:           
            np.random.seed(0)
            rand_pid = random.sample(match_pids_list_backup, 1)
            # print(rand_pid)
            matched_pids.extend(rand_pid)
            
            # Keep track of count
#             n = n +1                                   
#             print(n)
             
            
        # If there is more than one pid that age and sex matches, randomly choose one and add to main list 
    elif len(match_pids_list) >= 1:
        np.random.seed(0)
        rand_pid = random.sample(match_pids_list, 1)
        # print(rand_pid)
        matched_pids.extend(rand_pid)
#         n = n +1                                   
#         print(n)
         

    else:
        pass
            
                    
print(matched_pids)
print(len(matched_pids))


# In[ ]:





# In[ ]:




