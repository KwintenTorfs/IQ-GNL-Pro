import PySimpleGUI as sg

from Constants.design_GUI import accent, light_accent, text, various, FrameFont, window_size
from GUI.export import patient_parameters, slice_parameters, scanner_parameters, \
    study_parameters, gnl_pre_text
import GUI.export
from configuration import GUI_ICON
import GUI.technique
from Calculations.Global_Noise import standard_slice

settings_window_size = (int(0.45 * window_size[0]), int(0.4 * window_size[1]))

pre_and_suffix = {'AVG': 'AVG ',
                  'STD': 'STD ',
                  'HU': ' (HU)',
                  'LOW': ' - Low',
                  'HIGH': ' - High',
                  'STD SLICE': ' - per %s' % list(standard_slice.keys())[0],
                  'AREA': ' Area (cm²)',
                  'PERC': ' in body (%)',
                  'MASK': 'Mask Kernel (mm)',
                  'KERNEL': 'Mask Kernel (px)'}


def table_header(measure_per_scan: bool):
    """
        Create a header for a datatable of all parameters that are selected in the export parameters tab

        Parameters
        ----------
        measure_per_scan : bool
            Create table header for a table of scan averages or individual slices (False)
        Returns
        -------
        list: a list containing
            -header (list[str]) : a list of all parameters of data in the table
    """

    header = []
    if measure_per_scan:
        header.append('Calculation technique')
        for parameter in slice_parameters.keys():
            if slice_parameters[parameter]:
                header.append('%s%s' % (pre_and_suffix['AVG'], parameter))
                header.append('%s%s' % (pre_and_suffix['STD'], parameter))
        for parameter in GUI.export.tissue_parameters.keys():
            if GUI.export.tissue_parameters[parameter]:
                tissue = parameter.split(gnl_pre_text)[1]
                header.append('%s%s%s' % (pre_and_suffix['AVG'], parameter, pre_and_suffix['HU']))
                header.append('%s%s%s' % (pre_and_suffix['STD'], parameter, pre_and_suffix['HU']))
                header.append('%s%s%s' % (tissue, pre_and_suffix['LOW'], pre_and_suffix['HU']))
                header.append('%s%s%s' % (tissue, pre_and_suffix['HIGH'], pre_and_suffix['HU']))

    else:
        for parameter in slice_parameters.keys():
            if slice_parameters[parameter]:
                header.append(parameter)
        for parameter in GUI.export.tissue_parameters.keys():
            if GUI.export.tissue_parameters[parameter]:
                tissue = parameter.split(gnl_pre_text)[1]
                header.append('%s%s%s' % (parameter, pre_and_suffix['STD SLICE'], pre_and_suffix['HU']))
                header.append('%s%s' % (parameter, pre_and_suffix['HU']))
                header.append('%s%s%s' % (tissue, pre_and_suffix['LOW'], pre_and_suffix['HU']))
                header.append('%s%s%s' % (tissue, pre_and_suffix['HIGH'], pre_and_suffix['HU']))
                header.append('%s%s' % (tissue, pre_and_suffix['AREA']))
                header.append('%s%s' % (tissue, pre_and_suffix['PERC']))
    if True in GUI.export.tissue_parameters.values():
        header.append('%s' % pre_and_suffix['MASK'])
        header.append('%s' % pre_and_suffix['KERNEL'])
    for parameter in study_parameters.keys():
        if study_parameters[parameter]:
            header.append(parameter)
    for parameter in scanner_parameters.keys():
        if scanner_parameters[parameter]:
            header.append(parameter)
    for parameter in patient_parameters.keys():
        if patient_parameters[parameter]:
            header.append(parameter)
    return header


def create_table_header():
    measure_per_scan = GUI.technique.technique_parameters['PER SCAN']
    header = table_header(measure_per_scan)
    header_file = None
    if not measure_per_scan:
        header_file = table_header(not measure_per_scan)
    return header, header_file


def table_layout():
    headers, _ = create_table_header()
    widths = []
    for param in headers:
        widths.append(len(param) + 4)
    # noinspection PyTypeChecker
    layout = [[sg.Table(values=[], headings=headers, auto_size_columns=False, max_col_width=30,
                        display_row_numbers=True, justification='center', col_widths=widths,
                        vertical_scroll_only=False, background_color='white', header_text_color='white',
                        header_background_color=accent, text_color=text, header_font=FrameFont,
                        alternating_row_color=light_accent, sbar_trough_color=light_accent,
                        sbar_arrow_color=accent,
                        sbar_background_color=various,
                        expand_x=True, expand_y=True, key='TABLE',
                        metadata=headers, select_mode="browse")]]
    # right_click_menu=['&Right', right_click]
    return layout


def create_table_window():
    layout = table_layout()
    window_table = sg.Window(title='', layout=layout, size=settings_window_size, icon=GUI_ICON, finalize=True)
    window_table.bind('<Escape>', '+ESCAPE+')
    return window_table


def table_events(window, event, value):
    if '+MOUSE OVER+' in event:
        table_layout()
    return
