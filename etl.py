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


def clean_govt_sheet(path):
    df = pd.read_excel(path, sheet_name='GOVT', skiprows=7, skipfooter=5, header=None)
    df.iloc[0, 0] = 'The Month'
    df.drop(1, axis=1, inplace=True)
    parent_header = df.iloc[0].ffill().str.split(' / ').map(lambda x: x[0])
    child_header = df.iloc[1].fillna('').str.split(' / ').map(lambda x: x[0])
    df = df.iloc[2:]
    df.columns = parent_header + '_' + child_header
    df = df[~df['The Month_'].str.startswith('TOTAL') & ~df['The Month_'].str.startswith('Q')]
    df = df[~df['The Month_'].isna()]
    df['month'] = df['The Month_'].str.split(' / ').map(lambda x: month_dict[x[0].strip()])
    df['year'] = df['The Month_'].str[-4:]
    cols_to_keep = ['The Month_', 'month', 'year']
    cols_to_keep += [col for col in df.columns[1:-2] if not (col.split('_')[1] == '' or col.split('_')[1] == 'TOTAL')]
    df = df[cols_to_keep]
    df.fillna(0, inplace=True)
    df['month'] = df['month'].astype('str')
    df['date'] = pd.to_datetime(df['month'] + '-' + df['year']).dt.date
    df.drop('The Month_', axis=1, inplace=True)
    df_melted = df.melt(id_vars=['date', 'month', 'year'], var_name='instruments', value_name='volume')
    return df_melted
    

def clean_bond_sheet(path):
    df = pd.read_excel(path, sheet_name='BOND', skiprows=5, skipfooter=5, header=None)
    df.iloc[0, 0] = 'The Month'
    df.drop([1, 2], axis=1, inplace=True)
    parent_header = df.iloc[0].ffill().str.split(' / ').map(lambda x: x[0])
    child_header = df.iloc[1].fillna('').str.split(' / ').map(lambda x: x[0])
    df = df.iloc[2:]
    df.columns = parent_header + '_' + child_header
    df = df[~df['The Month_'].str.startswith('TOTAL') & ~df['The Month_'].str.startswith('Q')]
    df = df[~df['The Month_'].isna()]
    df['month'] = df['The Month_'].str.split(' / ').map(lambda x: month_dict[x[0].strip()])
    df['year'] = df['The Month_'].str[-4:]
    cols_to_keep = ['The Month_', 'month', 'year']
    cols_to_keep += [col for col in df.columns[1:-2] if not (col.split('_')[1] == '' or col.split('_')[1] == 'TOTAL')]
    df = df[cols_to_keep]
    df.fillna(0, inplace=True)
    df['month'] = df['month'].astype('str')
    df['date'] = pd.to_datetime(df['month'] + '-' + df['year']).dt.date
    df.drop('The Month_', axis=1, inplace=True)
    df_melted = df.melt(id_vars=['date', 'month', 'year'], var_name='instruments', value_name='volume')
    return df_melted


def clean_fed_prov_sheet(path):
    df = pd.read_excel(path, sheet_name='FED_PROV', skiprows=8, skipfooter=5, header=None)

    df.iloc[0, 0] = 'The Month'
    df.drop([1], axis=1, inplace=True)
    parent_header = df.iloc[0].ffill().str.split(' / ').map(lambda x: x[0])
    child_header = df.iloc[1].fillna('').str.split(' / ').map(lambda x: x[0])
    df = df.iloc[2:]
    df.columns = parent_header + '_' + child_header
    df = df[~df['The Month_'].str.startswith('TOTAL') & ~df['The Month_'].str.startswith('Q')]
    df = df[~df['The Month_'].isna()]
    df['month'] = df['The Month_'].str.split(' / ').map(lambda x: month_dict[x[0].strip()])
    df['year'] = df['The Month_'].str[-4:]
    cols_to_keep = ['The Month_', 'month', 'year']
    cols_to_keep += [col for col in df.columns[1:-2] if not (col.split('_')[1] == '' or col.split('_')[1] == 'TOTAL')]
    df = df[cols_to_keep]
    df.fillna(0, inplace=True)
    df['month'] = df['month'].astype('str')
    df['date'] = pd.to_datetime(df['month'] + '-' + df['year']).dt.date
    df.drop('The Month_', axis=1, inplace=True)
    df_melted = df.melt(id_vars=['date', 'month', 'year'], var_name='instruments', value_name='volume')
    return df_melted



def clean_strip_muni_sheet(path):
    df = pd.read_excel(path, sheet_name='STRIP_MUNI', skiprows=8, skipfooter=5, header=None)

    df.iloc[0, 0] = 'The Month'
    df.drop([1], axis=1, inplace=True)
    parent_header = df.iloc[0].ffill().str.split(' / ').map(lambda x: x[0])
    child_header = df.iloc[1].fillna('').str.split(' / ').map(lambda x: x[0])
    df = df.iloc[2:]
    df.columns = parent_header + '_' + child_header
    df = df[~df['The Month_'].str.startswith('TOTAL') & ~df['The Month_'].str.startswith('Q')]
    df = df[~df['The Month_'].isna()]
    df['month'] = df['The Month_'].str.split(' / ').map(lambda x: month_dict[x[0].strip()])
    df['year'] = df['The Month_'].str[-4:]
    cols_to_keep = ['The Month_', 'month', 'year']
    cols_to_keep += [col for col in df.columns[1:-2] if not (col.split('_')[1] == '' or col.split('_')[1] == 'TOTAL')]
    df = df[cols_to_keep]
    df.fillna(0, inplace=True)
    df['month'] = df['month'].astype('str')
    df['date'] = pd.to_datetime(df['month'] + '-' + df['year']).dt.date
    df.drop('The Month_', axis=1, inplace=True)
    df_melted = df.melt(id_vars=['date', 'month', 'year'], var_name='instruments', value_name='volume')
    return df_melted

path = 'raw_data/2024-Bond-and-Money-Market-Secondary-Trading-Statistics.xlsx'

print(clean_bond_sheet(path))
