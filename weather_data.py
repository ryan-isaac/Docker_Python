import numpy as np
import pandas as pd
from pandas import ExcelWriter
from datetime import date


#_______________________________#
# Exercise 1:
#_______________________________#


#_______________________________#
# Fetching Station Inventory data
#_______________________________#

url= "https://drive.google.com/file/d/1yotRMAUOAYCKv-fgCODxz20auMxbUzO3/view"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
station_inventory = pd.read_csv(path,
                  skiprows=2, 
                  header=0, 
                  sep=',')
station_inventory.drop(station_inventory[station_inventory['Name'] != 'TORONTO CITY'].index,inplace=True, axis=0)
toronto_id= station_inventory[station_inventory['Name'] =='TORONTO CITY']['Station ID']

#_______________________________#
# Fetching Weather data
#_______________________________#
# fetching data for each station name that contains Toronto City
# TORONTO station is was null for most values so I decided to get the median of all Toronto stations
# input date is date.today() => October 2021


def fetch_data(ids= toronto_id, input_date = date.today(), dataset = pd.DataFrame()):
    for ID in toronto_id:
        for year in range(input_date.year-3,input_date.year+1):
            dataset= pd.concat([dataset, \
            pd.read_csv(f"https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={ID}&Year={year}&Month={input_date.month}&Day={input_date.day}&timeframe=2&submit=Download+Data")], \
            join='outer', 
            ignore_index=True)
            
    # renaming columns
    dataset.drop_duplicates(inplace=True)
    dataset.columns = ['Name' if column_name == 'Station Name' else column_name for column_name in dataset.columns]
    dataset.columns = ['Longitude' if column_name == 'Longitude (x)' else column_name for column_name in dataset.columns]  
    dataset.columns = ['Latitude' if column_name == 'Latitude (y)' else column_name for column_name in dataset.columns]
        
    return dataset
#_______________________________#
# Merging tables
#_______________________________#
weather_data = fetch_data()

temp = station_inventory.copy()
temp.drop(['Longitude','Latitude','Name','Province','Latitude (Decimal Degrees)','Longitude (Decimal Degrees)'], axis=1, inplace=True)

temp1=weather_data.copy()
temp1.drop(['Longitude','Latitude','Name'], axis=1, inplace=True)

df= temp1
for i,column in enumerate(temp.columns.to_list()):
    df[column]= temp.values.tolist()[0][i]

    
#_______________________________#
# Processing data
#_______________________________#

# delete future and older than 3 years data
df.drop(df[(df['Year'] >= date.today().year) & (df['Month'] >= date.today().month) & (df['Day'] > date.today().day)].index, inplace= True, axis=0)
df.drop(df[(df['Year'] >= date.today().year) & (df['Month'] > date.today().month)].index, inplace= True, axis=0)
df.drop(df[(df['Year'] <= date.today().year-3) & (df['Month'] < date.today().month) & (df['Day'] < date.today().day)].index, inplace= True, axis=0)
df.drop(df[(df['Year'] <= date.today().year-3) & (df['Month'] < date.today().month)].index, inplace= True, axis=0)


# delete unused columns
df= df[['Climate ID', 'Year', 'Month', 'Day', 'Max Temp (°C)', 'Min Temp (°C)', 'Mean Temp (°C)']]


#_______________________________#
# Exporting data by year to one excel file
#_______________________________#

years = [x for x in set(df['Year'])]
df_name= {}

for year in years:
    df_name[f'df_{year}'] = df[df['Year'] == year]

with ExcelWriter('/usr/src/app/output/weather_data.xlsx',engine='xlsxwriter') as writer:
    try:
        for name, df_ in zip(df_name.keys(),df_name.values()):    
            df_.to_excel(writer, sheet_name=f'{name}')
        print('Success: Excel file saved as weather_data.xlsx')
    except:
        print('Error: Excel file not saved')



#_______________________________#
# Exercise 2:
#_______________________________#


# Max Temperature for year
print('Maximum Temperature for year: \n', df[['Year','Max Temp (°C)']].groupby('Year').max(),'\n')

# Minimum Temperature for year
print('Minimum Temperature for year: \n', df[['Year','Min Temp (°C)']].groupby('Year').min(),'\n')

# Average Temperature per month for year
print('Average Temperature per month for year: \n', df[['Year','Month','Mean Temp (°C)']].groupby(['Year','Month']).mean(), '\n')

# Average Temperature overall for year
print('Average Temperature overall for year: \n', df[['Year','Mean Temp (°C)']].groupby(['Year']).mean(),'\n')

# Number of days in year and previous year where temperature is a. Equal b. Within 1 degree
# Daily Mean tempreture is chosen
temps={}
equal= {}
within_1_degree={}

for year in sorted(df['Year'].value_counts().index):
    temps[f'temp_{year}']= df[df['Year'] == year]['Mean Temp (°C)']
    equal[year]=0
    within_1_degree[year]=0
    
    for temp in temps[f'temp_{year}']:
        try:
            if temp in temps[f'temp_{year-1}']:
                equal[year] +=1
            else:
                equal[year] += 0

            for tempr in np.arange(temp-1,temp+0.1,0.1):
                if tempr in temps[f'temp_{year-1}']:
                    within_1_degree[year] +=1
                    
            for tempr in np.arange(temp,temp+1.1,0.1):
                if tempr in temps[f'temp_{year-1}']:
                    within_1_degree[year] +=1
            else:
                within_1_degree[year] += 0
        except:
            continue
        
                
print('Number of days in year and previous year where temperature is equal: ',equal, '\n',
      'Number of days in year and previous year where temperature is within_1_degreei: \n',within_1_degree)

