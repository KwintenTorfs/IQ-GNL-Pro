import datetime

import numpy as np
import pandas as pd

from GUI.table import table_header, pre_and_suffix
from GUI.export import gnl_pre_text
from GUI.technique import technique_parameters
from Support.Hounsfield_Units import get_hounsfield_dictionary
from Calculations.calculation_functions import calculations, image_processing, image_processing_operations
from Calculations.Global_Noise import construct_noise_map, global_noise_from_noise_map, standard_slice, \
    get_kernel_in_pixel
from configuration import ROOT_DIR
from GUI.calculation_folders_to_files import get_calculable_slices

processing_steps = {'1 Basic dicom': False,
                    '2 Initialize image': False,
                    '3 Masking': False,
                    '4 WED': False,
                    '5 GNL': False}


def necessary_image_class_calculations(heading: list[str]):
    """
            Determine which calculations should be done in a slice, in order to calculate all parameters in the heading

            Parameters
            ----------
            heading : list[str]
                List of all calculable parameters

            Returns
            -------
            tuple: a tuple containing
                -calculate_gnl (bool) : Whether a GNL is calculated
                -calculate_image_parameters (dict(str:bool)) : A dictionary of which Image calculations need to be
                performed
    """
    global processing_steps
    calculate_image_parameters = processing_steps.copy()
    # Determine what we need to calculate
    for param in heading:
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
    calculate_gnl = calculate_image_parameters.pop('5 GNL')
    for operation in calculate_image_parameters.copy().keys():
        if not calculate_image_parameters[operation]:
            calculate_image_parameters.pop(operation)
    return calculate_gnl, calculate_image_parameters


def process_list_of_image_slices(image_slices, slice_dataframe, hounsfield_ranges, save_location,
                                 calculate_image_parameters, calculate_gnl, window):
    # Heading gives all parameters that need to be calculated
    log(window, 'BEGIN PROCESSING...')
    heading = list(slice_dataframe.head())
    mask_size = float(technique_parameters['MASK'])
    data = pd.DataFrame(data=None, columns=heading)
    nb_images = len(image_slices)
    string_image = '%%0%id' % len(str(nb_images))
    for i, image in enumerate(image_slices):
        # Here we do the different operations in the IMAGE class that are necessary to retrieve all info
        for operation in calculate_image_parameters.keys():
            image_processing_operations[operation](image)
        # If the Image Class is not valid, we can not do anything with it
        if not image.valid:
            log(window, image.filename + ' ---------> NOT VALID')
            continue

        info = dict(zip(heading, [None] * len(heading)))
        try:
            kernel = get_kernel_in_pixel(image.PixelSize, mask_size)
        except TypeError:
            kernel = None
        if calculate_gnl:
            noise_map = construct_noise_map(image.body, mask_size=kernel)
        else:
            noise_map = None

        for parameter in info.keys():
            # The dicom information is retrieved from the Image Class
            if parameter in calculations.keys():
                info[parameter] = calculations[parameter](image)
            # GNL info is calculated separately
            elif gnl_pre_text in parameter and pre_and_suffix['STD SLICE'] not in parameter:
                tissue = str(list(parameter.split(gnl_pre_text))[1]).split(pre_and_suffix['HU'])[0]
                low, high = hounsfield_ranges[tissue]
                # Lower limit of HU range for segmentation
                info['%s%s%s' % (tissue, pre_and_suffix['LOW'], pre_and_suffix['HU'])] = low
                # Higher limit of HU range for segmentation
                info['%s%s%s' % (tissue, pre_and_suffix['HIGH'], pre_and_suffix['HU'])] = high
                gnl_mode, gnl_median = global_noise_from_noise_map(image.body, noise_map, [low, high])
                info[parameter] = gnl_mode
                # Area and body percentage of segmented tissue for GNL calculation
                info['%s%s' % (tissue, pre_and_suffix['AREA'])], info['%s%s' % (tissue, pre_and_suffix['PERC'])] = \
                    image.get_tissue_measurements([low, high])
                # Calculate all GNL value for a standard thickness slice
                try:
                    info['%s%s%s%s' % (gnl_pre_text, tissue, pre_and_suffix['STD SLICE'], pre_and_suffix['HU'])] = \
                        gnl_mode * np.sqrt(standard_slice[list(standard_slice.keys())[0]]) / np.sqrt(image.SliceThickness)
                except TypeError:
                    log(window, 'TypeError  --->  GNL %s = None' % tissue)
                    info['%s%s%s%s' % (gnl_pre_text, tissue, pre_and_suffix['STD SLICE'], pre_and_suffix['HU'])] = None

            elif parameter == pre_and_suffix['MASK']:
                info[pre_and_suffix['KERNEL']] = kernel
                info[pre_and_suffix['MASK']] = mask_size

        # Add information to dataframe and matrix
        slice_dataframe.loc[len(slice_dataframe)] = info.values()
        data.loc[len(data)] = info.values()
        try:
            slice_dataframe.to_excel(save_location, sheet_name="Info per slice")
        except PermissionError:
            log(window, 'PERMISSION ERROR -----> Save file is opened somewhere else')
            break
        log(window, string_image % i + '/%i  ' % nb_images + image.filename + '  added to save location')
    log(window, 'PROCESSING FINISHED')
    return data


# path = r'D:\Quick Images\Test Chest\Test 9'
# save_location = r'%s\Temporary\Test.xlsx' % ROOT_DIR
#
#
# for p in patient_parameters.keys():
#     patient_parameters[p] = True
# for p in slice_parameters.keys():
#     slice_parameters[p] = True
# for p in study_parameters.keys():
#     study_parameters[p] = True
# for p in scanner_parameters.keys():
#     scanner_parameters[p] = True
# slice_parameters['Slice Number'] = True
# tissue_parameters['GNL Soft Tissue'] = True
# # tissue_parameters['GNL Lung Tissue'] = True
# technique_parameters['GNL 10 SLICE'] = True
# technique_parameters['GNL X SLICE'] = True
#
# header = table_header(False)
# # header.remove('Calculation technique')
# dataframe_slices = pd.DataFrame(None, columns=header)
# calculation_slices, calculation_positions = get_calculable_slices(path)
#
# hounsfield_ranges = get_hounsfield_dictionary()
#
# mask_size = technique_parameters['MASK']   # mm
# gnl_calculation, image_param = necessary_image_class_calculations(header)
#
# DATA = process_list_of_image_slices(calculation_slices, dataframe_slices, hounsfield_ranges, save_location=save_location)
def log(window, message, timestamp=True):
    now = datetime.datetime.now()
    prefix = ''
    if timestamp:
        date = '%04d-%02d-%02d' % (now.year, now.month, now.day)
        time = '%02d:%02d:%02d' % (now.hour, now.minute, now.second)
        prefix = date + '  ' + time + '   '
    # todo remove comment
    # window['LOG'].update(prefix + message+'\n', append=True)
