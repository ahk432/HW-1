#AIDAN KIM 
import pandas as pd 
import numpy as np

#QUESTION 2 

#https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data
bea = pd.read_csv(r'Table.csv', sep = 'delimiter')
print(bea)

#https://www.tutorialspoint.com/how-to-delete-only-one-row-in-csv-with-python
#Dropped values at the top of the csv file (CAEMP25N and County)
bea = bea.drop(bea.index[0])
bea = bea.drop(bea.index[0])
bea = bea.reset_index(drop = True)

#Dropped values at the top of the csv file (CAEMP25N and County)
bea['new_column'] = bea['CAEMP25N Total full-time and part-time employment by NAICS industry 1']
bea = bea.drop(columns = 'CAEMP25N Total full-time and part-time employment by NAICS industry 1')

#Column names were in a row. Created New Column header with those values
#(GeoFips, GeoName, LineCode, Description, 2005, 2006, 2007). Dropped row with column names and reset index
bea.columns = bea.iloc[0]
bea = bea.drop(bea.index[0])
bea = bea.reset_index(drop = True)

#Take away extra commas 
#https://stackoverflow.com/questions/67905780/removing-comma-from-values-in-column-csv-file-using-python-pandas
bea['GeoFips,GeoName,LineCode,Description,2005,2006,2007'] = bea['GeoFips,GeoName,LineCode,Description,2005,2006,2007'].replace(',,', ',', regex = True)
bea['GeoFips,GeoName,LineCode,Description,2005,2006,2007'] = bea['GeoFips,GeoName,LineCode,Description,2005,2006,2007'].replace(',,', '', regex = True)

#Take away extra spaces
bea['GeoFips,GeoName,LineCode,Description,2005,2006,2007'] = bea['GeoFips,GeoName,LineCode,Description,2005,2006,2007'].replace('   ', '', regex = True)

#Separate all values within commas and put them in their own columns 
#https://stackoverflow.com/questions/55539765/how-to-extract-each-value-in-a-column-of-comma-separated-strings-into-individual
bea = bea['GeoFips,GeoName,LineCode,Description,2005,2006,2007'].str.split(',', expand = True)

#Reassign column names
bea_columns = {0:'GeoFips',
               1:'GeoName1',
               2:'GeoName2',
               3:'LineCode',
               4:'Description',
               5:2005,
               6:2006,
               7:2007}
bea.rename(columns = bea_columns, inplace = True)

#Merge columns 1 and 2
bea['GeoName'] = bea['GeoName1'] + bea['GeoName2']
bea = bea.drop(columns = 'GeoName1')
bea = bea.drop(columns = 'GeoName2')
bea = bea.drop(bea.index[12472:12485])
bea['GeoName'] = bea['GeoName'].replace('"', '', regex = True)
print(bea)

bea = bea.drop(columns = ['GeoFips', 'LineCode', 8])

#Sorting by year
#https://pandas.pydata.org/docs/reference/api/pandas.melt.html
print(bea)
bea = pd.melt(bea, id_vars = ['GeoName', 'Description'], value_vars = [2005, 2006, 2007], var_name = 'Year', value_name = 'Number of Jobs')

#Make manufacturing, military, and total their own columns. Make year its own column
#https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
bea['Total Employment'] = np.where(bea['Description'] == 'Total employment (number of jobs)', bea['Number of Jobs'], np.nan)
bea['Manufacturing'] = np.where(bea['Description'] == '"Manufacturing"', bea['Number of Jobs'], np.nan)
bea['Military'] = np.where(bea['Description'] == '"Military"', bea['Number of Jobs'], np.nan)

#Grouping by Year and Geoname and creating a column with these values 
grouped = bea.groupby(['GeoName','Year'])
bea['Group'] = grouped.ngroup()
print(bea)

#Drop Description and Number of Jobs Columns
bea = bea.drop(['Description', 'Number of Jobs'], axis = 1)

#Filling NaN with values from rows after
#https://pandas.pydata.org/docs/reference/api/pandas.Series.bfill.html#pandas.Series.bfill
bea = bea.bfill()
print(bea)

#Dropping duplicate rows and then dropping group column
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html#pandas.DataFrame.drop_duplicates
bea = bea.drop_duplicates(subset = ['Group'], keep = 'first')
bea = bea.drop(['Group'], axis = 1).reset_index(drop = True)


#--------------------------------------------------------------------
#QUESTION 3
bls = pd.read_excel('ssamatab1.xlsx')
#Rename Columns
bls_col_names = {'Table 1. Civilian labor force and unemployment by metropolitan area, seasonally adjusted':'LAUS Code',
                 'Unnamed: 1':'ST FIPS Code',
                 'Unnamed: 2':'Area FIPS Code',
                 'Unnamed: 3':'Area',
                 'Unnamed: 4':'Year',
                 'Unnamed: 5':'Month',
                 'Unnamed: 6':'Civilian Labor Force',
                 'Unnamed: 7':'Employment',
                 'Unnamed: 8':'Unemployment',
                 'Unnamed: 9':'Unemployment Rate'}
