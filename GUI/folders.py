import PySimpleGUI as sg

from Constants.design_GUI import TitleFont, accent, window_size, TextFont, text, various, default_button, light_accent, \
    default_button_hover, SmallFont
from GUI.technique import technique_parameters
from configuration import GUI_ICON

measure_per_scan = technique_parameters['PER SCAN']
settings_window_size = (int(0.3 * window_size[0]), int(0.3 * window_size[1]))


def folders_layout():
    layout = [[sg.Text('Select Data', font=TitleFont, text_color=accent, justification='left')],
              [sg.Text('', font=SmallFont, text_color=text, justification='left')],
              [sg.Text('Source folder', font=TextFont, text_color=text, justification='left')],
              [sg.Input(key='SOURCE', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                        disabled=False, justification='left', background_color=various, border_width=1),
               sg.FolderBrowse(tooltip='Choose source folder', font=TextFont, button_color=default_button, size=(6, 1),
                               key='FIND SOURCE')]
              ]
    return layout


def create_folders_window():
    layout = folders_layout()
    window_folders = sg.Window(title='', layout=layout, size=settings_window_size, icon=GUI_ICON, finalize=True)
    window_folders['SOURCE'].widget.config(selectbackground=light_accent, selectforeground=text)
    window_folders['FIND SOURCE'].bind('<Enter>', '+MOUSE OVER+')
    window_folders['FIND SOURCE'].bind('<Leave>', '+MOUSE AWAY+')
    window_folders.bind('<Escape>', '+ESCAPE+')
    return window_folders


def folders_events(window, event, value):
    if event in [sg.WIN_CLOSED, '+ESCAPE+']:
        return

    elif event == 'FIND SOURCE+MOUSE OVER+':
        window['FIND SOURCE'].update(button_color=default_button_hover)
    elif event == 'FIND SOURCE+MOUSE AWAY+':
        window['FIND SOURCE'].update(button_color=default_button)
    return
