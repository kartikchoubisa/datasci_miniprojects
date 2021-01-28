import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('lab_data.xlsx',header=None)

plt.style.use('fast')
print(df)
for i in range(0,7*3,3):
    c_1 = df.iloc[:,i:i+3]
    c_1.columns = [0,1,2]

    U_max = c_1[1][2:].astype(float).idxmax()/100,  c_1[1][2:].max()
    U_min = c_1[1][2:].astype(float).idxmin()/100, c_1[1][2:].min()
    U = U_max[1]-U_min[1]
    U = round(float(U),2)

    fig,ax = plt.subplots()



    plt.xlabel('time (sec)')
    plt.ylabel('EMF (Volt)')
    size = c_1[0][0]
    metal = 'plastic' if c_1[0][1].lower().endswith('p') else 'copper'
    plt.title(f'{metal}, h={size}')
    ax.plot(c_1.iloc[2:,0], c_1.iloc[2:,1])


    plt.annotate(f'U = {U}', xy =(1.65,0.2))
    plt.annotate('', (1.6, U_max[1]), (1.6, U_min[1]), arrowprops={'arrowstyle': '<->'})

    ax.plot(U_max[0], U_max[1], '_', color = 'black')
    ax.plot(U_min[0], U_min[1], '_', color = 'black')

    plt.ylim(-1.2,1.2)
    plt.xlim(0,2)

    print(c_1[0][1])


    # plt.show()
    plt.savefig(f'{metal}, {size}.png')


    plt.cla()

    plt.xlabel('time (sec)')
    plt.ylabel('Photoguage output (Volts)')
    plt.title(f'{metal}, h={size}')
    ax.plot(c_1.iloc[2:,0], c_1.iloc[2:,2])
    plt.savefig(f'pv_{metal}, {size}.png')
    print(c_1)