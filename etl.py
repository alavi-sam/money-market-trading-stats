import pandas as pd
import os
import re
import datetime


data_files = os.listdir("raw_data")

def find_year(file):
    span = re.search(r'\d{4}', file).span()
    return int(file[span[0]: span[1]])


month_dict = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}


def clean_mmkt_sheet(path):
    df = pd.read_excel(path, sheet_name='MMKT', skiprows=4, skipfooter=5)
    df.columns = [col.split(' / ')[0].strip() for col in df.columns]
    df.drop([df.columns[0], df.columns[2]], axis=1, inplace=True)
    df = df[~df['The Month'].isna()]
    df = df[~df['The Month'].str.startswith('Q') & ~df['The Month'].str.startswith('TOTAL')]
    df.fillna(0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['month'] = df['The Month'].str.split('/').map(lambda x: month_dict[x[0].strip()])
    df['month'] = df['month'].astype('str')
    df['year'] = df['The Month'].str[-4:]
    df['date'] = pd.to_datetime(df['month'] + '-' + df['year']).dt.date
    df.drop(columns=['The Month', 'TOTAL'], inplace=True)
    df_melted = df.melt(id_vars=['date', 'month', 'year'], 
                        var_name='instrument', 
                        value_name='volume')
    return df_melted

    