#!/usr/bin/python3
# -*- coding: utf-8 -*-

from settings import * #import settings
import requests
from bs4 import BeautifulSoup
from time import localtime, strftime
import os
#import sys
import pandas as pd
#import numpy as np

# Create file settings.py with following data:
    
#URL assets list from morningstar.es

#quote_page = ['http://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id=XXXXXXXXX']

#number of shares for each mutual fund

#data_shares = ['1']

#groups for portfolio rebalancing

#group01 = ['Europe', 'N.America', 'Pacific', 'Pacific', 'Em.Markets', 'Em.Markets',
#           'Spain', 'Bonds', 'Bonds', 'Bonds']

#assing weights to groups

#dict01 = {'Europe': 16.8, 'N.America': 12.0, 'Pacific':7.20, 'Em.Markets':7.20,
#          'Spain':4.80, 'Bonds':52.0}


scriptdir =  os.path.dirname(os.path.abspath(__file__))  # set working dir
os.chdir(scriptdir)

#Defs needed**********************************************************

#BLOOMBERG EURUSD. Set the value for curr_usd var.

def usd_val():
    page = requests.get('http://www.bloomberg.com/apps/quote?ticker=EURUSD:CUR')
    soup = BeautifulSoup(page.text, 'html.parser')
    price_box = soup.find('div', attrs={'class':'price'})
    curr_usd = price_box.text
    return(curr_usd)



# CODE BEGINS HERE **********************************************************************
# for loop

#currency.1 = Eur
data_curr = ['1', '1', '1', '1', usd_val(), '1', '1', '1', '1', '1']

data_name = []
data_price = []


for pg in quote_page:
    page = requests.get(pg)
    soup = BeautifulSoup(page.text, 'html.parser')
    name_box = soup.find('h1')
    name = name_box.text.strip()
    price_box = soup.find('td', attrs={'class':'line text'})
    price = price_box.text[4:]
    data_name.append(name)
    data_price.append(price)

# Swap commas by dots
data_price2 = []
for i in data_price:
    data_price2.append(float(i.replace(',', '.')))


#name of columns for dataframe
colum01 = ['name', 'share', 'price', 'curr', 'group']

# create df
df = pd.DataFrame(columns=colum01)
#populate df
df['curr'] = pd.Series(data_curr)
df['group'] = pd.Series(group01)
df['name'] = pd.Series(data_name)
df['share'] = pd.Series(data_shares)
df['price'] = pd.Series(data_price2)

#set dtypes to numeric
df = df.convert_objects(convert_numeric=True)

# add new column with totals
df['total'] = df['share']*df['price']/df['curr']

df['total'] = round(df['total'], 2)
# new dataframe to calc rebalancing, grouped by 'group' and summed up

df_reb = df[['group', 'total']].groupby('group').sum()

df_reb = df_reb.reset_index()

# copy 'weights' to a new column to replace them by numeric weights

df_reb['weight'] = df_reb['group']

df_reb['weight'] = df_reb['weight'].replace(dict01)

# calc current weights
df_reb['act_wei'] = round(df_reb['total'] / df_reb['total'].sum()*100, 2)
#original weight / current weight.
df_reb['ratio'] = round(df_reb['weight'] / df_reb['act_wei'], 3)

#sum to rebalance
df_reb['reb'] = round(df_reb['total'].sum()*df_reb['weight']/100 - df_reb['total'],1)

df_reb['total'] = round(df_reb['total'], 2)

#we do the same as before but just for stocks, droping bonds

df_reb_stock = df_reb[df_reb['group'] != 'Bonds']

# calc weights modified to 100%
df_reb_stock['weight'] = df_reb_stock['weight'] / df_reb_stock['weight'].sum() * 100

#calc current weights
df_reb_stock['act_wei'] = round(df_reb_stock['total'] / df_reb_stock['total'].sum()*100, 2)

#calc ratios
df_reb_stock['ratio'] = round(df_reb_stock['weight'] / df_reb_stock['act_wei'], 3)

#sum to rebalance just for stocks
df_reb_stock['reb'] = round(df_reb_stock['total'].sum()*df_reb_stock['weight']/100 - df_reb_stock['total'], 1)




#  print to file 'output.txt'

def print_file(name):
    '''print_file('name_of_file.txt')
    create name_of_file.txt with calculated dataframes'''
    with open(name, 'w') as file01:
        file01.writelines("%s" % (strftime("%a, %d %b %Y %X +0000", localtime())))
        file01.writelines('\n')
        file01.writelines('\n')
        file01.writelines(df.to_string())
        file01.writelines('\n')
        file01.writelines('\n')
        file01.writelines('Current portfolio values is ' '%i' % df['total'].sum() + ' Euros')
        file01.writelines('\n')
        file01.writelines('\n')
        file01.writelines('*****************Complete rebalancing******************\n')
        file01.writelines('\n')
        file01.writelines('\n')
        file01.writelines(df_reb.to_string())
        file01.writelines('\n')
        file01.writelines('\n')
        file01.writelines('***************Stock market rebalancing****************\n')
        file01.writelines('\n')
        file01.writelines('\n')
        file01.writelines(df_reb_stock.to_string())
    return


###enviar email con mailgun



def send_email(nfile):
    '''send_email('attachment')'''
    MG_SANDBOX_DOMAIN_NAME = 'sandboxe3da12012a7c4b149236bb3e33f9c469.mailgun.org'
#    MG_KEY = 'XXXXXXXXXXXXXXX'
    ces = requests.post(
        "https://api.mailgun.net/v3/" + MG_SANDBOX_DOMAIN_NAME + "/messages",
        auth=("api", MG_KEY),
        files=[("attachment", open(nfile))],
        data={
            "from": "cesar.alvarez.moran@gmail.com",
            "to": "cesar.alvarez.moran@gmail.com",
            "subject": "Cartera a " + "%s" % (strftime("%a, %d %b %Y %X +0000", localtime())),
            "text": "Empty"
        })
    return("%s" % (strftime("%a, %d %b %Y %X +0000", localtime())) + ' ' + ces.text)


print_file('output.txt')

#send_email('output.txt')
