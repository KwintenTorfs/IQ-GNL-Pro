import os

import numpy as np


folder = r'C:\Users\ktorfs5\OneDrive - KU Leuven\Biomedical Interns\Amber De Vos'

folders_parameters = {'DB': False,
                      'SCAN': False,
                      'IMAGE': True,
                      'DB LOCATION': '',
                      'SCAN LOCATION': '',
                      'IMAGE LOCATION': '',
                      'DB FILES': [[], []],
                      'SCAN FILES': [[], []],
                      'IMAGE FILES': [[], []]}


def find_sibling_directories(selected_location, method):
    global folders_parameters
    files = '%s FILES' % method
    location_list = folders_parameters[files][0]
    parent_folder = os.path.abspath(os.path.join(selected_location, os.pardir))
    sibling_folders, sibling_locations = [], []
    for f in os.scandir(parent_folder):
        if f.is_dir():
            location = f.path.replace('\\', '/')
            print(location)
            print(selected_location)
            directory = os.path.basename(location)
            if location not in location_list and location != selected_location:
                sibling_folders.append(directory)
                sibling_locations.append(location)
    return sibling_folders, sibling_locations
