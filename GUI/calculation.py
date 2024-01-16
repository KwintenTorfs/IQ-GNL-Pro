import datetime
import os
import numpy as np
import pandas as pd
from GUI.save import operations_save, save_txt
from GUI.table import pre_and_suffix
from GUI.export import gnl_pre_text
from GUI.technique import technique_parameters
from Calculations.calculation_functions import calculations, image_processing, image_processing_operations
from Calculations.Global_Noise import construct_noise_map, global_noise_from_noise_map, standard_slice, \
    get_kernel_in_pixel
from GUI.calculation_folders_to_files import get_calculable_slices
from pytictoc import TicToc

from configuration import ROOT_DIR

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


def calculate_list_of_image_slices(image_slices, slice_dataframe, hounsfield_ranges, save_location,
                                   calculate_image_parameters, calculate_gnl, window, save_type):
    filename = os.path.basename(save_location)
    save_folder = os.path.dirname(save_location)
    temporary_save_location = str(os.path.join(save_folder, 'TEMP ' + filename).split('.')[0]) + '.txt'
    # Heading gives all parameters that need to be calculated
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
        # This is used to have also a temporary file
        try:
            save_txt(slice_dataframe, temporary_save_location)
        except PermissionError:
            log(window, 'PERMISSION ERROR -----> Save file FOLDER is opened somewhere else')
        log(window, string_image % (i + 1) + '/%i  ' % nb_images + image.filename + '  added to save location')
    return data


def process_list_of_image_slices(image_slices, slice_dataframe, hounsfield_ranges, save_location,
                                 calculate_image_parameters, calculate_gnl, window, save_type):
    data = calculate_list_of_image_slices(image_slices, slice_dataframe, hounsfield_ranges, save_location,
                                          calculate_image_parameters, calculate_gnl, window, save_type)
    try:
        operations_save[save_type](slice_dataframe, save_location)
    except PermissionError:
        log(window, 'PERMISSION ERROR -----> Save file FOLDER is opened somewhere else')
    return data


def process_list_of_folders(source_paths, slice_dataframe, scan_dataframe, hounsfield_ranges, save_location_files,
                            save_location_scans, image_param, calculate_gnl, window, save_type):
    t = TicToc()
    filename = os.path.basename(save_location_scans)
    save_folder = os.path.dirname(save_location_scans)
    temporary_save_location = str(os.path.join(save_folder, 'TEMP ' + filename)).split('.')[0] + '.txt'
    header_scan = list(scan_dataframe.head())
    nb_folders = len(source_paths)
    string_folder = '%%0%id' % len(str(nb_folders))
    t.tic()
    for i, folder in enumerate(source_paths):
        slices, measurements = get_calculable_slices(folder)
        data = calculate_list_of_image_slices(image_slices=slices,
                                              slice_dataframe=slice_dataframe,
                                              hounsfield_ranges=hounsfield_ranges,
                                              save_location=save_location_files,
                                              calculate_image_parameters=image_param,
                                              calculate_gnl=calculate_gnl,
                                              window=window,
                                              save_type=save_type)

        for method in measurements.keys():
            nb_slices = len(measurements[method])
            if nb_slices < 1:
                continue
            scan_info = dict(zip(header_scan, [None] * len(header_scan)))
            for parameter in scan_info.keys():
                if pre_and_suffix['AVG'] in parameter:
                    original_parameter = parameter.split(pre_and_suffix['AVG'])[1]
                    parameter_array = np.take(np.array(data[original_parameter]), np.array(measurements[method]))
                    try:
                        scan_info[pre_and_suffix['AVG'] + original_parameter] = np.nanmean(parameter_array)
                    except RuntimeWarning:
                        scan_info[pre_and_suffix['AVG'] + original_parameter] = None
                    try:
                        scan_info[pre_and_suffix['STD'] + original_parameter] = np.nanstd(parameter_array)
                    except RuntimeWarning:
                        scan_info[pre_and_suffix['STD'] + original_parameter] = None
                elif pre_and_suffix['STD'] in parameter:
                    pass
                elif parameter == 'Calculation Method':
                    scan_info[parameter] = method
                elif parameter == 'NB Slices':
                    scan_info[parameter] = nb_slices
                elif parameter == 'Path':
                    scan_info[parameter] = folder
                else:
                    scan_info[parameter] = data[parameter][0]
            scan_dataframe.loc[len(scan_dataframe)] = scan_info.values()

            # This is used to have also a temporary file
            try:
                save_txt(scan_dataframe, temporary_save_location)
            except PermissionError:
                log(window, 'PERMISSION ERROR -----> Save file FOLDER is opened somewhere else')

        log(window, '')
        log(window, string_folder % (i + 1) + '/%i  ' % nb_folders + folder + '  PROCESSED')
        log(window, '')
    t.toc()
    try:
        operations_save[save_type](slice_dataframe, save_location_files)
    except PermissionError:
        log(window, 'PERMISSION ERROR -----> Save file FOLDER is opened somewhere else')
    try:
        operations_save[save_type](scan_dataframe, save_location_scans)
    except PermissionError:
        log(window, 'PERMISSION ERROR -----> Save file FOLDER is opened somewhere else')


def log(window, message, timestamp=True):
    now = datetime.datetime.now()
    prefix = ''
    if timestamp:
        date = '%04d-%02d-%02d' % (now.year, now.month, now.day)
        time = '%02d:%02d:%02d' % (now.hour, now.minute, now.second)
        prefix = date + '  ' + time + '   '
    window['LOG'].update(prefix + message+'\n', append=True)
    add_to_active_log(prefix + message)


def create_log():
    open('current_log.txt', 'w')


def add_to_active_log(log_string):
    if os.path.exists('current_log.txt'):
        f = open('%scurrent_log.txt' % ROOT_DIR, 'a')
    else:
        f = open('%scurrent_log.txt' % ROOT_DIR, 'w')
    f.write(log_string + '\n')
    f.close()
    return
