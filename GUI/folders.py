import os.path

import PySimpleGUI as sg

from Constants.design_GUI import TitleFont, accent, window_size, TextFont, text, various, default_button, light_accent, \
    default_button_hover, SmallFont, accent_button, accent_button_hover
from GUI.popups import popup_yes_no
from configuration import GUI_ICON

settings_window_size = (int(0.4 * window_size[0]), int(0.55 * window_size[1]))
column_size = (20, 1)
folders_parameters = {'DB': True,
                      'SCAN': False,
                      'IMAGE': False,
                      'DB LOCATION': '',
                      'SCAN LOCATION': '',
                      'IMAGE LOCATION': '',
                      'DB FILES': [[], []],
                      'SCAN FILES': [[], []],
                      'IMAGE FILES': [[], []]}


def files_for_display(files):
    display_files = []
    for file in files:
        display_files.append(os.path.basename(file))
    return display_files


def folders_layout():
    global folders_parameters
    column_left = [[sg.Radio('Database', key='DB', group_id='EXPERIMENT', enable_events=True,
                             default=folders_parameters['DB'])],
                   [sg.Listbox(values=folders_parameters['DB FILES'][1], enable_events=True,
                               expand_x=True, expand_y=True, key='DB FILES', size=column_size,
                               highlight_background_color=light_accent, highlight_text_color=text)]]

    column_middle = [[sg.Radio('Scans', key='SCAN', group_id='EXPERIMENT', enable_events=True,
                               default=folders_parameters['SCAN'])],
                     [sg.Listbox(values=folders_parameters['SCAN FILES'][1], enable_events=True,
                                 expand_x=True, expand_y=True, key='SCAN FILES', size=column_size,
                                 highlight_background_color=light_accent, highlight_text_color=text)]]

    column_right = [[sg.Radio('Images', key='IMAGE', group_id='EXPERIMENT', enable_events=True,
                              default=folders_parameters['IMAGE'])],
                    [sg.Listbox(values=folders_parameters['IMAGE FILES'][1], enable_events=True,
                                expand_x=True, expand_y=True, key='IMAGE FILES', size=column_size,
                                highlight_background_color=light_accent, highlight_text_color=text)]]

    layout_db = [[sg.Text('Source folder', font=TextFont, text_color=text, justification='left')],
                 [sg.Input(key='DB LOCATION', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                           disabled=False, justification='left', background_color=various, border_width=1,
                           default_text=folders_parameters['DB LOCATION']),
                  sg.FolderBrowse(tooltip='Choose source folder', font=TextFont, button_color=default_button,
                                  size=(6, 1), key='FIND DB', enable_events=True)],
                 [sg.Push(),
                  sg.Button('Add Folder', key='ADD DB', button_color=accent_button, font=TextFont, size=(10, 1))]]

    layout_scan = [[sg.Text('Scan folder', font=TextFont, text_color=text, justification='left')],
                   [sg.Input(key='SCAN LOCATION', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                             disabled=False, justification='left', background_color=various, border_width=1,
                             default_text=folders_parameters['SCAN LOCATION']),
                    sg.FolderBrowse(tooltip='Choose scan folder', font=TextFont, button_color=default_button,
                                    size=(6, 1), key='FIND SCAN', enable_events=True)],
                   [sg.Push(),
                    sg.Button('Add Folder', key='ADD SCAN', button_color=accent_button, font=TextFont, size=(10, 1))]]

    layout_file = [[sg.Text('Select file', font=TextFont, text_color=text, justification='left')],
                   [sg.Input(key='IMAGE LOCATION', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                             disabled=False, justification='left', background_color=various, border_width=1,
                             default_text=folders_parameters['IMAGE LOCATION']),
                    sg.FileBrowse(tooltip='Choose file', font=TextFont, button_color=default_button,
                                  size=(6, 1), key='FIND IMAGE', enable_events=True)],
                   [sg.Push(),
                    sg.Button('Add File', key='ADD IMAGE', button_color=accent_button, font=TextFont, size=(8, 1))]]

    layout = [[sg.Text('Select Data', font=TitleFont, text_color=accent, justification='left')],
              [sg.Text('', font=SmallFont, text_color=text, justification='left')],
              [sg.Column(layout_db, expand_x=True, visible=folders_parameters['DB'], key='DB COLUMN'),
               sg.Column(layout_scan, expand_x=True, visible=folders_parameters['SCAN'], key='SCAN COLUMN'),
               sg.Column(layout_file, expand_x=True, visible=folders_parameters['IMAGE'], key='IMAGE COLUMN')],
              [sg.Column(column_left, expand_y=True, expand_x=True),
               sg.Column(column_middle, expand_x=True, expand_y=True),
               sg.Column(column_right, expand_y=True, expand_x=True)]
              ]
    return layout


