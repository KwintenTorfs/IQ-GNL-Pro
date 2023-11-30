import os.path

import PySimpleGUI as sg
import pandas as pd

from Constants.Images.images_b64 import MAP, image_rescale, SAVEASWHITE
from Constants.design_GUI import accent, TitleFont, text, TextFont, default_button, DefaultTextFont, default_text, \
    default_button_hover, light_accent, background, LargeFont, darker_grey, MenuFont
from configuration import RESULTS_FOLDER


def create_path(folder, file, file_type):
    return os.path.join(folder, file) + file_type


valid_save_files = {'Excel Workbook (*.xlsx)': '.xlsx',
                    'CSV (comma delimited) (*.csv)': '.csv',
                    'Text (Tab Delimited) (*.txt)': '.txt'}

df = pd.DataFrame(data=None)


def save_excel(dataframe: pd.DataFrame, save_location: str):
    dataframe.to_excel(save_location, index_label='Index')


def save_csv(dataframe: pd.DataFrame, save_location: str):
    dataframe.to_csv(save_location, sep=',', index_label='Index')


def save_txt(dataframe: pd.DataFrame, save_location: str):
    dataframe.to_csv(save_location, sep='\t', index_label='Index')


operations_save = {'Excel Workbook (*.xlsx)': save_excel,
                   'CSV (comma delimited) (*.csv)': save_csv,
                   'Text (Tab Delimited) (*.txt)': save_txt}

default_file = 'Book1'
default_file_text = 'Enter file name here'
default_folder = RESULTS_FOLDER
default_save_type = list(valid_save_files.keys())[0]
default_path = create_path(default_folder, default_file, default_save_type)


save_parameters = {'FILE TYPE': default_save_type,
                   'FILE': default_file_text,
                   'DEFAULT FILE': True,
                   'FOLDER': default_folder}

illegal_excel_characters = '*:?<>|"'
darker_frame = darker_grey


def get_save_locations():
    """
        Get the complete name that should be given to the data files that are saved
    :return:
        tuple: a tuple containing
        - save_location_files (str): A location with the measured data per slice
        - save_location_scans (str): A location with the measured data per scan
    """
    if save_parameters['DEFAULT FILE']:
        save_filename = default_file
    else:
        save_filename = save_parameters['FILE']
    save_directory = save_parameters['FOLDER']
    save_filetype = valid_save_files[save_parameters['FILE TYPE']]
    save_location_files = os.path.join(save_directory, save_filename) + ' (per slice)' + save_filetype
    save_location_scans = os.path.join(save_directory, save_filename) + save_filetype
    return save_location_files, save_location_scans


def save_layout():
    global save_parameters
    layout = [[sg.Text('Save As', font=TitleFont, text_color=accent, justification='left')],
              [sg.Column([[sg.Frame('', layout=[[sg.Button('', image_data=image_rescale(MAP, 23, 16),
                                                           image_size=(23, 16), button_color='white', border_width=0,
                                                           key='FOLDER1', button_type=sg.BUTTON_TYPE_BROWSE_FOLDER,
                                                           enable_events=True, target='FOLDER_IN'),
                                                 sg.Input(key='FOLDER_IN', visible=False, enable_events=True),
                                                 sg.Button(os.path.basename(default_folder), button_color='white',
                                                           font=LargeFont, border_width=0,
                                                           button_type=sg.BUTTON_TYPE_BROWSE_FOLDER, key='FOLDER2',
                                                           enable_events=True, target='FOLDER_IN')]],
                                    background_color='white', border_width=0, key='FRAME', expand_x=True)],
                          [sg.Input(default_text=save_parameters['FILE'], key='FILE', expand_x=True,
                                    font=DefaultTextFont, text_color=default_text, enable_events=True)],
                          [sg.Combo(list(valid_save_files.keys()), expand_x=True, text_color=text, font=TextFont,
                                    default_value=save_parameters['FILE TYPE'], key='FILE TYPE', enable_events=True,
                                    background_color='white')]]),
               # sg.Column([[sg.Text('', expand_y=True)],
               #            [sg.Frame('', layout=[[sg.Text(background_color='white', key='left', expand_x=True),
               #                                   sg.Button('', image_data=image_rescale(SAVEASWHITE, 17, 16),
               #                                             image_size=(20, 16), button_color='white', border_width=0,
               #                                             key='SAVE_ICON', size=(20, 1),
               #                                             enable_events=True),
               #                                   sg.Button('Save', button_color=(text, 'white'), font=MenuFont,
               #                                             border_width=0, key='SAVE', enable_events=True),
               #                                   sg.Text(background_color='white', key='right', expand_x=True)]],
               #                      background_color='white', border_width=0, key='FRAME2', expand_x=True,
               #                      size=(100, 30))]])
               ]]
    return layout


