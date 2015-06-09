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

# form_DataFrame = get_form(response)
# response = OurVolts_login(uname, pwd) 
# report_DataFrame = scrape_report()

base_url = "http://www.trackitforward.com"

def get_form(response):
    response_soup = BeautifulSoup(response.text)
    form = response_soup.select('form')[0]
    input_tags = form.select('input')
    names = [tag.get('name') for tag in input_tags]
    values = [tag.get('value') for tag in input_tags]
    checked = [(tag.get('checked') == 'checked') for tag in input_tags]
    typ = [tag.get('type') for tag in input_tags]
    form_vals = pd.DataFrame(zip(names, values, typ, checked),columns=['name','value','typ','checked'] )       
    return form_vals.set_index('name')

def OurVolts_login(uname, pwd):
    # log-in to OurVolts 
    LOGIN_URL =  base_url+"/user/login"
    login_response = requests.get(LOGIN_URL)
    form_vars = get_form(login_response)
    payload = form_vars['value'].to_dict()
    payload['name'] = uname
    payload['pass'] = pwd    
    sesh = requests.Session()
    sesh.post(LOGIN_URL,data=payload)
    return sesh

def scrape_report(from_date = "", to_date = "", all_fields = False):
    sesh = OurVolts_login("BarefootEfrem@gmail.com", "F3_JH!2P%%5hhh" )       
    
    # get report form  
    REPORT_URL = base_url+'/site/67286/manage/report'
    report_response = sesh.get(REPORT_URL)
    fvals = get_form(report_response)

    
    include_types = fvals['typ'].isin(['checkbox','hidden','text'])
    fvals.loc[include_types,'checked'] = True  # set all checkbox, hidden, and text input types to be sent
    
    payload = fvals[fvals.checked]['value'].to_dict()
    
    if from_date or  to_date or all_fields:
        update_dict = {'op' : 'Update Report',
                       'from_date': from_date, 
                       'to_date' : to_date}
        payload.update(update_dict)
        response = sesh.post(REPORT_URL,data=payload)
        new_fvals = get_form(response)
        payload['form_token'] = new_fvals['value']['form_token']
        payload['form_build_id'] = new_fvals['value']['form_build_id']
    
    
    payload['op'] = 'Export'
    response = sesh.post(REPORT_URL, data=payload)    
    report = pd.read_csv(StringIO(response.content))
    
    LOGOUT_URL = 'https://www.ourvolts.com/logout'
    logout_response = sesh.get(LOGOUT_URL)  # logout (Not sure if this is necessary)
    return report
    
    
# ********* Main Code ******************   
    
from_date = '' 
to_date = ''
#report = scrape_report(all_fields = True)
#report.to_csv('HUB_hours.csv')

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
        
df['Volunteer'] = df['Volunteer'].astype('category')
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