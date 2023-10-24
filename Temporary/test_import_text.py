import os.path
import numpy as np
import pandas as pd

from Support.Hounsfield_Units import add_hounsfield_range, drop_hounsfield_tissue, get_hounsfield_dataframe,\
    constant_source, get_hounsfield_dictionary

add_hounsfield_range('SHIT', [-np.inf, np.inf])
hu = get_hounsfield_dictionary(file='Original Tissue HU.txt')

add_hounsfield_range('BONKO', [0, np.infty])