bls.rename(columns = bls_col_names, inplace = True)

#Remove first three rows and last 4 rows as they are NaN/non-important values 
bls = bls.drop(bls.index[159987:159992])
bls = bls.drop(bls.index[0:3])
bls = bls.reset_index(drop = True)

#Remove Columns so that only area, year, month, and unemployment rate is left. Stored Area FIPS column for later use in area_fips
#https://www.geeksforgeeks.org/how-to-drop-one-or-multiple-columns-in-pandas-dataframe/#
area_fips = bls.copy()
bls = bls.drop(['LAUS Code', 'ST FIPS Code', 'Area FIPS Code', 'Civilian Labor Force', 'Employment', 'Unemployment'], index = None, axis = 1)

#Drop most recent entries from August 2023
#https://saturncloud.io/blog/pandas-delete-rows-based-on-multiple-columns-values/#:~:text=In%20Pandas%2C%20you%20can%20achieve,the%20rows%20to%20be%20dropped.
bls = bls.drop(bls[(bls['Year'] == '2023') & (bls['Month'] == '08')].index)
print(bls)

#-------------------------------------------------------------------
#QUESTION 4
#https://stackoverflow.com/questions/5552555/unicodedecodeerror-invalid-continuation-byte
geocorr = pd.read_csv(r'geocorr2018_2327805808.csv', sep = ',', encoding = 'latin-1')
print(geocorr)

#Dropping first row since this is just the column names 
geocorr = geocorr.drop(geocorr.index[0])

#Dropping values with 99999
#https://saturncloud.io/blog/how-to-remove-rows-with-specific-values-in-pandas-dataframe/
geocorr = geocorr.drop(geocorr[geocorr['cbsa10']=='99999'].index)
print(geocorr)

#Dropping all columns except for county name and cbsa10
geocorr = geocorr.drop(columns = ['county','cbsaname10','pop10','afact'])
print(geocorr)

#Rename Columns
geocorr = geocorr.rename(columns = {'cbsa10': 'Area FIPS Code', 'cntyname':'County'})

#--------------------------------------------------------------------------------------

#QUESTION 5


##BLS Data

#Changing Unemployment rate column from object to float 
bls['Unemployment Rate'] = pd.to_numeric(bls['Unemployment Rate'], errors='coerce')


#Sorting by Area and Year 
bls = bls.sort_values(by = ['Area', 'Year'])
bls = bls.reset_index(drop = True)

#Creating a groupedby object to store average unemployment rate values
grouped3 = bls.groupby(['Area', 'Year'])['Unemployment Rate'].mean().reset_index(name = 'Unemployment Rate')

#Dropping columns for month and unemployment rate 
bls = bls.drop(columns = 'Month')
bls = bls.drop(columns = 'Unemployment Rate')

#Dropping all duplicate values for year and area so that there is only one value for a year and area (i.e. Chicago 1990 only has one value)
bls = bls.drop_duplicates(subset = ['Year', 'Area'], keep = 'first')
bls = bls.reset_index(drop = True)

#Adding the average unemployment rate stored in grouped3 as a column to bls
bls['Avg. Unemployment Rate'] = grouped3['Unemployment Rate']


##Merging Geocorr and Bls dataframes

#Saved Area FIPS codes as a variable previously. Read it to the BLS data frame and cleaned it to match the BLS data set
area_fips = area_fips.sort_values(by = ['Area', 'Year'])
area_fips = area_fips.drop(['LAUS Code', 'ST FIPS Code', 'Civilian Labor Force', 'Employment', 'Unemployment'], index = None, axis = 1)
area_fips = area_fips.drop(columns = ['Month', 'Unemployment Rate']).reset_index(drop = True)
area_fips = area_fips.drop_duplicates(subset = ['Year', 'Area'], keep = 'first')
area_fips = area_fips.reset_index(drop = True)

#Creating a new column with area_fips 'Area FIPS Code column' 
bls['Area FIPS Code'] = area_fips['Area FIPS Code']

#Merge Geocorr with BLS
result = pd.merge(geocorr, bls, on = 'Area FIPS Code', how = 'right')

#Rename GeoName column in BEA data set to County to match with the results of merge file before 
bea = bea.rename(columns = {'GeoName':'County'})
result['Year'] = pd.to_numeric(result['Year'], errors='coerce') #changing Year column type to number

#Merging Result and bea on Year column and further narrowing it by only having entries between the years 2005 - 2007
final_merge = pd.merge(result, bea, on = ['Year'], how = 'inner')
final_merge = final_merge.drop(final_merge[final_merge['Year'] > 2007].index)
final_merge = final_merge.drop(final_merge[final_merge['Year'] < 2005].index)
final_merge.sort_values(by = 'County_x')

#Dropping extra county column 
final_merge = final_merge.drop(['County_y'], axis = 1)
final_merge.isna().any()
final_merge.to_excel('test.xlsx')