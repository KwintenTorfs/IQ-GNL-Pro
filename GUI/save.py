import PySimpleGUI as sg

from Constants.design_GUI import accent, TitleFont, text, TextFont, various, SpinSize, SmallFont, default_button

valid_save_files = ['.xlsx', '.csv']
default_file_text = 'Book1'
default_folder = r'..\Results'

exit_parameters = {'File Type': '.xlsx',
                   'FILE': default_file_text,
                   'FOLDER': default_folder}


def save_layout():
    layout = [[sg.Text('Save your current file?', font=TitleFont, text_color=accent, justification='left')],
              [sg.Text('File name', font=TextFont, text_color=text, justification='left')],

              [sg.Input(default_text=default_file_text, font=TextFont, text_color=text, justification='left',
                        key='FILE', expand_x=True, background_color=various, border_width=1),
               sg.Spin(values=valid_save_files, key='File Type', text_color=text, font=TextFont, size=SpinSize,
                       initial_value=exit_parameters['File Type'])],
              [sg.Text('', font=SmallFont, text_color=text, justification='left')],
              [sg.Text('Choose a location', font=TextFont, text_color=text, justification='left')],

              [sg.Input(key='FOLDER', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                        disabled=False, default_text=exit_parameters['FOLDER'],
                        justification='left', background_color=various, border_width=1),
               sg.FolderBrowse(tooltip='Choose a location', font=TextFont, button_color=default_button, size=(6, 1),
                               key='BROWSE')]
              ]
    return layout
