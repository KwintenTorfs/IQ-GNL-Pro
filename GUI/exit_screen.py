import FreeSimpleGUI as sg

from Constants.design_GUI import text, various, accent, light_accent, TitleFont, SmallFont, \
    ButtonFont, TextFont, SpinSize, my_width, my_height, default_button, default_button_hover, accent_button, \
    accent_button_hover
from configuration import GUI_ICON

valid_save_files = ['.xlsx', '.csv']
default_file_text = 'Book1'
default_folder = r'..\Results'

exit_parameters = {'File Type': '.xlsx',
                   '-IN-': default_file_text,
                   '-FOLDER-': default_folder}


def exit_layout():
    global exit_parameters
    layout = [[sg.Text('Save your current file?', font=TitleFont, text_color=accent, justification='left')],

              [sg.Text('', font=SmallFont, text_color=text, justification='left')],
              [sg.Text('File name', font=TextFont, text_color=text, justification='left')],

              [sg.Input(default_text=default_file_text, font=TextFont, text_color=text, justification='left',
                        key='-IN-', expand_x=True, background_color=various, border_width=1),
               sg.Spin(values=valid_save_files, key='File Type', text_color=text, font=TextFont, size=SpinSize,
                       initial_value=exit_parameters['File Type'])],

              [sg.Text('', font=SmallFont, text_color=text, justification='left')],
              [sg.Text('Choose a location', font=TextFont, text_color=text, justification='left')],

              [sg.Input(key='-FOLDER-', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                        disabled=False, default_text=exit_parameters['-FOLDER-'],
                        justification='left', background_color=various, border_width=1),
               sg.FolderBrowse(tooltip='Choose a location', font=TextFont, button_color=default_button, size=(6, 1),
                               key='BROWSE')],

              [sg.Text('', font=SmallFont, text_color=text, justification='left')],

              [sg.Push(),
               sg.Button(key='SAVE', button_text='Save', button_color=accent_button,
                         size=(4, 1), font=ButtonFont, border_width=1),
               sg.Button(key='EXIT', button_text="Don't save", button_color=default_button,
                         size=(10, 1), font=ButtonFont, border_width=1),
               sg.Button(key='CANCEL', button_text="Cancel", button_color=default_button,
                         size=(6, 1), font=ButtonFont, border_width=1)]]
    return layout


def create_exit_window():
    layout = exit_layout()
    window_exit = sg.Window('', layout, finalize=True, keep_on_top=True, icon=GUI_ICON, return_keyboard_events=True,
                            disable_minimize=True, size=(int(0.3 * my_width), int(0.28 * my_height)))
    window_exit['SAVE'].bind('<Enter>', '+MOUSE OVER+')
    window_exit['SAVE'].bind('<Leave>', '+MOUSE AWAY+')
    window_exit['CANCEL'].bind('<Enter>', '+MOUSE OVER+')
    window_exit['CANCEL'].bind('<Leave>', '+MOUSE AWAY+')
    window_exit['BROWSE'].bind('<Enter>', '+MOUSE OVER+')
    window_exit['BROWSE'].bind('<Leave>', '+MOUSE AWAY+')
    window_exit['EXIT'].bind('<Enter>', '+MOUSE OVER+')
    window_exit['EXIT'].bind('<Leave>', '+MOUSE AWAY+')
    window_exit['-IN-'].bind("<Return>", "_Enter")
    window_exit['-IN-'].widget.config(selectbackground=light_accent, selectforeground=text)
    window_exit['-FOLDER-'].widget.config(selectbackground=light_accent, selectforeground=text)
    window_exit['File Type'].widget.config(selectbackground=light_accent, selectforeground=text)
    return window_exit


def exit_events(window, event, value):
    close_program = False
    save = False
    if event == 'SAVE+MOUSE OVER+':
        window['SAVE'].update(button_color=accent_button_hover)
    elif event == 'SAVE+MOUSE AWAY+':
        window['SAVE'].update(button_color=accent_button)
    elif event == 'EXIT+MOUSE OVER+':
        window['EXIT'].update(button_color=default_button_hover)
    elif event == 'EXIT+MOUSE AWAY+':
        window['EXIT'].update(button_color=default_button)
    elif event == 'CANCEL+MOUSE OVER+':
        window['CANCEL'].update(button_color=default_button_hover)
    elif event == 'CANCEL+MOUSE AWAY+':
        window['CANCEL'].update(button_color=default_button)
    elif event == 'BROWSE+MOUSE OVER+':
        window['BROWSE'].update(button_color=default_button_hover)
    elif event == 'BROWSE+MOUSE AWAY+':
        window['BROWSE'].update(button_color=default_button)
    elif event == 'EXIT':
        close_program = True
        window.write_event_value(sg.WIN_CLOSED, None)
    elif event == 'SAVE':
        close_program = True
        window.write_event_value(sg.WIN_CLOSED, None)
        save = True
    elif event == 'CANCEL':
        close_program = False
        window.write_event_value(sg.WIN_CLOSED, None)
    elif event == '-IN-_Enter':
        window['-IN-'].update(text_color=text)
    if value['-IN-'] != default_file_text:
        window['-IN-'].update(text_color=text)
    for key in exit_parameters.keys():
        exit_parameters[key] = window[key].get()
    return close_program, save


