import os.path
import threading

import PySimpleGUI as sg
from Calculations.Image_Import import Image
from Constants.design_GUI import text, TextFont
from GUI.folders import folders_parameters, methods
from GUI.technique import technique_parameters
from GUI.calculation import table_header, process_list_of_image_slices, necessary_image_class_calculations, log
from GUI.save import get_save_locations
import pandas as pd

from Support.Hounsfield_Units import get_hounsfield_dictionary


def calculate_layout():
    layout = [[sg.Multiline(key='LOG', text_color=text, font=TextFont, expand_x=True, expand_y=True,
                            autoscroll=True, write_only=True, disabled=True)],
              [sg.Push(),
               sg.Button('Calculate', key='CALCULATE', button_color=(text, 'white'), font=TextFont)]]
    return layout


def calculate_events(window, event, value):
    if event == 'CALCULATE':
        # todo Give a notification if you are still in default save location or filename
        # todo Give a check whether a certain file already exists + override or not
        # todo
        log(window, '-' * 130)
        log(window, 'CALCULATION STARTED')
        log(window, '-' * 130)
        log(window, 'SETTINGS')
        type_of_input = input_folder_type()
        log(window, '\t\t Input type: \t\t %s' % type_of_input)
        source_paths = folders_parameters['%s FILES' % type_of_input][0]
        slices_header = table_header(False)
        calculate_gnl, image_param = necessary_image_class_calculations(slices_header)
        dataframe_slice = pd.DataFrame(data=None, columns=slices_header)
        calculate_per_scan = calculation_per_scan()
        log(window, '\t\t Avg per scan: \t\t %s' % calculate_per_scan)
        hounsfield_ranges = get_hounsfield_dictionary()
        save_location_files, save_location_scans = get_save_locations()
        log(window, '\t\t Save location: \t\t %s' % save_location_scans)
        log(window, 'PARAMETERS')
        for parameter in slices_header:
            log(window, '\t\t %s: \t\t %s' % (parameter, True))
        log(window, '-' * 130)
        if not calculate_per_scan:
            log(window, 'START SLICE MEASUREMENT')
            images = images_for_measurement_per_slice(type_of_input, source_paths)
            log(window, 'Number of images to process: %i' % len(images))
            threading.Thread(target=process_list_of_image_slices,
                             args=(images, dataframe_slice, hounsfield_ranges, save_location_files, image_param,
                                   calculate_gnl, window),
                             daemon=True).start()

        else:
            folders = folders_for_measurement_per_scan(type_of_input, source_paths)

    return


def input_folder_type():
    """
        Return the type of data is given (database, scans, images)

        Returns
        -------
        str:
            -method (str) : data type = DB, SCAN or IMAGE
        """
    for method in methods.values():
        if folders_parameters[method]:
            return method
    return None


def calculation_per_scan():
    """
        Return whether there are measurements per scan

        Returns
        -------
        bool:
            -bool : True if measured per scan
    """
    per_scan = technique_parameters['PER SCAN']
    per_slice = technique_parameters['PER SLICE']
    if per_scan and not per_slice:
        return True
    return False


def images_for_measurement_per_slice(type_of_input: str, source_paths: list[str]):
    """
        Find all valid slices in the input source paths. For IMAGES, check all source paths. For SCAN, search the
        different images in the scan. For DB, search different images in the different scans in the DBs. Return the
        Image class objects

        Parameters
        -------
        type_of_input: str
            The type of data involved: DB, SCAN or IMAGE
        source_paths: list[str]
            List of the paths to the different DBS, SCANS or IMAGES

        Returns
        -------
        list:
            -images (list[Image]) : List of all valid images, represented as an unprocessed Image File
    """
    images = []
    if type_of_input == 'IMAGE':
        for path in source_paths:
            directory = os.path.dirname(path)
            filename = os.path.basename(path)
            current_image = Image(directory, filename, process=False)
            if current_image.valid:
                images.append(current_image)
    elif type_of_input == 'SCAN':
        for directory in source_paths:
            for filename in os.listdir(directory):
                current_image = Image(directory, filename, process=False)
                if current_image.valid:
                    images.append(current_image)
    elif type_of_input == 'DB':
        for database in source_paths:
            for dir_name in os.listdir(database):
                directory = os.path.join(database, dir_name)
                for filename in os.listdir(directory):
                    current_image = Image(directory, filename, process=False)
                    if current_image.valid:
                        images.append(current_image)
    else:
        return None
    return images


def folders_for_measurement_per_scan(type_of_input: str, source_paths: list[str]):
    """
        Find all valid folders in the input source paths. For IMAGES, this is None. For SCAN, these are the individual
        scan folders. For DB, search the different scans in the DBs.

        Parameters
        -------
        type_of_input: str
            The type of data involved: DB, SCAN or IMAGE
        source_paths: list[str]
            List of the paths to the different DBS, SCANS or IMAGES

        Returns
        -------
        list:
            folders (list[str]) : List of all scans (sub folders) in the different databases
    """
    folders = []
    if type_of_input == 'SCAN':
        folders = source_paths
    elif type_of_input == 'DB':
        for source in source_paths:
            for directory in os.listdir(source):
                folder_path = os.path.join(source, directory)
                if os.path.isdir(folder_path):
                    folders.append(os.path.join(folder_path))
    else:
        return None
    return folders

