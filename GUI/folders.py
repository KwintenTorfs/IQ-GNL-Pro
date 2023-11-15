import os.path
import threading

import PySimpleGUI as sg
import numpy as np

from Constants.design_GUI import TitleFont, accent, window_size, TextFont, text, various, default_button, \
    light_accent, default_button_hover, accent_button, accent_button_hover
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


enable_lists = {'DB': [True, True, True],
                'SCAN': [False, True, True],
                'IMAGE': [False, False, True]}

list_methods = ['DB', 'SCAN', 'IMAGE']


def files_for_display(files):
    display_files = []
    for file in files:
        display_files.append(os.path.basename(file))
    return display_files


def folders_layout():
    global folders_parameters
    right_click_menu = ['&Right', ['Delete', 'Siblings']]
    column_left = [[sg.Radio('Database', key='DB', group_id='EXPERIMENT', enable_events=True,
                             default=folders_parameters['DB'])],
                   [sg.Listbox(values=folders_parameters['DB FILES'][1], enable_events=True,
                               expand_x=True, expand_y=True, key='DB FILES', size=column_size,
                               highlight_background_color=light_accent, highlight_text_color=text,
                               horizontal_scroll=True, right_click_menu=right_click_menu)]]

    column_middle = [[sg.Radio('Scans', key='SCAN', group_id='EXPERIMENT', enable_events=True,
                               default=folders_parameters['SCAN'])],
                     [sg.Listbox(values=folders_parameters['SCAN FILES'][1], enable_events=True,
                                 expand_x=True, expand_y=True, key='SCAN FILES', size=column_size,
                                 highlight_background_color=light_accent, highlight_text_color=text,
                                 horizontal_scroll=True, right_click_menu=right_click_menu)]]

    column_right = [[sg.Radio('Images', key='IMAGE', group_id='EXPERIMENT', enable_events=True,
                              default=folders_parameters['IMAGE'])],
                    [sg.Listbox(values=folders_parameters['IMAGE FILES'][1], enable_events=True,
                                expand_x=True, expand_y=True, key='IMAGE FILES', size=column_size,
                                highlight_background_color=light_accent, highlight_text_color=text,
                                horizontal_scroll=True, right_click_menu=right_click_menu)]]

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
              [sg.Column(layout_db, expand_x=True, visible=folders_parameters['DB'], key='DB COLUMN'),
               sg.Column(layout_scan, expand_x=True, visible=folders_parameters['SCAN'], key='SCAN COLUMN'),
               sg.Column(layout_file, expand_x=True, visible=folders_parameters['IMAGE'], key='IMAGE COLUMN')],
              [sg.Column(column_left, expand_y=True, expand_x=True),
               sg.Column(column_middle, expand_x=True, expand_y=True),
               sg.Column(column_right, expand_y=True, expand_x=True)]
              ]
    return layout


def bind_folders(window_folders):
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
    global folders_parameters
    for method in list_methods:
        folders_parameters['%s FILES' % method] = [[], []]
    set_all_lists(window)


def set_browse(window):
    global folders_parameters
    for method in list_methods:
        window['%s COLUMN' % method].update(visible=folders_parameters[method])


def set_all_lists(window):
    global folders_parameters
    for method in list_methods:
        files = "%s FILES" % method
        window[files].update(values=folders_parameters[files][1])