def save_events(window, event, _):
    global save_parameters
    if event != 'FILE':
        current_file = window['FILE'].get()
        if current_file == '':
            window['FILE'].update(default_file_text, text_color=default_text)
            window['FILE'].widget.configure(font=DefaultTextFont)
            save_parameters['FILE'] = default_file_text
            save_parameters['DEFAULT FILE'] = True
    if event in [sg.WIN_CLOSED, '+ESCAPE+']:
        return
    elif event in ['FOLDER1+MOUSE OVER+', 'FOLDER2+MOUSE OVER+', 'FRAME+MOUSE OVER+']:
        window['FOLDER1'].update(button_color=darker_frame)
        window['FOLDER2'].update(button_color=darker_frame)
        window['FRAME'].Widget.config(background=darker_frame)
        window['FOLDER1'].ParentRowFrame.config(background=darker_frame)
        window['FOLDER2'].ParentRowFrame.config(background=darker_frame)
    elif event in ['FOLDER1+MOUSE AWAY+', 'FOLDER2+MOUSE AWAY+', 'FRAME+MOUSE AWAY+']:
        window['FOLDER1'].update(button_color='white')
        window['FOLDER2'].update(button_color='white')
        window['FRAME'].Widget.config(background='white')
        window['FOLDER1'].ParentRowFrame.config(background='white')
        window['FOLDER2'].ParentRowFrame.config(background='white')
    elif event in ['SAVE+MOUSE OVER+', 'SAVE_ICON+MOUSE OVER+', 'FRAME2+MOUSE OVER+']:
        window['SAVE'].update(button_color=light_accent)
        window['SAVE_ICON'].update(button_color=light_accent)
        window['FRAME2'].Widget.config(background=light_accent)
        window['left'].Widget.config(background=light_accent)
        window['right'].Widget.config(background=light_accent)
        window['FRAME2'].Widget.configure(highlightbackground=accent, highlightcolor=accent, highlightthickness=1)
        window['SAVE'].ParentRowFrame.config(background=light_accent)
        window['SAVE_ICON'].ParentRowFrame.config(background=light_accent)
    elif event in ['SAVE+MOUSE AWAY+', 'SAVE_ICON+MOUSE AWAY+', 'FRAME2+MOUSE AWAY+']:
        window['SAVE'].update(button_color='white')
        window['SAVE_ICON'].update(button_color='white')
        window['FRAME2'].Widget.config(background='white')
        window['left'].Widget.config(background='white')
        window['right'].Widget.config(background='white')
        window['FRAME2'].Widget.configure(highlightbackground=text, highlightcolor=text, highlightthickness=1)
        window['SAVE'].ParentRowFrame.config(background='white')
        window['SAVE_ICON'].ParentRowFrame.config(background='white')
    # elif event == 'SAVE+MOUSE OVER+':
    #     window['SAVE'].update(button_color=default_button_hover)
    # elif event == 'SAVE+MOUSE AWAY+':
    #     window['SAVE'].update(button_color=default_button)
    elif event == 'FILE':
        current_file = window['FILE'].get()
        if default_file_text in current_file:
            current_file = current_file.split(default_file_text)[1]
        elif current_file == default_file_text[:-1]:
            current_file = ''
        window['FILE'].update(current_file, text_color=text)
        window['FILE'].widget.configure(font=TextFont)
        save_parameters['FILE'] = current_file
        save_parameters['DEFAULT FILE'] = False
    elif event == 'FOLDER_IN':
        folder = window[event].get()
        save_parameters['FOLDER'] = folder
        window['FOLDER2'].update(os.path.basename(folder))
        window['FOLDER1'].update(button_color='white')
        window['FOLDER2'].update(button_color='white')
        window['FRAME'].Widget.config(background='white')
        window['FOLDER1'].ParentRowFrame.config(background='white')
        window['FOLDER2'].ParentRowFrame.config(background='white')

    elif event == 'FILE TYPE':
        save_parameters['FILE TYPE'] = window[event].get()

    elif event in ['SAVE', 'SAVE_ICON']:
        filename = save_parameters['FILE']
        folder_name = save_parameters['FOLDER']
        extension = valid_save_files[save_parameters['FILE TYPE']]
        path = create_path(folder_name, filename, extension)
        save_parameters['PATH'] = path
    return


def save_bindings(window):
    window.bind('<Escape>', '+ESCAPE+')
    window['FOLDER1'].bind('<Enter>', '+MOUSE OVER+')
    window['FOLDER1'].bind('<Leave>', '+MOUSE AWAY+')
    window['FRAME'].bind('<Enter>', '+MOUSE OVER+')
    window['FRAME'].bind('<Leave>', '+MOUSE AWAY+')
    window['FOLDER2'].bind('<Enter>', '+MOUSE OVER+')
    window['FOLDER2'].bind('<Leave>', '+MOUSE AWAY+')
    # window['SAVE'].bind('<Enter>', '+MOUSE OVER+')
    # window['SAVE'].bind('<Leave>', '+MOUSE AWAY+')
    # window['FRAME2'].bind('<Enter>', '+MOUSE OVER+')
    # window['FRAME2'].bind('<Leave>', '+MOUSE AWAY+')
    # window['SAVE_ICON'].bind('<Enter>', '+MOUSE OVER+')
    # window['SAVE_ICON'].bind('<Leave>', '+MOUSE AWAY+')
    # window['FRAME2'].Widget.configure(highlightbackground=text, highlightcolor=text, highlightthickness=1)

    window['FILE'].widget.config(selectbackground=light_accent, selectforeground=text)
    widget = window['FILE TYPE'].Widget
    widget.tk.eval('[ttk::combobox::PopdownWindow %s].f.l configure -foreground %s -background %s -'
                   'selectforeground %s -selectbackground %s' % (widget, text, background, text, light_accent))