def sure_you_want_to_close():
    layout = [[sg.Text('Save your current file?', font=TitleFont, text_color=accent, justification='left')],

              [sg.Text('', font=SmallFont, text_color=text, justification='left')],
              [sg.Text('File name', font=TextFont, text_color=text, justification='left')],

              [sg.Input(default_text=default_file_text, font=TextFont, text_color=text, justification='left',
                        key='-IN-', expand_x=True, background_color=various, border_width=1),
               sg.Spin(values=valid_save_files, key='File Type', text_color=text, font=TextFont, size=SpinSize,
                       initial_value=exit_parameters['File Type'])],

              [sg.Text('', font=SmallFont, text_color=text, justification='left')],
              [sg.Text('Choose a location', font=TextFont, text_color=text, justification='left')],

              [sg.Input(key='-FOLDER-', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                        disabled=False, default_text=exit_parameters['-FOLDER-'],
                        justification='left', background_color=various, border_width=1),
               sg.FolderBrowse(tooltip='Choose a location', font=TextFont, button_color=default_button, size=(6, 1),
                               key='BROWSE')],

              [sg.Text('', font=SmallFont, text_color=text, justification='left')],

              [sg.Push(),
               sg.Button(key='SAVE', button_text='Save', button_color=accent_button,
                         size=(4, 1), font=ButtonFont, border_width=1),
               sg.Button(key='EXIT', button_text="Don't save", button_color=default_button,
                         size=(10, 1), font=ButtonFont, border_width=1),
               sg.Button(key='CANCEL', button_text="Cancel", button_color=default_button,
                         size=(6, 1), font=ButtonFont, border_width=1)]]
    window = sg.Window('', layout, finalize=True, keep_on_top=True, icon=GUI_ICON, return_keyboard_events=True,
                       disable_minimize=True, size=(int(0.3 * my_width), int(0.28 * my_height)), force_toplevel=True,
                       resizable=False, grab_anywhere=False, grab_anywhere_using_control=False)
    window['SAVE'].bind('<Enter>', '+MOUSE OVER+')
    window['SAVE'].bind('<Leave>', '+MOUSE AWAY+')
    window['CANCEL'].bind('<Enter>', '+MOUSE OVER+')
    window['CANCEL'].bind('<Leave>', '+MOUSE AWAY+')
    window['BROWSE'].bind('<Enter>', '+MOUSE OVER+')
    window['BROWSE'].bind('<Leave>', '+MOUSE AWAY+')
    window['EXIT'].bind('<Enter>', '+MOUSE OVER+')
    window['EXIT'].bind('<Leave>', '+MOUSE AWAY+')
    window['-IN-'].bind("<Return>", "_Enter")
    window['-IN-'].widget.config(selectbackground=light_accent, selectforeground=text)
    window['-FOLDER-'].widget.config(selectbackground=light_accent, selectforeground=text)
    window['File Type'].widget.config(selectbackground=light_accent, selectforeground=text)
    close_program = False
    save = False
    while True:
        event, value = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'SAVE+MOUSE OVER+':
            window['SAVE'].update(button_color=accent_button_hover)
        elif event == 'SAVE+MOUSE AWAY+':
            window['SAVE'].update(button_color=accent_button)
        elif event == 'EXIT+MOUSE OVER+':
            window['EXIT'].update(button_color=default_button_hover)
        elif event == 'EXIT+MOUSE AWAY+':
            window['EXIT'].update(button_color=default_button)
        elif event == 'CANCEL+MOUSE OVER+':
            window['CANCEL'].update(button_color=default_button_hover)
        elif event == 'CANCEL+MOUSE AWAY+':
            window['CANCEL'].update(button_color=default_button)
        elif event == 'BROWSE+MOUSE OVER+':
            window['BROWSE'].update(button_color=default_button_hover)
        elif event == 'BROWSE+MOUSE AWAY+':
            window['BROWSE'].update(button_color=default_button)
        elif event == 'EXIT':
            close_program = True
            window.write_event_value(sg.WIN_CLOSED, None)
        elif event == 'SAVE':
            close_program = True
            window.write_event_value(sg.WIN_CLOSED, None)
            save = True
        elif event == 'CANCEL':
            close_program = False
            window.write_event_value(sg.WIN_CLOSED, None)
        elif event == '-IN-_Enter':
            window['-IN-'].update(text_color=text)
        if value['-IN-'] != default_file_text:
            window['-IN-'].update(text_color=text)

    window.close()

    return close_program, save
