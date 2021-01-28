import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('temp.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index(df['Date'])
df_og = df.copy() ### df original is stored here (2005 to 2015)
df = df['2005':'2014']
df['DOY'] = df.Date.dt.strftime('%d %b')
df['year'] = df.Date.dt.strftime('%Y')
df = df.mask(df['DOY'] == '29 Feb', other = np.nan).dropna()
del df['Date']
df.rename({'Data_Value': 'Temp'}, axis = 'columns', errors = 'raise', inplace = True)
df['Temp'] = df['Temp']/10
dfmax = df[df['Element'] == 'TMAX']
dfmin = df[df['Element'] == 'TMIN']

dfmax = dfmax[['Temp', 'DOY', 'year']].groupby('DOY', as_index = False).agg({'Temp': np.max})
dfmin = dfmin[['Temp', 'DOY', 'year']].groupby('DOY', as_index = False).agg({'Temp': np.min})
dfmax['Dateind'] = pd.to_datetime(dfmax['DOY'], format= "%d %b")
dfmin['Dateind'] = pd.to_datetime(dfmax['DOY'], format= "%d %b")
dfmax = dfmax.sort_values('Dateind').drop('Dateind', axis = 1).reset_index(drop=True)
dfmin = dfmin.sort_values('Dateind').drop('Dateind', axis = 1).reset_index(drop=True)

dfmax.to_csv('maxtemp.csv')
dfmin.to_csv('mintemp.csv')


#------ 2015


ly = df_og.copy()['2015']
ly['DOY'] = ly.Date.dt.strftime('%d %b')
ly['year'] = ly.Date.dt.strftime('%Y')
ly = ly.mask(ly['DOY'] == '29 Feb', other = np.nan).dropna()
del ly['Date']
ly.rename({'Data_Value': 'Temp'}, axis = 'columns', errors = 'raise', inplace = True)
ly['Temp'] = ly['Temp']/10

lymax = ly[ly['Element'] == 'TMAX']
lymin = ly[ly['Element'] == 'TMIN']

lymax = lymax[['Temp', 'DOY', 'year']].groupby('DOY', as_index = False).agg({'Temp': np.max})
lymin = lymin[['Temp', 'DOY', 'year']].groupby('DOY', as_index = False).agg({'Temp': np.min})
lymax['Dateind'] = pd.to_datetime(lymax['DOY'], format= "%d %b")
lymin['Dateind'] = pd.to_datetime(lymax['DOY'], format= "%d %b")
lymax = lymax.sort_values('Dateind').drop('Dateind', axis = 1).reset_index(drop=True)
lymin = lymin.sort_values('Dateind').drop('Dateind', axis = 1).reset_index(drop=True)



dfmax['lytemp'] = lymax['Temp']
dfmin['lytemp'] = lymin['Temp']

dfmax = dfmax[dfmax['Temp']<dfmax['lytemp']].drop('Temp', axis = 1)
dfmin = dfmin[dfmin['Temp']>dfmin['lytemp']].drop('Temp', axis = 1)

dfmax.to_csv('lymax.csv')
dfmin.to_csv('lymin.csv')



# --- ---- --- matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl

# plt.style.use('ggplot')
color = {
    'blue' : (119, 158, 203),
}

dfmax = pd.read_csv('maxtemp.csv', index_col=[0])
dfmin = pd.read_csv('mintemp.csv', index_col=[0])
lymax = pd.read_csv('lymax.csv', index_col=[0])
lymin = pd.read_csv('lymin.csv', index_col=[0])

x = dfmax['DOY'].copy()

fig = plt.figure(figsize=(16,8))
ax = fig.add_subplot(111)
ax.plot(x, dfmax['Temp'], color = 'xkcd:blue', alpha = 0.5,
        label = 'Extreme (High and Low) point for each day-of-year through 2005-2014')
ax.plot(x, dfmin['Temp'], color = 'xkcd:blue', alpha = 0.5)
# ax.tick_params(
#     axis = 'x',
#     which = 'both',
#     bottom = False,
#     top = False,
#     labelbottom = True
# )
ax.fill_between(x, dfmax['Temp'], dfmin['Temp'], alpha = 0.5, color = 'lightblue')


ax.scatter(lymax['DOY'], lymax['lytemp'], color = 'orangered',
           label = 'extreme points in 2015 which broke previous record')
ax.scatter(lymin['DOY'], lymin['lytemp'], color = 'orangered')



ax.set_xlabel('Time of the Year')
ax.set_ylabel('Temperature (in degrees celsius)')
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ticks = np.arange(15, 365, 30)
ax.set_xticks(ticks)
ax.tick_params(bottom = False)
ax.set_xticklabels(labels)
ax.set_title('Extreme temperatures through 2005-2014, and record-breaking days in 2015')
ax.legend(loc = 'lower center')


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('plot')
plt.show()
