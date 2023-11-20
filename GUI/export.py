import PySimpleGUI as sg
import numpy as np

from Constants.design_GUI import text, various, accent, FrameFont, TitleFont, TextFont, default_button, \
    default_button_hover, accent_button, accent_button_hover, window_size, TextFontBold
from Support.Hounsfield_Units import get_hounsfield_dictionary, get_original_tissues
from configuration import GUI_ICON

scanner_parameters = {'Manufacturer': True,
                      'Model': True,
                      'Station': False,
                      'Channels': False,
                      'Software Version': False,
                      'Filter Type': False,
                      'Exposure Modulation Type': False,
                      'Acquisition Type': False,
                      }

patient_parameters = {'Patient Sex': False,
                      'Patient Age (y)': False,
                      'Body Part Examined': False,
                      'PACSID': False,
                      'Patient ID': False,
                      }

study_parameters = {'kVp': True,
                    'Kernel': True,
                    'FOV (mm)': False,
                    'Slice Thickness (mm)': False,
                    'Pixel Size (mm)': False,
                    'Pitch': False,
                    'Protocol': False,
                    'Procedure': False,
                    'Total Collimation (mm)': False,
                    'Single Collimation (mm)': False,
                    'Study Date': False,
                    'Exposure Time (ms)': False,
                    'Revolution Time (s)': False,
                    'Folder': False,
                    'Matrix Size': False,
                    'Study Comments': False,
                    'Study Description': False,
                    'Path': False
                    }

slice_parameters = {'Slice Number': False,
                    'mAs': True,
                    'mA': False,
                    'CTDI (mGy)': False,
                    'SSDE (mGy)': False,
                    'WED (cm)': False,
                    'Truncation Correction': False,
                    'Truncation Fraction': False,
                    'File': False,
                    'Position in Stack': False,
                    'Body Area (cm²)': False}

gnl_pre_text = 'GNL '


def get_available_tissues():
    current_tissues = get_hounsfield_dictionary()
    parameters = {}
    for k in current_tissues:
        gnl = '%s%s' % (gnl_pre_text, k)
        parameters[gnl] = False
    return parameters


tissue_parameters = get_available_tissues()
settings_window_size = (int(0.6 * window_size[0]), int(0.6 * window_size[1]))
word_size = (20, 1)
frame_border = 0
frame_color = various
box_color = 'white'
frame_text_color = text
nb_gnl_per_column = 15


