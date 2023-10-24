import PySimpleGUI as sg
import numpy as np

from Calculations.Global_Noise import samei_kernel
from Constants.design_GUI import text, various, accent, light_accent, TitleFont, SmallFont, TextFont, SpinSize, \
    window_size
from configuration import GUI_ICON

settings_window_size = (int(0.45 * window_size[0]), int(0.4 * window_size[1]))
default_nb_slices = 5
allowed_slices = '0123456789'
max_slices_digits = 4
default_kernel_size = samei_kernel
kernels = np.arange(1, 33, 2)

technique_parameters = {'GNL MID AX': False,
                        'GNL ALL SLICE': False,
                        'GNL 10 SLICE': True,
                        'GNL X SLICE': False,
                        'NB': default_nb_slices,
                        'PER SCAN': True,
                        'PER SLICE': False}


def technique_layout():
    column_left = [[sg.Text('')]]
    disabled_scan = technique_parameters['PER SLICE']
    column_right = [[sg.Checkbox('Mid axial slice', key='GNL MID AX', default=technique_parameters['GNL MID AX'],
                                 text_color=text, font=TextFont, expand_x=True, disabled=disabled_scan,
                                 enable_events=True)],
                    [sg.Checkbox('All slices (+avg)', key='GNL ALL SLICE', text_color=text, enable_events=True,
                                 font=TextFont, default=technique_parameters['GNL ALL SLICE'], disabled=disabled_scan)],
                    [sg.Checkbox('10 equidistant slices (+avg)', key='GNL 10 SLICE', text_color=text, font=TextFont,
                                 default=technique_parameters['GNL 10 SLICE'], disabled=disabled_scan,
                                 enable_events=True)],
                    [sg.Checkbox('', key='GNL X SLICE', text_color=text, font=TextFont, enable_events=True,
                                 default=technique_parameters['GNL X SLICE'], disabled=disabled_scan),
                     sg.Input(text_color=text, font=TextFont, background_color=various, key='NB', enable_events=True,
                              default_text=technique_parameters['NB'], size=(max_slices_digits, 1),
                              disabled=disabled_scan),
                     sg.Text('equidistant slices (+avg)', key='text', text_color=text, font=TextFont)]]

    layout = [[sg.Text('Measurement Methods', font=TitleFont, text_color=accent, justification='left')],
              [sg.Radio('Measure per scan', key='PER SCAN', group_id='MEASUREMENT', enable_events=True,
                        default=technique_parameters['PER SCAN']),
               sg.Radio('Measure per slice', key='PER SLICE', group_id='MEASUREMENT', enable_events=True,
                        default=technique_parameters['PER SLICE'])],
              [sg.Text('', font=SmallFont)],
              [sg.Column(column_left, size=(5, 1)),
               sg.Column(column_right, expand_x=True)],
              [sg.Text('', font=SmallFont)],
              [sg.Text('GNL calculation settings', font=TextFont, text_color=text)],
              [sg.Text('Kernel Size', font=TextFont, text_color=text),
               sg.Spin(initial_value=default_kernel_size, values=list(kernels), disabled=True, size=SpinSize),
               sg.Text('NEEDS TO BE RESEARCHED', font=TextFont, text_color=accent)]]

    return layout


def create_technique_window():
    layout = technique_layout()
    window_technique = sg.Window(title='', layout=layout, size=settings_window_size, icon=GUI_ICON, finalize=True)
    window_technique['NB'].widget.config(selectbackground=light_accent, selectforeground=text)
    window_technique.bind('<Escape>', '+ESCAPE+')
    return window_technique


def technique_events(window, event, value):
    if event in [sg.WIN_CLOSED, '+ESCAPE+']:
        return
    elif event == 'PER SLICE':
        window['GNL ALL SLICE'].update(True, disabled=True)
        window['GNL MID AX'].update(False, disabled=True)
        window['GNL 10 SLICE'].update(False, disabled=True)
        window['GNL X SLICE'].update(False, disabled=True)
        window['NB'].update(disabled=True)
        window['text'].update(text_color='grey')
    elif event == 'PER SCAN':
        window['GNL ALL SLICE'].update(technique_parameters['GNL ALL SLICE'], disabled=False)
        window['GNL MID AX'].update(technique_parameters['GNL MID AX'], disabled=False)
        window['GNL 10 SLICE'].update(technique_parameters['GNL 10 SLICE'], disabled=False)
        window['GNL X SLICE'].update(technique_parameters['GNL X SLICE'], disabled=False)
        window['NB'].update(technique_parameters['NB'], disabled=False)
        window['text'].update(text_color=text)
    elif event == 'NB':
        current_value = value[event]
        # If the last added value is not allowed, it is not added
        if len(current_value) and current_value[-1] not in allowed_slices:
            current_value = current_value[:-1]
        # If you copy a text and not all characters are allowed. The value is set to default
        if not all([character in allowed_slices for character in current_value]) and len(value):
            current_value = str(default_nb_slices)
        window[event].update(current_value)
        # If the nb slices is too long for the text space, it is shortened
        if len(value[event]) > max_slices_digits:
            window[event].update(value[event][:-1])

    for key in technique_parameters.keys():
        technique_parameters[key] = window[key].get()
