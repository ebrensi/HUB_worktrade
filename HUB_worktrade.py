# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 21:55:21 2015

@author: Efrem
"""
# This script is gonna log into OurVolts and scrape volunteers' hours information

import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime as dt
from StringIO import StringIO
import os

    
    
# ********* Main Code ******************   
from_date = '' 
to_date = ''

dir_list = pd.Series(os.listdir(os.getcwd()))
dd = dir_list.str.extract('hours-(\d+)-(\d+)-(\d+)-(\d+)-(\d+)-(\d+)').dropna().sort([0,1,2,3,4,5],ascending=False)
file_name = dir_list[dd.index[0]]

print('Reading "%s"...') % file_name 
report = pd.read_csv(file_name)

#df = report[['Date','Volunteer','Hours','Activity','Notes']]
df = report[['Date','Volunteer','Hours']]
week_frq = 'W-Sun'


# fill in missing data of volunteer Names and Activities
df['Volunteer'] = df['Volunteer'].fillna('(unknown)')     
if 'Activity' in df.columns:    
    df['Activity'] = df['Activity'].fillna('(unspecified)')

# convert dates to pandas datetime objects
df['Date'] = pd.to_datetime(df['Date']) 
if 'Submitted Date' in df.columns: 
    df['Submitted Date'] = pd.to_datetime(df['Submitted Date']) 
  
df = df.sort(['Volunteer','Date'])  
        
#df['Volunteer'] = df['Volunteer'].astype('category')
#vol = pd.pivot_table(df,columns='Volunteer',index='Date',values='Hours', aggfunc=pd.np.sum)

"""
volunteers = df.Volunteer.unique()
if not from_date:
    from_date = df.index.min()
if not to_date:
    to_date = df.index.max()
        
weeks = pd.date_range(start_date, end_date, freq=week_frq)

vdata = pd.DataFrame(index=weeks, columns=volunteers)#.fillna(0)

#volunteers = ['Efrem Rensi']

for volunteer in volunteers:
#    print volunteer + " worked..."
    mask = (df['Volunteer'] == volunteer) & (df.Date > start_date) & (df.Date < end_date)
    hours = df[mask][['Date','Hours']].set_index('Date')
    weekly_hours = hours.resample(week_frq, how='sum')#.fillna(0) 
#    print weekly_hours    
    vdata[volunteer][weekly_hours.index] = weekly_hours
    
vdata.T.to_excel('weekly_recap.xls')
"""