def export_layout():
    global tissue_parameters
    current_db_tissues = get_available_tissues().keys()
    current_parameter_tissues = tissue_parameters.copy().keys()
    # Check for current tissues in DB and add new ones to tissue parameters
    for tissue in current_db_tissues:
        if tissue not in tissue_parameters.keys():
            tissue_parameters[tissue] = False

    # Check for current tissues in tissue parameters and remove the ones that aren't in DB
    for tissue in current_parameter_tissues:
        if tissue not in current_db_tissues:
            tissue_parameters.pop(tissue)

    longest_word_patients = max([len(i) for i in patient_parameters.keys()])
    size = (longest_word_patients + 2, 1)
    layout_patients = [[sg.Checkbox(text=parameter, default=patient_parameters[parameter], size=size,
                                    key=parameter, text_color=text, font=TextFont, background_color=frame_color,
                                    checkbox_color=box_color, enable_events=True)]
                       for parameter in sorted(patient_parameters.keys(), key=lambda v: (v.upper(), v[0].islower()))]
    # noinspection PyTypeChecker
    layout_patients.append([sg.Text('', expand_y=True, background_color=frame_color)])
    # noinspection PyTypeChecker
    layout_patients.append([sg.Push(background_color=frame_color),
                            sg.Button('Reject All', key='REJECT PATIENTS', font=TextFont, button_color=default_button,
                                      size=(10, 1)),
                            sg.Button('Select all', key='ALL PATIENTS', font=TextFont, button_color=default_button,
                                      size=(10, 1))
                            ])
    longest_word_scanner = max([len(i) for i in scanner_parameters.keys()])
    size = (longest_word_scanner + 2, 1)
    layout_scanner = [[sg.Checkbox(text=parameter, default=scanner_parameters[parameter], size=size, key=parameter,
                                   text_color=text, font=TextFont, background_color=frame_color,
                                   checkbox_color=box_color, enable_events=True)]
                      for parameter in sorted(scanner_parameters.keys(), key=lambda v: (v.upper(), v[0].islower()))]
    # noinspection PyTypeChecker
    layout_scanner.append([sg.Text('', expand_y=True, background_color=frame_color)])
    # noinspection PyTypeChecker
    layout_scanner.append([sg.Push(background_color=frame_color),
                           sg.Button('Reject All', key='REJECT SCANNER', font=TextFont, button_color=default_button,
                                     size=(10, 1)),
                           sg.Button('Select All', key='ALL SCANNER', font=TextFont, button_color=default_button,
                                     size=(10, 1))
                           ])

    longest_word_study = max([len(i) for i in study_parameters.keys()])
    size = (longest_word_study + 2, 1)
    layout_study = [[sg.Checkbox(text=parameter, default=study_parameters[parameter], size=size, key=parameter,
                                 text_color=text, font=TextFont, background_color=frame_color,
                                 checkbox_color=box_color, enable_events=True)]
                    for parameter in sorted(study_parameters.keys(), key=lambda v: (v.upper(), v[0].islower()))]
    # noinspection PyTypeChecker
    layout_study.append([sg.Text('', expand_y=True, background_color=frame_color)])
    # noinspection PyTypeChecker
    layout_study.append([sg.Push(background_color=frame_color),
                         sg.Button('Reject All', key='REJECT STUDY', font=TextFont, button_color=default_button,
                                   size=(10, 1)),
                         sg.Button('Select All', key='ALL STUDY', font=TextFont, button_color=default_button,
                                   size=(10, 1))
                         ])

    longest_word_slice = max([len(i) for i in slice_parameters.keys()])
    size = (longest_word_slice + 2, 1)
    layout_slice = [[sg.Checkbox(text=parameter, default=slice_parameters[parameter], size=size, key=parameter,
                                 text_color=text, font=TextFont, background_color=frame_color,
                                 checkbox_color=box_color, enable_events=True)]
                    for parameter in sorted(slice_parameters.keys(), key=lambda v: (v.upper(), v[0].islower()))]
    # noinspection PyTypeChecker
    layout_slice.append([sg.Text('', expand_y=True, background_color=frame_color)])
    # noinspection PyTypeChecker
    layout_slice.append([sg.Push(background_color=frame_color),
                         sg.Button('Reject All', key='REJECT SLICE', font=TextFont, button_color=default_button,
                                   size=(10, 1)),
                         sg.Button('Select All', key='ALL SLICE', font=TextFont, button_color=default_button,
                                   size=(10, 1))
                         ])

    left_column = [[sg.Frame('Scanner Parameters', layout=layout_scanner, font=FrameFont, title_color=frame_text_color,
                             expand_y=True, expand_x=True, border_width=frame_border, background_color=frame_color)],
                   [sg.Frame('Patient Parameters', layout=layout_patients, font=FrameFont, title_color=frame_text_color,
                             expand_y=True, expand_x=True, border_width=frame_border, background_color=frame_color)]]

    middle_column = [[sg.Frame('Study Parameters', layout=layout_study, font=FrameFont, title_color=frame_text_color,
                               expand_y=True, expand_x=True, border_width=frame_border, background_color=frame_color)]]

    right_column = [[sg.Frame('Slice Parameters', layout=layout_slice, border_width=frame_border,
                              background_color=frame_color,
                              expand_y=True, expand_x=True, font=FrameFont, title_color=frame_text_color)]]

    original_tissues = get_original_tissues()

    nb_columns = np.ceil(len(tissue_parameters) / nb_gnl_per_column).astype(int)
    longest_word_gnl = max([len(i) for i in tissue_parameters.keys()])
    size = (longest_word_gnl + 2, 1)
    layout_columns = [[] for _ in range(nb_columns)]
    for i, tissue in enumerate(tissue_parameters.keys()):
        column = np.floor(i / nb_gnl_per_column).astype(int)
        font = TextFont
        if tissue.split(gnl_pre_text)[1] in original_tissues:
            font = TextFontBold
        layout_columns[column].append([sg.Checkbox(text=tissue, default=tissue_parameters[tissue], size=size,
                                                   text_color=text, font=font, background_color=frame_color, key=tissue,
                                                   checkbox_color=box_color, enable_events=True)])
    layout_gnl = [[sg.Column(column_layout, background_color=frame_color, expand_x=True, expand_y=True)
                   for column_layout in layout_columns],
                  [sg.Text('', expand_y=True, background_color=frame_color)],
                  [sg.Push(background_color=frame_color),
                   sg.Button('Reject All', key='REJECT GNL', font=TextFont, button_color=default_button, size=(10, 1)),
                   sg.Button('Select All', key='ALL GNL', font=TextFont, button_color=default_button, size=(10, 1))]]

    gnl_column = [[sg.Frame('GNL Parameters', layout=layout_gnl, border_width=frame_border, font=FrameFont,
                            background_color=frame_color, expand_y=True, expand_x=True, title_color=frame_text_color)]]

    layout = [[sg.Text('Select export parameters', font=TitleFont, text_color=accent, justification='left'),
               sg.Push(),
               sg.Button('Reject All', key='REJECT SETTINGS', font=TextFont, button_color=default_button, size=(11, 1)),
               sg.Button('Select All', key='ALL SETTINGS', font=TextFont, button_color=accent_button, size=(11, 1))
               ],
              [sg.Column(left_column, expand_x=True, expand_y=True),
               sg.Column(middle_column, expand_x=True, expand_y=True),
               sg.Column(right_column, expand_x=True, expand_y=True),
               sg.Column(gnl_column, expand_x=True, expand_y=True)],
              ]
    return layout