def create_folders_window():
    layout = folders_layout()
    window_folders = sg.Window(title='', layout=layout, size=settings_window_size, icon=GUI_ICON, finalize=True)
    window_folders['DB LOCATION'].widget.config(selectbackground=light_accent, selectforeground=text)
    window_folders['SCAN LOCATION'].widget.config(selectbackground=light_accent, selectforeground=text)
    window_folders['IMAGE LOCATION'].widget.config(selectbackground=light_accent, selectforeground=text)
    window_folders['FIND DB'].bind('<Enter>', '+MOUSE OVER+')
    window_folders['FIND DB'].bind('<Leave>', '+MOUSE AWAY+')
    window_folders['FIND SCAN'].bind('<Enter>', '+MOUSE OVER+')
    window_folders['FIND SCAN'].bind('<Leave>', '+MOUSE AWAY+')
    window_folders['FIND IMAGE'].bind('<Enter>', '+MOUSE OVER+')
    window_folders['FIND IMAGE'].bind('<Leave>', '+MOUSE AWAY+')
    window_folders['ADD DB'].bind('<Enter>', '+MOUSE OVER+')
    window_folders['ADD DB'].bind('<Leave>', '+MOUSE AWAY+')
    window_folders['ADD SCAN'].bind('<Enter>', '+MOUSE OVER+')
    window_folders['ADD SCAN'].bind('<Leave>', '+MOUSE AWAY+')
    window_folders['ADD IMAGE'].bind('<Enter>', '+MOUSE OVER+')
    window_folders['ADD IMAGE'].bind('<Leave>', '+MOUSE AWAY+')
    window_folders['DB FILES'].bind('<Delete>', '+DELETE+')
    window_folders['SCAN FILES'].bind('<Delete>', '+DELETE+')
    window_folders['IMAGE FILES'].bind('<Delete>', '+DELETE+')

    window_folders.bind('<Escape>', '+ESCAPE+')
    return window_folders


def set_lists(window, db, scan, image):
    global folders_parameters
    window['DB FILES'].update(disabled=not db, values=folders_parameters['DB FILES'][1])
    window['SCAN FILES'].update(disabled=not scan, values=folders_parameters['SCAN FILES'][1])
    window['IMAGE FILES'].update(disabled=not image, values=folders_parameters['IMAGE FILES'][1])
    folders_parameters['DB'] = window['DB'].get()
    folders_parameters['SCAN'] = window['SCAN'].get()
    folders_parameters['IMAGE'] = window['IMAGE'].get()
    set_browse(window)


def swipe_lists(window):
    folders_parameters['DB FILES'] = [[], []]
    folders_parameters['SCAN FILES'] = [[], []]
    folders_parameters['IMAGE FILES'] = [[], []]
    set_all_lists(window)


def set_browse(window):
    for method in ['DB', 'SCAN', 'IMAGE']:
        window['%s COLUMN' % method].update(visible=folders_parameters[method])


def set_all_lists(window):
    for method in ['DB', 'SCAN', 'IMAGE']:
        files = '%s FILES' % method
        window[files].update(values=folders_parameters[files][1])


