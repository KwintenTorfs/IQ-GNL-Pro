import os

import numpy as np


a = [[1, 2, 3], ['a', 'b', 'c']]

event = 'b'

i = a[1].index(event)
print(a[0][i])