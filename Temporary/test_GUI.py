import os.path

import numpy as np
import pandas as pd

import GUI.export
from GUI.calculate import images_for_measurement_per_slice
from GUI.calculation import process_list_of_image_slices, necessary_image_class_calculations, process_list_of_folders
from GUI.calculation_folders_to_files import get_calculable_slices
from GUI.save import get_save_locations
from GUI.table import table_header, pre_and_suffix
from GUI.technique import technique_parameters
from Support.Hounsfield_Units import get_hounsfield_dictionary

SCAN = r'D:\Database - ERPW Project\Databases\Lungman\Lungman - Covid\KULQCCT16ERPWDIK_Unknown_20230928_112112679'
SCAN2 = r'D:\Database - ERPW Project\Databases\Patient\Patients - Conventional\Patients - Conventional\DE_BIE_ERIK_CHRISTIANE_20230921_135327310'


# for p in GUI.export.patient_parameters.keys():
#     GUI.export.patient_parameters[p] = True
# for p in GUI.export.slice_parameters.keys():
#     GUI.export.slice_parameters[p] = True
# for p in GUI.export.study_parameters.keys():
#     GUI.export.study_parameters[p] = True
# for p in GUI.export.scanner_parameters.keys():
#     GUI.export.scanner_parameters[p] = True
GUI.export.tissue_parameters['GNL Soft Tissue'] = True
technique_parameters['GNL MID AX'] = True
technique_parameters['GNL 10 SLICE'] = False
technique_parameters['GNL X SLICE'] = True
technique_parameters['GNL ALL SLICE'] = False
technique_parameters['NB'] = 5

type_of_input = 'SCAN'
source_paths = [SCAN, SCAN2]
save_location_files, save_location_scans = get_save_locations()
slices_header = table_header(False)
header_scan = table_header(True)
calculate_gnl, image_param = necessary_image_class_calculations(slices_header)
slice_dataframe = pd.DataFrame(data=None, columns=slices_header)
hounsfield_ranges = get_hounsfield_dictionary()
scan_dataframe = pd.DataFrame(data=None, columns=header_scan)
process_list_of_folders(source_paths, slice_dataframe, scan_dataframe, hounsfield_ranges, save_location_files, save_location_scans, image_param, calculate_gnl, window=None)
# for folder in source_paths:
#     slices, measurements = get_calculable_slices(folder)
#     data = process_list_of_image_slices(image_slices=slices,
#                                         slice_dataframe=slice_dataframe,
#                                         hounsfield_ranges=hounsfield_ranges,
#                                         save_location=save_location_files,
#                                         calculate_image_parameters=image_param,
#                                         calculate_gnl=calculate_gnl,
#                                         window=None)
#
#     for method in measurements.keys():
#         nb_slices = len(measurements[method])
#         if nb_slices < 1:
#             continue
#         scan_info = dict(zip(header_scan, [None] * len(header_scan)))
#         for parameter in scan_info.keys():
#             if pre_and_suffix['AVG'] in parameter:
#                 original_parameter = parameter.split(pre_and_suffix['AVG'])[1]
#                 position_in_data = slices_header.index(original_parameter)
#                 parameter_array = np.take(np.array(data[original_parameter]), np.array(measurements[method]))
#                 scan_info[pre_and_suffix['AVG'] + original_parameter] = np.nanmean(parameter_array)
#                 scan_info[pre_and_suffix['STD'] + original_parameter] = np.nanstd(parameter_array)
#             elif pre_and_suffix['STD'] in parameter:
#                 pass
#             elif parameter == 'Calculation Method':
#                 scan_info[parameter] = method
#             elif parameter == 'NB Slices':
#                 scan_info[parameter] = nb_slices
#             elif parameter == 'Path':
#                 scan_info[parameter] = os.path.dirname(data[parameter][0])
#             else:
#                 scan_info[parameter] = data[parameter][0]
#
#         scan_dataframe.loc[len(scan_dataframe)] = scan_info.values()
#         scan_dataframe.to_excel(save_location_scans)
