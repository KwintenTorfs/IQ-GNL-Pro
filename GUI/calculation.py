import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Calculations.Image_Import import Image
from GUI.table import create_table_header, table_header, pre_and_suffix
from GUI.export import patient_parameters, slice_parameters, study_parameters, scanner_parameters, tissue_parameters, \
    gnl_pre_text
from Support.Hounsfield_Units import get_hounsfield_dictionary
from Calculations.calculation_functions import calculations, image_processing, image_processing_operations
from Calculations.Global_Noise import construct_noise_map, global_noise_from_noise_map, standard_slice, \
    get_kernel_in_pixel
from configuration import ROOT_DIR

path = r'D:\Quick Images\Kernel Size GNL'
save_location = r'%s\Temporary\Test.xlsx' % ROOT_DIR


for p in patient_parameters.keys():
    patient_parameters[p] = True
for p in slice_parameters.keys():
    slice_parameters[p] = True
for p in study_parameters.keys():
    study_parameters[p] = True
for p in scanner_parameters.keys():
    scanner_parameters[p] = True

# todo integrate into the tool
# tissue_parameters['GNL Soft Tissue'] = True
# tissue_parameters['GNL Lung Tissue'] = True

header = table_header(False)
# header.remove('Calculation technique')
df = pd.DataFrame(None, columns=header)

folder_list = os.listdir(path)

hounsfield_ranges = get_hounsfield_dictionary()

calculate_image_parameters = {'1 Basic dicom': False,
                              '2 Initialize image': False,
                              '3 Masking': False,
                              '4 WED': False,
                              '5 GNL': False}

# Determine what we need to calculate
for param in header:
    if gnl_pre_text in param:
        for operation in calculate_image_parameters.keys():
            calculate_image_parameters[operation] = True
        break
    elif param in image_processing.keys():
        if image_processing[param] == 'BASIC':
            calculate_image_parameters['1 Basic dicom'] = True
        elif image_processing[param] == 'MASK':
            calculate_image_parameters['1 Basic dicom'] = True
            calculate_image_parameters['2 Initialize image'] = True
            calculate_image_parameters['3 Masking'] = True
        elif image_processing[param] == 'WED':
            calculate_image_parameters['4 WED'] = True
            calculate_image_parameters['2 Initialize image'] = True
            calculate_image_parameters['3 Masking'] = True
            calculate_image_parameters['1 Basic dicom'] = True
            break

calculate_gnl = calculate_image_parameters.pop('5 GNL')
for operation in calculate_image_parameters.copy().keys():
    if not calculate_image_parameters[operation]:
        calculate_image_parameters.pop(operation)


for fol in folder_list:
    image = Image(path, fol, process=False)
    for operation in calculate_image_parameters.keys():
        image_processing_operations[operation](image)
    if not image.valid:
        continue
    selected_parameters = header
    info = dict(zip(header, [None] * len(header)))

    mask_size = 1  # mm
    try:
        kernel = get_kernel_in_pixel(image.PixelSize, mask_size)
    except TypeError:
        kernel = None
    if calculate_gnl:
        noise_map = construct_noise_map(image.body, mask_size=kernel)
    else:
        noise_map = None

    for parameter in info.keys():
        if parameter in calculations.keys():
            info[parameter] = calculations[parameter](image)
        elif gnl_pre_text in parameter and pre_and_suffix['STD SLICE'] not in parameter:
            tissue = (parameter.split(gnl_pre_text)[1]).split(pre_and_suffix['HU'])[0]
            low, high = hounsfield_ranges[tissue]
            info['%s%s%s' % (tissue, pre_and_suffix['LOW'], pre_and_suffix['HU'])] = low
            info['%s%s%s' % (tissue, pre_and_suffix['HIGH'], pre_and_suffix['HU'])] = high
            gnl_mode, gnl_median = global_noise_from_noise_map(image.body, noise_map, [low, high])
            info[parameter] = gnl_mode
            info['%s%s' % (tissue, pre_and_suffix['AREA'])], info['%s%s' % (tissue, pre_and_suffix['PERC'])] = \
                image.get_tissue_measurements([low, high])
            try:
                info['%s%s%s%s' % (gnl_pre_text, tissue, pre_and_suffix['STD SLICE'], pre_and_suffix['HU'])] = \
                    gnl_mode * np.sqrt(standard_slice[list(standard_slice.keys())[0]]) / np.sqrt(image.SliceThickness)
            except TypeError:
                info['%s%s%s%s' % (gnl_pre_text, tissue, pre_and_suffix['STD SLICE'], pre_and_suffix['HU'])] = None

        elif parameter == pre_and_suffix['MASK']:
            info[pre_and_suffix['KERNEL']] = kernel
            info[pre_and_suffix['MASK']] = mask_size

    df.loc[len(df)] = info.values()
    df.to_excel(save_location, sheet_name="Per Slice")


