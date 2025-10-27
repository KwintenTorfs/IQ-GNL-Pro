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
    if list_len < no_slices:
        return np.arange(0, list_len)
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
    nb_slices = len(os.listdir(source_dir))

    positions_all, positions_average_x, positions_average_10, position_mid_axial = [], [], [], []
    if technique_parameters['GNL X SLICE']:
        take_nb = np.min([nb_slices, int(technique_parameters['NB'])])
        positions_average_x = select_number_of_positions(nb_slices, take_nb)

    if technique_parameters['GNL ALL SLICE']:
        positions_all = np.arange(nb_slices)

    if technique_parameters['GNL 10 SLICE']:
        positions_average_10 = select_number_of_positions(nb_slices, 10)

    if technique_parameters['GNL MID AX'] and nb_slices > 0:
        position_mid_axial = [nb_slices // 2]

    positions_needed = np.array(sorted(
        list(set(positions_all) | set(positions_average_x) | set(positions_average_10) | set(position_mid_axial))))
    files = natsorted(os.listdir(source_dir))
    calculation_slices = [Image(source_dir, files[file], process=False) for file in positions_needed]
    calculation_positions = dict()
    calculation_positions['GNL 10 SLICE'] = [np.argwhere(val == positions_needed)[0][0] for val in positions_average_10]
    calculation_positions['GNL X SLICE'] = [np.argwhere(val == positions_needed)[0][0] for val in positions_average_x]
    calculation_positions['GNL ALL SLICE'] = [np.argwhere(val == positions_needed)[0][0] for val in positions_all]
    calculation_positions['GNL MID AX'] = [np.argwhere(val == positions_needed)[0][0] for val in position_mid_axial]
    return calculation_slices, calculation_positions