def folders_events(window, event, value):
    global folders_parameters

    # If the window is closed
    if event in [sg.WIN_CLOSED, '+ESCAPE+']:
        return

    # For automatic events, involving buttons etc.
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

    # To add a new file or folder to the existing selected lists
    elif 'ADD' in event and 'MOUSE' not in event:
        selected_method = event.split('ADD ')[1]
        files = '%s FILES' % selected_method
        loc = '%s LOCATION' % selected_method
        location = window[loc].get().replace('/', '\\')
        window[event].update(button_color=accent_button)
        if location != '' and (os.path.isdir(location) or os.path.isfile(location)):
            if location not in folders_parameters[files][0]:
                folders_parameters[files][0].append(location)
                folder = os.path.basename(location)
                folders_parameters[files][1].append(folder)
                set_all_lists(window)
            else:
                sg.popup('Already In list', auto_close=True, auto_close_duration=1, any_key_closes=True, font=TextFont,
                         text_color=text, title='', no_titlebar=True, keep_on_top=True, background_color=light_accent,
                         button_color=accent_button)

            create_sibling_folder_window(location, selected_method, window)
        folders_parameters[loc] = ''
        window[loc].update(folders_parameters[loc])

    # Functions for all events concerning the individual lists
    elif 'FILES' in event:
        selected_method = event.split(' FILES')[0]
        files = '%s FILES' % selected_method
        all_selected_indices = window[files].get_indexes()
        if not all_selected_indices:
            return
        index = all_selected_indices[0]
        selected_value = window[files].get_list_values()[index]
        current_location = folders_parameters[files][0][index]

        # Operation 1 = deleting an event from the lists
        if '+DELETE+' in event:
            if not window[selected_method].get():
                return
            method_index = list_methods.index(selected_method)
            delete_lists = [method for method in list_methods if list_methods.index(method) > method_index]
            for method in delete_lists:
                folders_parameters['%s FILES' % method] = [[], []]
            folders_parameters[files][1].remove(selected_value)
            folders_parameters[files][0].remove(current_location)
            window[files].update(set_to_index=[])
            set_all_lists(window)

        # Operation 2 = when selecting a value in DB => shows the sub-folders in SCAN
        elif 'DB' in event and folders_parameters['DB']:
            files_in_map = os.listdir(current_location)
            locations_in_map = []
            for file in files_in_map.copy():
                scan_location = os.path.join(current_location, file)
                if os.path.isdir(scan_location):
                    locations_in_map.append(scan_location)
                else:
                    files_in_map.remove(file)
            folders_parameters['SCAN FILES'][0] = locations_in_map
            folders_parameters['SCAN FILES'][1] = files_in_map
            set_all_lists(window)
            window['DB FILES'].update(set_to_index=index)
            window['IMAGE FILES'].update(values=[])

        # Operation 3 = when selecting a value in SCAN => shows the sub-files in IMAGE
        elif 'SCAN' in event:
            files_in_map = os.listdir(current_location)
            locations_in_map = []
            for file in files_in_map.copy():
                scan_location = os.path.join(current_location, file)
                if os.path.isfile(scan_location):
                    locations_in_map.append(scan_location)
                else:
                    files_in_map.remove(file)
            folders_parameters['IMAGE FILES'][0] = locations_in_map
            folders_parameters['IMAGE FILES'][1] = files_in_map
            set_all_lists(window)
            window['SCAN FILES'].update(set_to_index=index)

    # Event in case you are going to switch the method of getting slices
    elif event in list_methods:
        if folders_parameters[event]:
            return
        else:
            switch_method = popup_yes_no('Are you sure you want to switch methods?')
            if switch_method:
                swipe_lists(window)
                db, sc, im = enable_lists[event]
                set_lists(window, db, sc, im)
            else:
                for method in list_methods:
                    window[method].update(folders_parameters[method])

    elif event in ['Delete', 'Siblings']:
        method_values = list(folders_parameters.values())[0:3]
        selected_method = list_methods[method_values.index(True)]
        files = '%s FILES' % selected_method
        selected_indices = window[files].get_indexes()
        if not selected_indices:
            return
        if event == 'Delete':
            window.write_event_value('%s+DELETE+' % files, value)
        elif event == 'Siblings':
            index = selected_indices[0]
            selected_location = folders_parameters[files][0][index]
            create_sibling_folder_window(selected_location, selected_method, window)

    return


########################################################################################################################
#
# Popup with Sibling Folders
#

siblings_window_size = (int(0.2 * window_size[0]), int(0.4 * window_size[1]))


def find_sibling_directories(selected_location, method):
    global folders_parameters
    files = '%s FILES' % method
    location_list = folders_parameters[files][0]
    parent_folder = os.path.abspath(os.path.join(selected_location, os.pardir))
    sibling_folders, sibling_locations = [], []
    for f in os.scandir(parent_folder):
        if f.is_dir():
            location = f.path
            directory = os.path.basename(location)
            if location not in location_list and location != selected_location:
                sibling_folders.append(directory)
                sibling_locations.append(location)
    return sibling_folders, sibling_locations


def find_sibling_files(selected_location, method):
    global folders_parameters
    files = '%s FILES' % method
    location_list = folders_parameters[files][0]
    parent_folder = os.path.abspath(os.path.join(selected_location, os.pardir))
    sibling_folders, sibling_locations = [], []
    for f in os.scandir(parent_folder):
        if f.is_file():
            location = f.path
            directory = os.path.basename(location)
            if location not in location_list and location != selected_location:
                sibling_folders.append(directory)
                sibling_locations.append(location)
    return sibling_folders, sibling_locations


