# bogleapp
script for python3.4 to track a boglehead portfolio
Usage:
Create file settings.py with following data:
    
URL assets list from morningstar.es
quote_page = ['http://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id=XXXXXXXXX']

number of shares for each mutual fund
data_shares = ['1']

groups for portfolio rebalancing
group01 = ['Europe', 'N.America', 'Pacific', 'Pacific', 'Em.Markets', 'Em.Markets',
           'Spain', 'Bonds', 'Bonds', 'Bonds']

assing weights to groups. sum of weights = 100
dict01 = {'Europe': 16.8, 'N.America': 12.0, 'Pacific':7.20, 'Em.Markets':7.20,
          'Spain':4.80, 'Bonds':52.0}

Running this script, we will get an output.txt file with the following data:

A list with assets value:

                    name    share   price    curr       group     total
Pictet-Japan Index R EUR   10.000  100.00  1.0000     Pacific   1000.00

Current portfolio values is 1000 Euros



********