def set_all_parameters(window, parameters, end_value):
    for parameter in parameters.keys():
        window[parameter].update(end_value)
        parameters[parameter] = end_value


def export_events(window, event, value):
    global tissue_parameters
    if event in [sg.WIN_CLOSED, '+ESCAPE+']:
        return
    elif event == 'ALL SLICE+MOUSE OVER+':
        window['ALL SLICE'].update(button_color=default_button_hover)
    elif event == 'ALL SLICE+MOUSE AWAY+':
        window['ALL SLICE'].update(button_color=default_button)
    elif event == 'ALL PATIENTS+MOUSE OVER+':
        window['ALL PATIENTS'].update(button_color=default_button_hover)
    elif event == 'ALL PATIENTS+MOUSE AWAY+':
        window['ALL PATIENTS'].update(button_color=default_button)
    elif event == 'ALL SCANNER+MOUSE OVER+':
        window['ALL SCANNER'].update(button_color=default_button_hover)
    elif event == 'ALL SCANNER+MOUSE AWAY+':
        window['ALL SCANNER'].update(button_color=default_button)
    elif event == 'ALL STUDY+MOUSE OVER+':
        window['ALL STUDY'].update(button_color=default_button_hover)
    elif event == 'ALL STUDY+MOUSE AWAY+':
        window['ALL STUDY'].update(button_color=default_button)
    elif event == 'ALL GNL+MOUSE OVER+':
        window['ALL GNL'].update(button_color=default_button_hover)
    elif event == 'ALL GNL+MOUSE AWAY+':
        window['ALL GNL'].update(button_color=default_button)
    elif event == 'ALL SETTINGS+MOUSE OVER+':
        window['ALL SETTINGS'].update(button_color=accent_button_hover)
    elif event == 'ALL SETTINGS+MOUSE AWAY+':
        window['ALL SETTINGS'].update(button_color=accent_button)

    elif event == 'REJECT SLICE+MOUSE OVER+':
        window['REJECT SLICE'].update(button_color=default_button_hover)
    elif event == 'REJECT SLICE+MOUSE AWAY+':
        window['REJECT SLICE'].update(button_color=default_button)
    elif event == 'REJECT PATIENTS+MOUSE OVER+':
        window['REJECT PATIENTS'].update(button_color=default_button_hover)
    elif event == 'REJECT PATIENTS+MOUSE AWAY+':
        window['REJECT PATIENTS'].update(button_color=default_button)
    elif event == 'REJECT SCANNER+MOUSE OVER+':
        window['REJECT SCANNER'].update(button_color=default_button_hover)
    elif event == 'REJECT SCANNER+MOUSE AWAY+':
        window['REJECT SCANNER'].update(button_color=default_button)
    elif event == 'REJECT STUDY+MOUSE OVER+':
        window['REJECT STUDY'].update(button_color=default_button_hover)
    elif event == 'REJECT STUDY+MOUSE AWAY+':
        window['REJECT STUDY'].update(button_color=default_button)
    elif event == 'REJECT GNL+MOUSE OVER+':
        window['REJECT GNL'].update(button_color=default_button_hover)
    elif event == 'REJECT GNL+MOUSE AWAY+':
        window['REJECT GNL'].update(button_color=default_button)
    elif event == 'REJECT SETTINGS+MOUSE OVER+':
        window['REJECT SETTINGS'].update(button_color=default_button_hover)
    elif event == 'REJECT SETTINGS+MOUSE AWAY+':
        window['REJECT SETTINGS'].update(button_color=default_button)

    elif event in slice_parameters.keys():
        slice_parameters[event] = value[event]
    elif event in scanner_parameters.keys():
        scanner_parameters[event] = value[event]
    elif event in study_parameters.keys():
        study_parameters[event] = value[event]
    elif event in patient_parameters.keys():
        patient_parameters[event] = value[event]
    elif event in tissue_parameters.keys():
        tissue_parameters[event] = value[event]
    elif event == 'ALL SLICE':
        set_all_parameters(window, slice_parameters, True)
    elif event == 'ALL PATIENTS':
        set_all_parameters(window, patient_parameters, True)
    elif event == 'ALL STUDY':
        set_all_parameters(window, study_parameters, True)
    elif event == 'ALL SCANNER':
        set_all_parameters(window, scanner_parameters, True)
    elif event == 'ALL GNL':
        set_all_parameters(window, tissue_parameters, True)
    elif event == 'ALL SETTINGS':
        set_all_parameters(window, patient_parameters, True)
        set_all_parameters(window, study_parameters, True)
        set_all_parameters(window, scanner_parameters, True)
        set_all_parameters(window, slice_parameters, True)
        set_all_parameters(window, tissue_parameters, True)
    elif event == 'REJECT SLICE':
        set_all_parameters(window, slice_parameters, False)
    elif event == 'REJECT PATIENTS':
        set_all_parameters(window, patient_parameters, False)
    elif event == 'REJECT STUDY':
        set_all_parameters(window, study_parameters, False)
    elif event == 'REJECT SCANNER':
        set_all_parameters(window, scanner_parameters, False)
    elif event == 'REJECT GNL':
        set_all_parameters(window, tissue_parameters, False)
    elif event == 'REJECT SETTINGS':
        set_all_parameters(window, patient_parameters, False)
        set_all_parameters(window, study_parameters, False)
        set_all_parameters(window, scanner_parameters, False)
        set_all_parameters(window, slice_parameters, False)
        set_all_parameters(window, tissue_parameters, False)
    return


