import gspread
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import requests
import pandas as pd
import datetime
import calendar
from Functions import *

#google api configuration
scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("D:\\Python Scripts\\ATL Data\\project files\\secret_key.json",scopes = scopes)

gc = pygsheets.authorize(service_file='D:\\Python Scripts\\ATL Data\\project files\\secret_key.json')
file = gspread.authorize(creds)

#select google sheet spread sheet
workbook = file.open_by_url('https://docs.google.com/spreadsheets/d/13_iuVX0sKYp-PuQjbz9QiWbCedplZ1IL2tHQsHpJnxw/edit?gid=1811641792#gid=1811641792')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/13_iuVX0sKYp-PuQjbz9QiWbCedplZ1IL2tHQsHpJnxw/edit?gid=1811641792#gid=1811641792')

#select sheet
sheet = workbook.worksheet("Marketing dep. data")
df = pd.DataFrame(sheet.get_all_records())


#convert to date
#----------------------------------------------------------------
df['New Start date'] = df['Date Start'].apply(lambda x: convert_to_date(x))
df['New End date'] = df['Date End'].apply(lambda x: convert_to_date(x))
df['Duration'] = (df['New End date'] - df['New Start date']).dt.days + 1
df['period_time'] = (df['New End date'] - df['New Start date']).dt.days + 1
Min_Date = df['New Start date'].min()
Max_Date = df['New End date'].max()
pd.set_option('display.max_columns', None)
# print(df)


#getting the whole period
months_full = pd.date_range(Min_Date,Max_Date, 
              freq='MS').strftime("%Y-%m-%d").tolist()

for i in months_full:
    df[i]=i


df[months_full] = df[months_full].apply(pd.to_datetime)
df = df[df['Type'] == 'Bilboard']

#------------------------------------------------------------

for m in months_full:
    current_month = pd.to_datetime(m)
    year , month = current_month.year , current_month.month
    a = calendar.monthrange(year, month)[1] #last day of month
    last_day_of_current_month = datetime.datetime(current_month.year, current_month.month,a)
    
    key= 0
    next_month = get_next_month(current_month)
    current_month = current_month.strftime('%Y-%m-%d')  
    if current_month == months_full[-1]:
        key = 1
        next_month = current_month

    for i in df.index: 
        if(isinstance(df.loc[i,current_month], datetime.datetime)):
            if (((df.loc[i,'New Start date'] > df.loc[i,current_month]) | (df.loc[i,'New Start date'] == df.loc[i,current_month] )) & ( (key == 1) | (df.loc[i,'New Start date'] < df.loc[i,next_month]) )): #revising or >=
                x = (last_day_of_current_month - df.loc[i,'New Start date']).days + 1 
                if(df.loc[i,'Duration'] > x ):
                    df.loc[i,current_month] = x 
                    df.loc[i,"Duration"] = df.loc[i,"Duration"] - x
                    this_month = current_month #to itterate on current month
                    while df.loc[i,'Duration'] > 0:
                        this_month = get_next_month(this_month)
                        count_days_of_month = get_max_day_of_month(this_month)
                        if (df.loc[i,'Duration'] > count_days_of_month):
                            df.loc[i,'Duration'] = df.loc[i,'Duration'] - count_days_of_month
                            df.loc[i,this_month] = count_days_of_month       
                        else:
                            df.loc[i,this_month] = df.loc[i,'Duration']
                            df.loc[i,'Duration'] = 0         
                else:
                    df.loc[i,current_month] = df.loc[i,'Duration'] # days mikhahim
                    df.loc[i,'Duration'] = 0
            else :
                df.loc[i,current_month] = 0
        else:
            continue

pd.set_option('display.max_columns', None)
#print(df)


#calculating shares
df['Duration'] = (df['New End date'] - df['New Start date']).dt.days + 1
df= df[df['Cost(IRR)'] != '']
df['Cost(IRR)']=df['Cost(IRR)'].apply(lambda x: float(x))


for i in months_full:
    df[i] = (df[i]/df['Duration'])*(df['Cost(IRR)'])



#unpivot dataframe
id_var = ['Status','City','Service']
df1 =pd.melt(df,id_vars=id_var, value_vars = months_full, var_name= 'Month', value_name = 'cost')
df1 = df1.dropna()


df1= df1[df1['cost'] != 0]
df1 = df1.groupby(['Status','City', 'Service', 'Month']).sum().reset_index()
df1 = df1.reset_index(drop = True)


#select the first sheet 
wks = sh[0]

#update the first sheet with df, startting at cell A1. 
wks.clear()
wks.set_dataframe(df1, 'A1')

print("ss")
print("sure")

print("seems to be coorect")