def folders_events(window, event, value):
    global folders_parameters
    if event in [sg.WIN_CLOSED, '+ESCAPE+']:
        return

    elif 'MOUSE OVER' in event and 'FIND' in event:
        window[event.split('+MOUSE OVER+')[0]].update(button_color=default_button_hover)
    elif 'MOUSE AWAY' in event and 'FIND' in event:
        window[event.split('+MOUSE AWAY+')[0]].update(button_color=default_button)

    elif 'LOCATION' in event and 'MOUSE' not in event:
        window['FIND %s' % event.split(' LOCATION')[0]].update(button_color=default_button)

    elif 'MOUSE OVER' in event and 'ADD' in event:
        window[event.split('+MOUSE OVER+')[0]].update(button_color=accent_button_hover)
    elif 'MOUSE AWAY' in event and 'ADD' in event:
        window[event.split('+MOUSE AWAY+')[0]].update(button_color=accent_button)

    elif 'ADD' in event and 'MOUSE' not in event:
        data_type = event.split('ADD ')[1]
        files = '%s FILES' % data_type
        loc = '%s LOCATION' % data_type
        location = window[loc].get()
        if location != '' and (os.path.isdir(location) or os.path.isfile(location)):
            if location not in folders_parameters[files][0]:
                folders_parameters[files][0].append(location)
                folders_parameters[files][1].append(os.path.basename(location))
                set_all_lists(window)
            else:
                sg.popup('Already In list', auto_close=True, auto_close_duration=1, any_key_closes=True, font=TextFont,
                         text_color=text, title='', no_titlebar=True, keep_on_top=True, background_color=light_accent,
                         button_color=accent_button)
        folders_parameters[loc] = ''
        window[loc].update(folders_parameters[loc])

    elif 'FILES' in event:
        print(event)
        data_type = event.split(' FILES')[0]
        files = '%s FILES' % data_type
        select_list = window[files].get()
        print(select_list)
        if not select_list:
            window[files].update(set_to_index=[])
            return
        selected = select_list[0]
        index = folders_parameters[files][1].index(selected)
        current_location = folders_parameters[files][0][index]
        if '+DELETE+' in event:
            folders_parameters[files][1].remove(selected)
            folders_parameters[files][0].remove(current_location)
            window[files].update(set_to_index=[])
            set_all_lists(window)
        elif 'DB' in event and folders_parameters['DB']:
            files_in_map = os.listdir(current_location)
            locations_in_map = []
            for file in files_in_map.copy():
                scan_location = os.path.join(current_location, file)
                if os.path.isdir(scan_location):
                    locations_in_map.append(scan_location)
                else:
                    files_in_map.remove(file)
            window['DB FILES'].update(set_to_index=selected)
            folders_parameters['SCAN FILES'][0] = locations_in_map
            folders_parameters['SCAN FILES'][1] = files_in_map
            set_all_lists(window)
        elif 'SCAN' in event and folders_parameters['SCAN']:
            files_in_map = os.listdir(current_location)
            print(current_location)
            print(files_in_map)
            locations_in_map = []
            for file in files_in_map.copy():
                scan_location = os.path.join(current_location, file)
                if os.path.isfile(scan_location):
                    locations_in_map.append(scan_location)
                else:
                    files_in_map.remove(file)
            window['SCAN FILES'].update(set_to_index=selected)
            folders_parameters['IMAGE FILES'][0] = locations_in_map
            folders_parameters['IMAGE FILES'][1] = files_in_map
            set_all_lists(window)
            # todo find method to add the sub-lists to the other list

    elif event == 'DB':
        if folders_parameters['DB']:
            return
        else:
            switch_method = popup_yes_no('Are you sure you want to switch methods?')
            if switch_method:
                swipe_lists(window)
                set_lists(window, True, True, False)
            else:
                for method in ['DB', 'SCAN', 'IMAGE']:
                    window[method].update(folders_parameters[method])
    elif event == 'SCAN':
        if folders_parameters['SCAN']:
            return
        else:
            switch_method = popup_yes_no('Are you sure you want to switch methods?')
            if switch_method:
                swipe_lists(window)
                set_lists(window, False, True, True)
            else:
                for method in ['DB', 'SCAN', 'IMAGE']:
                    window[method].update(folders_parameters[method])
    elif event == 'IMAGE':
        if folders_parameters['IMAGE']:
            return
        else:
            switch_method = popup_yes_no('Are you sure you want to switch methods?')
            if switch_method:
                swipe_lists(window)
                set_lists(window, False, False, True)
            else:
                for method in ['DB', 'SCAN', 'IMAGE']:
                    window[method].update(folders_parameters[method])

    return

