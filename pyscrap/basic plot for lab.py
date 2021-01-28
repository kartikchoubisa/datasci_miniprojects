xs = (
    4.716981132,
    11.53846154,
    21.66666667,
    47.72727273,
    62.5,
    2.5,
    23.68421053,

)

ys = (
    4.285,
    4.2,
    4.394,
    4.276,
    4.501,
    4.373,
    4.193,

)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

xy = sorted(list(zip(xs,ys)), key = lambda x: x[0])
print(xy)
xs, ys = list(zip(*xy))

plt.style.use('fast')
fig,ax = plt.subplots()
plt.xlabel('velocity (cm/sec)')
plt.ylabel('Flux')
plt.title(f'Total Flux vs velocity (including both tubes)')
ax.plot(xs,ys)
plt.show()