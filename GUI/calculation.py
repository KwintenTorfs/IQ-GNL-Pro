import os

import numpy as np
import pandas as pd

from Calculations.Image_Import import Image
from GUI.table import create_table_header, table_header
from GUI.export import patient_parameters, slice_parameters, study_parameters, scanner_parameters
from Calculations.calculation_functions import calculations
path = r'D:\Quick Images\Kernel Size GNL2'
save_location = r'D:\Quick Images'

header = table_header(False)
header.remove('Calculation technique')
df = pd.DataFrame(None, columns=header)


for fol in os.listdir(path):
    image = Image(path, fol)
    if not image.valid:
        continue
    parameters = study_parameters
    result = parameters.copy()
    for parameter in parameters.keys():
        result[parameter] = calculations[parameter](image)

