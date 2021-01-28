import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.animation as animation
from random import shuffle
import re

with open("marks.txt") as f:
    lines = [x.strip() for x in f.readlines()]

print(lines)

search = re.compile(".\d$")

marks = []

for i, s in enumerate(lines):
    m = search.findall(s)
    print(search.findall(s))
    if len(m) != 0:
        marks.append(int(m[0]))

print(marks)

print(sum(marks)/len(marks))



