import matplotlib.pyplot as plt
import numpy as np

from GUI.calculation import add_to_active_log
from pytictoc import TicToc

t = TicToc()

nb = np.arange(0, 10000)
time = np.zeros(len(nb))
for i in nb:
    t.tic()
    add_to_active_log('HEllo')
    t_val = t.tocvalue()
    time[i] = t_val

plt.plot(nb, time)
plt.show()