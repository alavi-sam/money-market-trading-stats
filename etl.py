import pandas as pd
import os
import re
import datetime

# List all files in raw_data directory
data_files = os.listdir("raw_data")

def find_year(file):
    """Extract year from filename"""
    span = re.search(r'\d{4}', file).span()
    return int(file[span[0]: span[1]])

# Map month names to numbers
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
    """Clean money market trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='MMKT', skiprows=5, header=None)
        df.iloc[0, 0] = 'The Month'
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df.columns = [col.split(' / ')[0].strip() for col in df.columns]
        df = df[~df['The Month'].isna()]
        df = df[~df['The Month'].str.startswith('Q') & ~df['The Month'].str.startswith('TOTAL')]
    else:
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
                        var_name='instruments', 
                        value_name='volume')
    return df_melted


def clean_govt_sheet(path):
    """Clean government bond trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='GOVT', skiprows=5, header=None)
    else:
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
    """Clean bond trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='BOND', skiprows=5, header=None)
    else:
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
    """Clean federal/provincial bond trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='FED_PROV', skiprows=5, header=None)

    else:
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
    """Clean STRIP and municipal bond trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='STRIP_MUNI', skiprows=5, header=None)
    else:
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


def clean_corp_sheet(path):
    """Clean corporate bond trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='CORP', skiprows=5, header=None)
    else:
        df = pd.read_excel(path, sheet_name='CORP', skiprows=8, skipfooter=5, header=None)
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
    df['Other Domestic Bonds_Issuer'] = df['Other Domestic Bonds_Issuer'].astype('float') 
    df.fillna(0, inplace=True)
    df['month'] = df['month'].astype('str')
    df['date'] = pd.to_datetime(df['month'] + '-' + df['year']).dt.date
    df.drop('The Month_', axis=1, inplace=True)
    df_melted = df.melt(id_vars=['date', 'month', 'year'], var_name='instruments', value_name='volume')
    return df_melted
    

def clean_mbs_abs_sheet(path):
    """Clean MBS/ABS trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='MBS_ABS', skiprows=5, header=None)
    else:
        df = pd.read_excel(path, sheet_name='MBS_ABS', skiprows=8, skipfooter=5, header=None)
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
    df['Asset-Backed Securities_Issuer'] = df['Asset-Backed Securities_Issuer'].astype('float')
    df.fillna(0, inplace=True)
    df['month'] = df['month'].astype('str')
    df['date'] = pd.to_datetime(df['month'] + '-' + df['year']).dt.date
    df.drop('The Month_', axis=1, inplace=True)
    df_melted = df.melt(id_vars=['date', 'month', 'year'], var_name='instruments', value_name='volume')
    return df_melted


def clean_bonds_repo_sheet(path):
    """Clean bond repo trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='BOND_REPO', skiprows=5, header=None)
    else:
        df = pd.read_excel(path, sheet_name='BOND_REPO', skiprows=5, skipfooter=5, header=None)
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


def clean_mmkt_repo_sheet(path):
    """Clean money market repo trading data sheet"""
    if find_year(path) < 2020:
        df = pd.read_excel(path, sheet_name='MMKT_REPO', skiprows=5, header=None)
        df.iloc[0, 0] = 'The Month'
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df.columns = [col.split(' / ')[0].strip() for col in df.columns]
        df = df[~df['The Month'].isna()]
        df = df[~df['The Month'].str.startswith('Q') & ~df['The Month'].str.startswith('TOTAL')]
    else:
        df = pd.read_excel(path, sheet_name='MMKT_REPO', skiprows=5, skipfooter=5)    
        df.columns = [col.split(' / ')[0].strip() for col in df.columns]
        df.drop([df.columns[1]], axis=1, inplace=True)
        df = df[~df['The Month'].isna()]
        df = df[~df['The Month'].str.startswith('Q') & ~df['The Month'].str.startswith('TOTAL')]
    df.fillna(0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['month'] = df['The Month'].str.split('/').map(lambda x: month_dict[x[0].strip()])
    df['month'] = df['month'].astype('str')
    df['year'] = df['The Month'].str[-4:]
    df['date'] = pd.to_datetime(df['month'] + '-' + df['year']).dt.date
    df.head()
    df.drop(columns=['The Month', 'TOTAL'], inplace=True)
    df_melted = df.melt(id_vars=['date', 'month', 'year'], 
                        var_name='instruments', 
                        value_name='volume')
    return df_melted

if __name__ == '__main__':
    # Process all Excel files and output to CSV
    data_files = os.listdir("raw_data")
    os.makedirs('processed_data', exist_ok=True)

    mmkt_sheets = [clean_mmkt_sheet(os.path.join('raw_data', path)) for path in data_files]  
    df_mmkt = pd.concat(mmkt_sheets).sort_values(by=['date', 'instruments'])
    df_mmkt.to_csv(os.path.join('processed_data', 'MMKT.csv'))

    bond_sheets = [clean_bond_sheet(os.path.join('raw_data', path)) for path in data_files]
    df_bond = pd.concat(bond_sheets).sort_values(by=['date', 'instruments'])
    df_bond.to_csv(os.path.join('processed_data', 'BOND.csv'))

    govt_sheets = [clean_govt_sheet(os.path.join('raw_data', path)) for path in data_files]
    df_govt = pd.concat(govt_sheets).sort_values(by=['date', 'instruments'])
    df_govt.to_csv(os.path.join('processed_data', 'GOVT.csv'))

    fed_prov_sheets = [clean_fed_prov_sheet(os.path.join('raw_data', path)) for path in data_files]
    df_fed_prov = pd.concat(fed_prov_sheets).sort_values(by=['date', 'instruments'])
    df_fed_prov.to_csv(os.path.join('processed_data', 'FED_PROV.csv'))

    strip_muni_sheets = [clean_strip_muni_sheet(os.path.join('raw_data', path)) for path in data_files]
    df_strip_muni = pd.concat(strip_muni_sheets).sort_values(by=['date', 'instruments'])
    df_strip_muni.to_csv(os.path.join('processed_data', 'STRIP_MUNI.csv'))

    corp_sheets = [clean_corp_sheet(os.path.join('raw_data', path)) for path in data_files]
    df_corp = pd.concat(corp_sheets).sort_values(by=['date', 'instruments'])
    df_corp.to_csv(os.path.join('processed_data', 'CORP.csv'))

    mbs_abs_sheets = [clean_mbs_abs_sheet(os.path.join('raw_data', path)) for path in data_files]
    df_mbs_abs = pd.concat(mbs_abs_sheets).sort_values(by=['date', 'instruments'])
    df_mbs_abs.to_csv(os.path.join('processed_data', 'MBS_ABS.csv'))

    bond_repo_sheets = [clean_bonds_repo_sheet(os.path.join('raw_data', path)) for path in data_files]
    df_bond_repo = pd.concat(bond_repo_sheets).sort_values(by=['date', 'instruments'])
    df_bond_repo.to_csv(os.path.join('processed_data', 'BOND_REPO.csv'))

    mmkt_repo_sheets =[clean_mmkt_repo_sheet(os.path.join('raw_data', path)) for path in data_files]
    df_mmkt_repo = pd.concat(mmkt_repo_sheets).sort_values(by=['date', 'instruments'])
    df_mmkt_repo.to_csv(os.path.join('processed_data', 'MMKT_REPO.csv'))

    # print(df_mmkt_repo)
