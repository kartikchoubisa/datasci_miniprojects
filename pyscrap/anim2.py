import pandas as pd
import numpy as np
from scipy import stats

town_data = pd.Series(dtype='string')
with open('university_towns.txt') as f:
    for line in f.readlines():
        if list(line)[-7:-1] == list('[edit]'):
            state = line
        else:
            town_data = town_data.append(pd.Series([line], index = [state]))

town_data = town_data.to_frame().reset_index()
town_data = town_data.rename(columns={'index': 'State', 0: 'Town'})
# town_data = town_data.applymap(lambda x: x.strip())
town_data['State'] = town_data['State'].replace(to_replace = '\[.*', value = "", regex = True).str.strip()
town_data['Town'] = town_data['Town'].replace(to_replace = '\(.*', value = "", regex = True).str.strip()

# print(town_data[town_data['State'] == 'Massachusetts'])
# town_data.to_csv("uni_towns.csv")

# import pandas as pd
# df = pd.read_csv('uni_towns.csv', index_col= [0])
# print(df)

gdp = pd.read_excel('gdplev.xls', usecols='E:G', skiprows = range(8), header = None)
gdp = gdp[[4, 6]].rename(columns={4: 'Quarter', 6: 'GDP'})
gdp = gdp.set_index(['Quarter'])
# print(gdp)

rec_start = gdp['GDP'].rolling(3).apply(lambda x: x.iloc[0]>x.iloc[1]>x.iloc[2])
rec_start = rec_start.shift(-1)

def find_rec(gdp):
    df = gdp.copy()
    # df[['start', 'end']] = df[['start', 'end']].applymap(int)
    recessions_list = []

    while True:
        starts, ends = False, False
        if len(df.index) <= 3:
            print('df too small')
            break

        for i in range(0, len(df.index)):
            if df['start'][i] == float(1):
                starts = True
                start_loc = i
                break
        else:
            print('no recssion left')
            starts = False
            break

        if starts:
            for j in range(start_loc+1, len(df.index)):
                if df['end'][j] == float(1):
                    ends = True
                    end_loc = j
                    break
            else:
                print('last recession started, but not ended yet')
                ends = False
                break


        if starts and ends:
            recessions_list.append(df.iloc[start_loc: end_loc+1].copy())
            df.iloc[:end_loc+1] = np.NaN
            df = df.dropna()

        elif starts and not ends:
            print(f'last recssion start: {df.iloc[start_loc]}')
            break

        elif not starts and ends:
            print('something wrong')
            break

        elif not starts and not ends:
            print('no recssions left')
            break
        # print(df)####

    return recessions_list

rec_end = gdp['GDP'].rolling(3).apply(lambda x: x.iloc[0] < x.iloc[1] < x.iloc[2])
gdp['start'], gdp['end'] = rec_start, rec_end
# print(gdp)

# housing = pd.read_csv('City_Zhvi_AllHomes.csv')
# states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
# housing['State'].replace(states, inplace = True)
# housing.set_index(['State', 'RegionName'], inplace = True)
# housing.drop(columns=['RegionID', 'Metro', 'CountyName', 'SizeRank'], inplace=True)
# housing = housing.groupby(pd.PeriodIndex(housing.columns, freq='Q'), axis = 1).mean()
# housing = housing.loc[:, pd.Period('2000Q1'):]
#
# housing.to_csv('housing_cleaned.csv')

housing = pd.read_csv('housing_cleaned.csv', index_col = [0,1])
housing.columns = housing.columns.str.lower()

housing['ratio'] = housing.apply(lambda x: x['2008q2']/x['2009q2'], axis = 1)




# housing[housing['RegionName'] == 'Lynchburg']
uni_towns = town_data
uni_towns.set_index(['State', 'Town'], inplace= True)

utown_df = housing.loc[housing.index.intersection(uni_towns.index)]
non_utown_df = housing.loc[housing.index.difference(uni_towns.index)]

print(utown_df.shape, non_utown_df.shape)

# housing =  set(uni_towns['Town']).intersection(set(housing.reset_index().RegionName))

result = stats.ttest_ind(utown_df['ratio'].dropna(), non_utown_df['ratio'].dropna())
# result = utown_df.agg(np.mean, axis = 1)

# print(utown_df[utown_df['ratio'].isnull()][['2008q2', '2009q2']], non_utown_df['ratio'].isnull())

print(result)