def create_export_window():
    layout = export_layout()
    window_export = sg.Window(title='', layout=layout, size=settings_window_size, icon=GUI_ICON, finalize=True)
    window_export['ALL SLICE'].bind('<Enter>', '+MOUSE OVER+')
    window_export['ALL SLICE'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['ALL PATIENTS'].bind('<Enter>', '+MOUSE OVER+')
    window_export['ALL PATIENTS'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['ALL STUDY'].bind('<Enter>', '+MOUSE OVER+')
    window_export['ALL STUDY'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['ALL SCANNER'].bind('<Enter>', '+MOUSE OVER+')
    window_export['ALL SCANNER'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['ALL SETTINGS'].bind('<Enter>', '+MOUSE OVER+')
    window_export['ALL SETTINGS'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['ALL GNL'].bind('<Enter>', '+MOUSE OVER+')
    window_export['ALL GNL'].bind('<Leave>', '+MOUSE AWAY+')

    window_export['REJECT SLICE'].bind('<Enter>', '+MOUSE OVER+')
    window_export['REJECT SLICE'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['REJECT PATIENTS'].bind('<Enter>', '+MOUSE OVER+')
    window_export['REJECT PATIENTS'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['REJECT STUDY'].bind('<Enter>', '+MOUSE OVER+')
    window_export['REJECT STUDY'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['REJECT SCANNER'].bind('<Enter>', '+MOUSE OVER+')
    window_export['REJECT SCANNER'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['REJECT SETTINGS'].bind('<Enter>', '+MOUSE OVER+')
    window_export['REJECT SETTINGS'].bind('<Leave>', '+MOUSE AWAY+')
    window_export['REJECT GNL'].bind('<Enter>', '+MOUSE OVER+')
    window_export['REJECT GNL'].bind('<Leave>', '+MOUSE AWAY+')
    window_export.bind('<Escape>', '+ESCAPE+')
    return window_export
