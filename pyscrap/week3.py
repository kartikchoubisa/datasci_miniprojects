import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995])

df['mean'] = df.mean(axis = 1)
df['std'] = df.std(axis = 1)
df['sem'] = df.sem(axis = 1)
df['i_min']=df['mean']-df['sem']*4
df['i_max']=df['mean']+df['sem']*4
df['yerr']=df['sem']*4

y = 35000 # change this parameter
color_up = '#BB0A21'
color_in = '#E9EDDE'
color_down = '#427AA1'

fig, ax = plt.subplots()



colors = []
for i, row in df.iterrows():
  if y > row['i_max']:
    colors.append(color_up)
  elif y < row['i_min']:
    colors.append(color_down)
  else:
    colors.append(color_in)


ax.bar(df.index, df['mean'], yerr = df['yerr'], color = colors)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(bottom = False)
ax.set_xticks([1992, 1993, 1994, 1995])

# ax.plot([0, 199], [y,y])

plt.show()