import os.path
import threading

import FreeSimpleGUI as sg
from Calculations.Image_Import import Image
from Constants.Images.images_b64 import image_rescale, CALCULATOR
from Constants.design_GUI import text, TextFont, MenuFont, light_accent, accent
from GUI.folders import folders_parameters, methods
from GUI.table import table_header
from GUI.technique import technique_parameters
from GUI.calculation import process_list_of_image_slices, necessary_image_class_calculations, log, \
    process_list_of_folders
from GUI.save import get_save_locations, save_parameters
from GUI.popups import popup_yes_no
import pandas as pd

from Support.Hounsfield_Units import get_hounsfield_dictionary


def calculate_layout():

    calculate_button = sg.Frame('', layout=[[sg.Text(background_color='white', key='CALCULATE LEFT', expand_x=True),
                                             sg.Button('', image_data=image_rescale(CALCULATOR, 17, 25),
                                                       image_size=(17, 25), button_color='white', border_width=0,
                                                       key='CALCULATE ICON', size=(20, 1), enable_events=True),
                                             sg.Button('Calculate', button_color=(text, 'white'), font=MenuFont,
                                                       border_width=0, key='CALCULATE', enable_events=True),
                                             sg.Text(background_color='white', key='CALCULATE RIGHT', expand_x=True)]],
                                background_color='white', border_width=0, key='CALCULATE FRAME', size=(140, 35))

    layout = [[sg.Multiline(key='LOG', text_color='blue', font=TextFont, expand_x=True, expand_y=True,
                            autoscroll=True, write_only=True, disabled=True)],
              [sg.Push(),
               calculate_button
               ]]
    return layout


def calculate_bindings(window):
    window['CALCULATE'].bind('<Enter>', '+MOUSE OVER+')
    window['CALCULATE'].bind('<Leave>', '+MOUSE AWAY+')
    window['CALCULATE FRAME'].bind('<Enter>', '+MOUSE OVER+')
    window['CALCULATE FRAME'].bind('<Leave>', '+MOUSE AWAY+')
    window['CALCULATE ICON'].bind('<Enter>', '+MOUSE OVER+')
    window['CALCULATE ICON'].bind('<Leave>', '+MOUSE AWAY+')
    window['CALCULATE ICON'].bind('<Enter>', '+MOUSE OVER+')
    window['CALCULATE ICON'].bind('<Leave>', '+MOUSE AWAY+')
    window['CALCULATE LEFT'].bind('<Enter>', '+MOUSE OVER+')
    window['CALCULATE LEFT'].bind('<Leave>', '+MOUSE AWAY+')
    window['CALCULATE RIGHT'].bind('<Enter>', '+MOUSE OVER+')
    window['CALCULATE RIGHT'].bind('<Leave>', '+MOUSE AWAY+')
    window['CALCULATE FRAME'].Widget.configure(highlightbackground=text, highlightcolor=text, highlightthickness=1)


