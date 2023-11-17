import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Calculations.Image_Import import Image
from GUI.table import create_table_header, table_header, pre_and_suffix
from GUI.export import patient_parameters, slice_parameters, study_parameters, scanner_parameters, tissue_parameters, \
    gnl_pre_text
from Support.Hounsfield_Units import get_hounsfield_dictionary
from Calculations.calculation_functions import calculations
from Calculations.Global_Noise import construct_noise_map, global_noise_from_noise_map, standard_slice
from configuration import ROOT_DIR

path = r'D:\Quick Images\Kernel Size GNL2'
save_location = r'%s\Temporary\Test.xlsx' % ROOT_DIR

parameters_that_need_masking = ['WED (cm)', 'SSDE (mGy)', 'Truncation Correction', 'Truncation']

# for p in patient_parameters.keys():
#     patient_parameters[p] = True
# for p in slice_parameters.keys():
#     slice_parameters[p] = True
# for p in study_parameters.keys():
#     study_parameters[p] = True
# for p in scanner_parameters.keys():
#     scanner_parameters[p] = True
tissue_parameters['GNL Soft Tissue'] = True
tissue_parameters['GNL Lung Tissue'] = True


header = table_header(False)
# header.remove('Calculation technique')
df = pd.DataFrame(None, columns=header)

folder_list = os.listdir(path)

hounsfield_ranges = get_hounsfield_dictionary()
gnl_calculation = False

for param in header:
    if gnl_pre_text in param:
        gnl_calculation = True
        break


for fol in folder_list:
    image = Image(path, fol)
    if not image.valid:
        continue
    selected_parameters = header
    info = dict(zip(header, [None] * len(header)))

    kernel = 7
    noise_map = construct_noise_map(image.body, mask_size=7)
    #todo change kernel

    for parameter in info.keys():
        print(parameter)
        if parameter in calculations.keys():
            info[parameter] = calculations[parameter](image)
        elif gnl_pre_text in parameter and pre_and_suffix['STD SLICE'] not in parameter:
            print(parameter)
            tissue = (parameter.split(gnl_pre_text)[1]).split(pre_and_suffix['HU'])[0]
            low, high = hounsfield_ranges[tissue]
            info['%s%s%s' % (tissue, pre_and_suffix['LOW'], pre_and_suffix['HU'])] = low
            info['%s%s%s' % (tissue, pre_and_suffix['HIGH'], pre_and_suffix['HU'])] = high
            gnl_mode, gnl_median = global_noise_from_noise_map(image.body, noise_map, [low, high])
            info[parameter] = gnl_mode
            info['%s%s%s' % (parameter, pre_and_suffix['STD SLICE'], pre_and_suffix['HU'])] = \
                gnl_mode * np.sqrt(standard_slice[list(standard_slice.keys())[0]]) / np.sqrt(image.SliceThickness)
    df.loc[len(df)] = info.values()
    df.to_excel(save_location)
