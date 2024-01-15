import os
import numpy as np
import pandas as pd

from Support.dataframe_operations import change_column_to_data_type
from configuration import ROOT_DIR

constant_source = r'%s\assets' % ROOT_DIR


def get_hounsfield_dataframe(source, file):
    # Will return the hounsfield txt document 'file' and read it as a Dataframe
    try:
        location = os.path.join(source, file)
        dataframe = pd.read_csv(location, sep=';', header=0)
    except (TypeError, FileNotFoundError, ValueError):
        return False
    return dataframe


def get_hounsfield_range(dataframe, tissue):
    # Returns the hounsfield unit range for a specific tissue in a dataframe
    try:
        lo = dataframe.loc[dataframe['Tissue'] == tissue, 'Lower Limit'].iloc[0]
        hi = dataframe.loc[dataframe['Tissue'] == tissue, 'Upper Limit'].iloc[0]
    except (IndexError, AttributeError):
        return None
    return [lo, hi]


def get_hounsfield_dictionary(source=constant_source, file='Current Tissue HU.txt'):
    # Reads in the text file with current hounsfield units and returns the values as a dictionary
    dataframe = get_hounsfield_dataframe(source, file)
    if dataframe is False:
        return dataframe
    change_column_to_data_type(dataframe, 'Lower Limit', float)
    change_column_to_data_type(dataframe, 'Upper Limit', float)
    hounsfield_dict = {}
    try:
        tissues = dataframe['Tissue']
    except TypeError:
        return
    for tissue in tissues:
        hounsfield_range = get_hounsfield_range(dataframe, tissue)
        if hounsfield_range:
            hounsfield_dict[tissue] = hounsfield_range
    return hounsfield_dict


def add_hounsfield_range(tissue, hounsfield_range, source=constant_source):
    # Adds a new tissue with hounsfield units to the currently used text file
    try:
        lo, hi = hounsfield_range
        if lo >= hi:
            return False
    except TypeError:
        return False
    if type(tissue) is not str:
        return False
    dataframe = get_hounsfield_dataframe(source, 'Current Tissue HU.txt')
    if dataframe is False:
        return False
    tissues = np.array(dataframe['Tissue'])
    if tissue in tissues:
        return False
    else:
        data_line = [tissue, hounsfield_range[0], hounsfield_range[1]]
        dataframe.loc[len(dataframe)] = data_line
        current = os.path.join(source, 'Current Tissue HU.txt')
        dataframe.to_csv(current, sep=';', index=False)
    return True


def drop_hounsfield_tissue(tissue, source=constant_source):
    # Removes a new tissue with hounsfield units to the currently used text file
    if type(tissue) is not str:
        return False
    dataframe = get_hounsfield_dataframe(source, 'Current Tissue HU.txt')
    original_tissues = get_original_tissues(source)
    if tissue in original_tissues:
        return False
    dataframe.drop(dataframe[dataframe['Tissue'] == tissue].index, inplace=True)
    current = os.path.join(source, 'Current Tissue HU.txt')
    dataframe.to_csv(current, sep=';', index=False)
    return True


def get_original_tissues(source=constant_source):
    # Returns the original tissues
    dataframe = get_hounsfield_dataframe(source, 'Original Tissue HU.txt')
    if dataframe is False:
        return False
    return np.array(dataframe['Tissue'])


def get_original_hu_ranges(source=constant_source):
    # Returns the original tissues and values as a dictionary
    return get_hounsfield_dictionary(source=source, file='Original Tissue HU.txt')


def hu_str2float(low, high):
    # For storage, we need the HU range in float
    if low == '-∞':
        low = -np.inf
    else:
        low = float(low)
    if high == '∞':
        high = np.inf
    else:
        high = float(high)
    return low, high


def hu_float2str(low, high):
    # For use in GUI, we need HU range in string
    if high == np.infty:
        high = infinity
    else:
        high = str(int(high))
    if low == -np.infty:
        low = '-%s' % infinity
    else:
        low = str(int(low))
    return low, high


infinity = '∞'
