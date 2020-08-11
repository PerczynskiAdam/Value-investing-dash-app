import pandas as pd
import glob
from functools import reduce


#### Create dataframe with gpw indicators for each stock
# Load all csv files from directory
data_files = glob.glob(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indicators\*.csv')

# Merge files on indexes
indis_df = reduce(lambda left, right: pd.merge(left, right, left_index = True, right_index = True, how = 'outer'), 
[pd.read_csv(df, index_col = [0, 1]) for df in data_files])

#drop_duplicates
indis_df.drop_duplicates(inplace = True)

#reset_indexes
indis_df.reset_index(inplace=True)

#rename column names
indis_df = indis_df.rename(columns = {indis_df.columns[0]: "Ticker", indis_df.columns[1]: "Data"})

#replace % to empty string
indis_df = indis_df.replace("%", "", regex = True)

#change date quarter to last day of each quarter
dictdate = {'/Q1': '-03', '/Q2': '-06', '/Q3': '-09', '/Q4': '-12'}
for k,v in dictdate.items():
   indis_df['Data'] = indis_df['Data'].str.replace(k, v)

indis_df['Data'] = pd.to_datetime(indis_df['Data'])

#set index to Data column
indis_df = indis_df.set_index("Data", drop = True)

#change date as last day of month to further usage
indis_df.index = indis_df.index.to_period("M").to_timestamp("M")

#change ROE and Marża zysku operacyjnego to numeric
indis_df[['ROE', 'Marża zysku operacyjnego']] = indis_df[['ROE', 'Marża zysku operacyjnego']].apply(pd.to_numeric)

#export dataframe to csv
indis_df.to_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indis_df.csv', encoding = 'utf_8_sig')

#filter by date
df_2019 = indis_df[indis_df.index == "2019-12-31"]

#choose stocks that C/Z < 5
df_2019[(df_2019['Cena / Zysk'] < 5) & (df_2019['ROE'] > 10)]

