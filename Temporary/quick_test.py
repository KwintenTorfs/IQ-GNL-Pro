import os

import numpy as np


a = ['HUohe', 'hjshgk', 'q', 'shdkfvgsiudhvu']

b = max([len(i) for i in a])

columns = [[] for i in range(2)]
for i, word in enumerate(a):
    print(i, word)
    col = np.floor(i / 2).astype(int)
    columns[col].append(word)