def create_sibling_folder_window(folder, method, window):
    global folders_parameters
    files = '%s FILES' % method
    parent_location = os.path.abspath(os.path.join(folder, os.pardir))
    if method in ['DB', 'SCAN']:
        siblings, sibling_locations = find_sibling_directories(folder, method)
    else:
        siblings, sibling_locations = find_sibling_files(folder, method)
    if not sibling_locations:
        return
    layout = [[sg.Text('Sibling folders', font=TitleFont, text_color=accent, justification='left')],
              [sg.Listbox(siblings, expand_x=True, expand_y=True, select_mode='multiple', key='SIBLINGS',
                          no_scrollbar=True, horizontal_scroll=True)],
              [sg.Push(),
               sg.Button('Reject all', key='REJECT', font=TextFont, button_color=default_button, size=(11, 1)),
               sg.Button('Select all', key='ALL', font=TextFont, button_color=default_button, size=(11, 1)),
               sg.Button('Add', key='ADD', button_color=accent_button, font=TextFont, size=(5, 1))]]

    window_siblings = sg.Window('', layout, finalize=True, size=siblings_window_size, icon=GUI_ICON, resizable=False,
                                disable_minimize=True, keep_on_top=True)
    popup_window = None
    window_siblings['ADD'].bind('<Enter>', '+MOUSE OVER+')
    window_siblings['ADD'].bind('<Leave>', '+MOUSE AWAY+')
    window_siblings['ALL'].bind('<Enter>', '+MOUSE OVER+')
    window_siblings['ALL'].bind('<Leave>', '+MOUSE AWAY+')
    window_siblings['REJECT'].bind('<Enter>', '+MOUSE OVER+')
    window_siblings['REJECT'].bind('<Leave>', '+MOUSE AWAY+')
    window_siblings.bind('<Escape>', '+ESCAPE+')

    window_siblings['SIBLINGS'].widget.config(selectbackground=light_accent, selectforeground=text)

    while True:
        event, value = window_siblings.read()

        if event in [sg.WIN_CLOSED, 'Exit', '+ESCAPE+']:
            window_siblings.close()
            break
        elif event == 'ADD+MOUSE OVER+':
            window_siblings['ADD'].update(button_color=accent_button_hover)
        elif event == 'ADD+MOUSE AWAY+':
            window_siblings['ADD'].update(button_color=accent_button)
        elif event == 'ALL+MOUSE OVER+':
            window_siblings['ALL'].update(button_color=default_button_hover)
        elif event == 'ALL+MOUSE AWAY+':
            window_siblings['ALL'].update(button_color=default_button)
        elif event == 'REJECT+MOUSE OVER+':
            window_siblings['REJECT'].update(button_color=default_button_hover)
        elif event == 'REJECT+MOUSE AWAY+':
            window_siblings['REJECT'].update(button_color=default_button)

        elif event == 'ALL':
            end = len(window_siblings['SIBLINGS'].get_list_values())
            indices = list(np.arange(0, end, 1))
            window_siblings['SIBLINGS'].update(set_to_index=indices)
        elif event == 'REJECT':
            window_siblings['SIBLINGS'].update(set_to_index=[])
        elif event == 'ADD':
            selected_siblings = value['SIBLINGS']
            window_siblings['ADD'].update(disabled=True)
            window_siblings['ALL'].update(disabled=True)
            window_siblings['REJECT'].update(disabled=True)
            popup_window = popup('Uploading...')
            threading.Thread(target=add_siblings,
                             args=(window_siblings, selected_siblings, parent_location, files,),
                             daemon=True).start()
            set_all_lists(window)
            if method in ['DB', 'SCAN']:
                siblings, _ = find_sibling_directories(folder, method)
            else:
                siblings, _ = find_sibling_files(folder, method)
            window_siblings['SIBLINGS'].update(values=siblings)

        elif event == 'DONE':
            popup_window.close()
            popup_window = None
            window_siblings['ADD'].update(disabled=False)
            window_siblings['ALL'].update(disabled=False)
            window_siblings['REJECT'].update(disabled=False)
            if not window_siblings['SIBLINGS'].get():
                window_siblings.write_event_value('Exit', None)

    return


def popup(message):
    sg.theme('DarkGrey')
    layout = [[sg.Text(message)]]
    window = sg.Window('Message', layout, no_titlebar=True, finalize=True, keep_on_top=True, grab_anywhere=True)
    sg.theme('GNL GUI Theme')
    return window


def add_siblings(window, selected_siblings, parent_location, files):
    global folders_parameters
    for selected_sibling in selected_siblings:
        location = os.path.join(parent_location, selected_sibling)
        if location not in folders_parameters[files][0]:
            folders_parameters[files][0].append(location)
            folders_parameters[files][1].append(selected_sibling)
    window.write_event_value('DONE', None)
