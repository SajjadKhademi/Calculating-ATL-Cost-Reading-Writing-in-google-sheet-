import pandas as pd
import datetime
import calendar


def convert_to_date(df):
    if (isinstance (df,str)):
        #x = datetime.datetime.strptime(df,"%d/%m/%Y")
        return pd.to_datetime(df,errors='coerce',dayfirst=True,yearfirst=True, format="%d/%m/%Y")
    else:
        Month = int(df.strftime('%m'))
        Day = int(df.strftime('%d'))
        Year = int(df.strftime('%Y'))
        df = datetime.datetime(Year,Month,Day)
        return pd.to_datetime(df , errors='coerce' ,format="%Y-%m-%d")

#######################################################

def get_max_day_of_month(month):
    m = pd.to_datetime(month)
    year , month = m.year , m.month
    last_day = calendar.monthrange(year, month)[1] #last day of month
    return last_day

########################################################

def get_next_month(m):
    current_month = pd.to_datetime(m)
    if current_month.month < 12:
        next_month = datetime.datetime(current_month.year, current_month.month+1, 1)
    else:
        next_month = datetime.datetime(current_month.year+1, 1, 1)   
    next_month = next_month.strftime('%Y-%m-%d')
    return next_month