def calculate_events(window, event, _):
    if event in ['CALCULATE', 'CALCULATE ICON']:
        window['CALCULATE'].update(button_color='white')
        window['CALCULATE ICON'].update(button_color='white')
        window['CALCULATE FRAME'].Widget.config(background='white')
        window['CALCULATE LEFT'].Widget.config(background='white')
        window['CALCULATE RIGHT'].Widget.config(background='white')
        window['CALCULATE FRAME'].Widget.configure(highlightbackground=text, highlightcolor=text, highlightthickness=1)
        window['CALCULATE'].ParentRowFrame.config(background='white')
        window['CALCULATE ICON'].ParentRowFrame.config(background='white')
        save_location_files, save_location_scans = get_save_locations()
        if os.path.isfile(save_location_scans):
            log(window, os.path.basename(save_location_scans) + ' already exists in folder ' +
                os.path.dirname(save_location_scans))
            go_on = popup_yes_no(os.path.basename(save_location_scans) + ' already exists.\nDo you want to replace it?',
                                 'Confirm Save As')
            if go_on:
                log(window, save_location_scans + ' ----------> OVERWRITE')
            else:
                window.Element('Save').Select()
                return
        log(window, '-' * 130)
        log(window, 'CALCULATION STARTED')
        log(window, '-' * 130)
        log(window, 'SETTINGS')
        type_of_input = input_folder_type()
        log(window, '\t\t Input type: \t\t %s' % type_of_input)
        source_paths = folders_parameters['%s FILES' % type_of_input][0]
        slices_header = table_header(False)
        if len(slices_header) < 1:
            log(window, '')
            log(window, 'No Export Parameters selected')
            log(window, '')
            return
        scan_header = table_header(True)
        calculate_gnl, image_param = necessary_image_class_calculations(slices_header)
        dataframe_slice = pd.DataFrame(data=None, columns=slices_header)
        dataframe_scan = pd.DataFrame(data=None, columns=scan_header)
        calculate_per_scan = calculation_per_scan()
        log(window, '\t\t Avg per scan: \t\t %s' % calculate_per_scan)
        hounsfield_ranges = get_hounsfield_dictionary()
        save_type = save_parameters['FILE TYPE']
        log(window, '\t\t Save location: \t\t %s' % save_location_scans)
        log(window, 'PARAMETERS')
        for parameter in slices_header:
            log(window, '\t\t %s: \t\t %s' % (parameter, True))
        log(window, '-' * 130)
        if not calculate_per_scan:
            log(window, 'START SLICE MEASUREMENT')
            log(window, '')
            images = images_for_measurement_per_slice(type_of_input, source_paths)
            log(window, 'Number of images to process: %i' % len(images))
            threading.Thread(target=process_list_of_image_slices,
                             args=(images, dataframe_slice, hounsfield_ranges, save_location_files, image_param,
                                   calculate_gnl, window, save_type),
                             daemon=True).start()

        else:
            log(window, 'START SCAN MEASUREMENT')
            log(window, '')
            folders = folders_for_measurement_per_scan(type_of_input, source_paths)
            log(window, 'Number of folders to process: %i' % len(folders))
            log(window, '')
            threading.Thread(target=process_list_of_folders,
                             args=(folders, dataframe_slice, dataframe_scan, hounsfield_ranges, save_location_files,
                                   save_location_scans, image_param, calculate_gnl, window, save_type),
                             daemon=True).start()

    elif event in ['CALCULATE+MOUSE OVER+', 'CALCULATE ICON+MOUSE OVER+', 'CALCULATE FRAME+MOUSE OVER+',
                   'CALCULATE LEFT+MOUSE OVER+', 'CALCULATE RIGHT+MOUSE OVER+']:
        window['CALCULATE'].update(button_color=light_accent)
        window['CALCULATE ICON'].update(button_color=light_accent)
        window['CALCULATE FRAME'].Widget.config(background=light_accent)
        window['CALCULATE LEFT'].Widget.config(background=light_accent)
        window['CALCULATE RIGHT'].Widget.config(background=light_accent)
        window['CALCULATE FRAME'].Widget.configure(highlightbackground=accent, highlightcolor=accent, highlightthickness=1)
        window['CALCULATE'].ParentRowFrame.config(background=light_accent)
        window['CALCULATE ICON'].ParentRowFrame.config(background=light_accent)
    elif event in ['CALCULATE+MOUSE AWAY+', 'CALCULATE ICON+MOUSE AWAY+', 'CALCULATE FRAME+MOUSE AWAY+',
                   'CALCULATE LEFT+MOUSE AWAY+', 'CALCULATE RIGHT+MOUSE AWAY+']:
        window['CALCULATE'].update(button_color='white')
        window['CALCULATE ICON'].update(button_color='white')
        window['CALCULATE FRAME'].Widget.config(background='white')
        window['CALCULATE LEFT'].Widget.config(background='white')
        window['CALCULATE RIGHT'].Widget.config(background='white')
        window['CALCULATE FRAME'].Widget.configure(highlightbackground=text, highlightcolor=text, highlightthickness=1)
        window['CALCULATE'].ParentRowFrame.config(background='white')
        window['CALCULATE ICON'].ParentRowFrame.config(background='white')

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
