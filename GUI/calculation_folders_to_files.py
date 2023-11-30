import os
import numpy as np
from natsort import natsorted
from Calculations.Image_Import import Image
from GUI.technique import technique_parameters


scan_codes = {'GNL MID AX': 'M',
              'GNL 10 SLICE': 'T',
              'GNL X SLICE': 'X',
              'GNL ALL SLICE': 'A'}


def select_number_of_positions(list_len: int, no_slices: int):
    """
        Function to take a set amount of equidistant slices in ar array with specific length

        Parameters
        ----------
        list_len : int
            Length of the array
        no_slices : int
            Number of equidistant slices

        Returns
        -------
        array:
            -An array of the positions in the list that make up the equidistant slices
    """
    try:
        division_length = list_len / no_slices
        overshoot_per_side = (division_length - 1) / 2
        exact_positions = np.arange(overshoot_per_side, list_len, division_length)
        return np.array(np.round(exact_positions), dtype=int)
    except ZeroDivisionError:
        return np.array([], dtype=int)


def get_valid_slices(directory: str):
    """
            Returns all the slices in a directory that are valid Image Classes

            Parameters
            ----------
            directory : str
                Path to a local directory with dicom images of one CT scan

            Returns
            -------
            list :
                -valid_slices (list[Image]) : A list of valid Image elements
        """
    valid_slices = []
    for slab in natsorted(os.listdir(directory)):
        image = Image(directory, slab, process=False)
        if image.valid:
            valid_slices.append(image)
    return valid_slices


def get_calculable_slices(source_dir: str):
    """
            Determines which slices of a CT image stack should be used to calculate the average in certain amount of
            slices, all slices and/or the mid-axial value.

            Parameters
            ----------
            source_dir : str
                Path to a local directory with dicom images of one CT scan

            Returns
            -------
            tuple: a tuple containing
                -calculation_slices (list[Image]) : A list of valid Image elements
                -calculation_positions (list[Image]) : A list of the Image positions necessary for GNL AVG, MID AXD...
    """
    global scan_codes
    slices = get_valid_slices(directory=source_dir)
    nb_slices = len(slices)
    calculation_positions = {key: [] for key in scan_codes.keys()}
    if technique_parameters['GNL X SLICE']:
        positions_average_x = select_number_of_positions(nb_slices, int(technique_parameters['NB']))
        scans_average_x = [slices[position] for position in positions_average_x]
    else:
        scans_average_x = []

    if technique_parameters['GNL ALL SLICE']:
        scans_average_all = slices.copy()
    else:
        scans_average_all = []

    if technique_parameters['GNL 10 SLICE']:
        positions_average_10 = select_number_of_positions(nb_slices, 10)
        scans_average_10 = [slices[position] for position in positions_average_10]
    else:
        scans_average_10 = []

    if technique_parameters['GNL MID AX'] and nb_slices > 0:
        position_mid_axial = nb_slices // 2
        scans_mid_axial = [slices[position_mid_axial]]
    else:
        scans_mid_axial = []

    to_calculate_list = scans_average_10.copy()
    to_calculate_list.extend(scans_average_x)
    to_calculate_list.extend(scans_average_all)
    to_calculate_list.extend(scans_mid_axial)
    calculation_slices = list(set(to_calculate_list))
    slice_method = [''] * len(calculation_slices)

    for i, slab in enumerate(calculation_slices):
        if slab in scans_mid_axial:
            slice_method[i] += scan_codes['GNL MID AX']
            calculation_positions['GNL MID AX'] += [i]
        if slab in scans_average_10:
            calculation_positions['GNL 10 SLICE'].append(i)
        if slab in scans_average_x:
            calculation_positions['GNL X SLICE'].append(i)
        if slab in scans_average_all:
            calculation_positions['GNL ALL SLICE'].append(i)
    return calculation_slices, calculation_positions
