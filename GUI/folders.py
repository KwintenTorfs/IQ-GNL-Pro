import os.path
import threading

import PySimpleGUI as sg
import numpy as np

from Constants.Images.images_b64 import image_rescale, FOLDERBROWSEWHITE, FOLDERADDWHITE
from Constants.design_GUI import TitleFont, accent, window_size, TextFont, text, various, default_button, \
    light_accent, default_button_hover, accent_button, accent_button_hover, LargeFont
from GUI.popups import popup_yes_no
from GUI.save import darker_frame
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
methods = {'Database': 'DB',
           'Scans': 'SCAN',
           'Images': 'IMAGE'}

browse_operations = ['FIND', 'BROWSE', 'FRAME']
add_operations = ['ADD', 'ICON ADD', 'BOX ADD']

list_methods = list(methods.values())
method_names = list(methods.keys())


def files_for_display(files):
    display_files = []
    for file in files:
        display_files.append(os.path.basename(file))
    return display_files


def folders_layout():
    global folders_parameters
    right_click_menu = ['&Right', ['Delete', 'Siblings']]
    column_left = [[sg.Radio(method_names[0], key='DB', group_id='EXPERIMENT', enable_events=True,
                             default=folders_parameters['DB'])],
                   [sg.Listbox(values=folders_parameters['DB FILES'][1], enable_events=True,
                               expand_x=True, expand_y=True, key='DB FILES', size=column_size,
                               highlight_background_color=light_accent, highlight_text_color=text,
                               horizontal_scroll=True, right_click_menu=right_click_menu)]]

    column_middle = [[sg.Radio(method_names[1], key='SCAN', group_id='EXPERIMENT', enable_events=True,
                               default=folders_parameters['SCAN'])],
                     [sg.Listbox(values=folders_parameters['SCAN FILES'][1], enable_events=True,
                                 expand_x=True, expand_y=True, key='SCAN FILES', size=column_size,
                                 highlight_background_color=light_accent, highlight_text_color=text,
                                 horizontal_scroll=True, right_click_menu=right_click_menu)]]

    column_right = [[sg.Radio(method_names[2], key='IMAGE', group_id='EXPERIMENT', enable_events=True,
                              default=folders_parameters['IMAGE'])],
                    [sg.Listbox(values=folders_parameters['IMAGE FILES'][1], enable_events=True,
                                expand_x=True, expand_y=True, key='IMAGE FILES', size=column_size,
                                highlight_background_color=light_accent, highlight_text_color=text,
                                horizontal_scroll=True, right_click_menu=right_click_menu)]]

    layout_db = [[sg.Text('Source folder', font=TextFont, text_color=text, justification='left')],
                 [sg.Input(key='DB LOCATION', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                           disabled=False, justification='left', background_color=various, border_width=1,
                           default_text=folders_parameters['DB LOCATION']),
                  sg.Frame('', layout=[[sg.Button('', image_data=image_rescale(FOLDERBROWSEWHITE, 22, 15),
                                                  image_size=(22, 15), button_color='white', border_width=0,
                                                  key='BROWSE DB', button_type=sg.BUTTON_TYPE_BROWSE_FOLDER,
                                                  enable_events=True, target='DB LOCATION'),
                                        sg.Button('Browse', button_color='white', font=TextFont, border_width=0,
                                                  button_type=sg.BUTTON_TYPE_BROWSE_FOLDER, key='FIND DB', size=(7, 1),
                                                  enable_events=True, target='DB LOCATION')]],
                           key='FRAME DB', border_width=0, size=(100, 25))],
                 [sg.Push(),
                  sg.Frame('', layout=[[sg.Button('', image_data=image_rescale(FOLDERADDWHITE, 20, 15),
                                                  image_size=(22, 15), button_color='white', border_width=0,
                                                  key='ICON ADD DB', enable_events=True),
                                        sg.Button('Add folder', button_color='white', font=TextFont, border_width=0,
                                                  key='ADD DB', size=(10, 1), enable_events=True)]],
                           key='BOX ADD DB', border_width=0, size=(100, 25))]]

    layout_scan = [[sg.Text('Scan folder', font=TextFont, text_color=text, justification='left')],
                   [sg.Input(key='SCAN LOCATION', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                             disabled=False, justification='left', background_color=various, border_width=1,
                             default_text=folders_parameters['SCAN LOCATION']),
                    sg.Frame('', layout=[[sg.Button('', image_data=image_rescale(FOLDERBROWSEWHITE, 22, 15),
                                                    image_size=(22, 15), button_color='white', border_width=0,
                                                    key='BROWSE SCAN', button_type=sg.BUTTON_TYPE_BROWSE_FOLDER,
                                                    enable_events=True, target='SCAN LOCATION'),
                                          sg.Button('Browse', button_color='white', font=TextFont, border_width=0,
                                                    button_type=sg.BUTTON_TYPE_BROWSE_FOLDER, key='FIND SCAN',
                                                    size=(7, 1),
                                                    enable_events=True, target='SCAN LOCATION')]],
                             key='FRAME SCAN', border_width=0, size=(100, 25))],
                   [sg.Push(),
                    sg.Frame('', layout=[[sg.Button('', image_data=image_rescale(FOLDERADDWHITE, 20, 15),
                                                    image_size=(22, 15), button_color='white', border_width=0,
                                                    key='ICON ADD SCAN', enable_events=True),
                                          sg.Button('Add folder', button_color='white', font=TextFont, border_width=0,
                                                    key='ADD SCAN', size=(10, 1), enable_events=True)]],
                             key='BOX ADD SCAN', border_width=0, size=(100, 25))]]

    layout_file = [[sg.Text('Select file', font=TextFont, text_color=text, justification='left')],
                   [sg.Input(key='IMAGE LOCATION', expand_x=True, enable_events=True, font=TextFont, text_color=text,
                             disabled=False, justification='left', background_color=various, border_width=1,
                             default_text=folders_parameters['IMAGE LOCATION']),
                    sg.Frame('', layout=[[sg.Button('', image_data=image_rescale(FOLDERBROWSEWHITE, 22, 15),
                                                    image_size=(22, 15), button_color='white', border_width=0,
                                                    key='BROWSE IMAGE', button_type=sg.BUTTON_TYPE_BROWSE_FILE,
                                                    enable_events=True, target='IMAGE LOCATION'),
                                          sg.Button('Browse', button_color='white', font=TextFont, border_width=0,
                                                    button_type=sg.BUTTON_TYPE_BROWSE_FOLDER, key='FIND IMAGE',
                                                    size=(7, 1),
                                                    enable_events=True, target='IMAGE LOCATION')]],
                             key='FRAME IMAGE', border_width=0, size=(100, 25))],
                   [sg.Push(),
                    sg.Frame('', layout=[[sg.Button('', image_data=image_rescale(FOLDERADDWHITE, 20, 15),
                                                    image_size=(22, 15), button_color='white', border_width=0,
                                                    key='ICON ADD IMAGE', enable_events=True),
                                          sg.Button('Add file', button_color='white', font=TextFont, border_width=0,
                                                    key='ADD IMAGE', size=(10, 1), enable_events=True)]],
                             key='BOX ADD IMAGE', border_width=0, size=(100, 25))]]

    layout = [[sg.Text('Select Data', font=TitleFont, text_color=accent, justification='left')],
              [sg.Column(layout_db, expand_x=True, visible=folders_parameters['DB'], key='DB COLUMN'),
               sg.Column(layout_scan, expand_x=True, visible=folders_parameters['SCAN'], key='SCAN COLUMN'),
               sg.Column(layout_file, expand_x=True, visible=folders_parameters['IMAGE'], key='IMAGE COLUMN')],
              [sg.Column(column_left, expand_y=True, expand_x=True),
               sg.Column(column_middle, expand_x=True, expand_y=True),
               sg.Column(column_right, expand_y=True, expand_x=True)]
              ]
    return layout


def folders_bindings(window):
    window['DB LOCATION'].widget.config(selectbackground=light_accent, selectforeground=text)
    window['SCAN LOCATION'].widget.config(selectbackground=light_accent, selectforeground=text)
    window['IMAGE LOCATION'].widget.config(selectbackground=light_accent, selectforeground=text)
    window['ADD DB'].bind('<Enter>', '+MOUSE OVER+')
    window['ADD DB'].bind('<Leave>', '+MOUSE AWAY+')
    window['ADD SCAN'].bind('<Enter>', '+MOUSE OVER+')
    window['ADD SCAN'].bind('<Leave>', '+MOUSE AWAY+')
    window['ADD IMAGE'].bind('<Enter>', '+MOUSE OVER+')
    window['ADD IMAGE'].bind('<Leave>', '+MOUSE AWAY+')
    window['DB FILES'].bind('<Delete>', '+DELETE+')
    window['SCAN FILES'].bind('<Delete>', '+DELETE+')
    window['IMAGE FILES'].bind('<Delete>', '+DELETE+')
    for method in methods.values():
        for browse_operation in browse_operations:
            window['%s %s' % (browse_operation, method)].bind('<Enter>', '+MOUSE OVER+')
            window['%s %s' % (browse_operation, method)].bind('<Leave>', '+MOUSE AWAY+')
        for add_operation in add_operations:
            window['%s %s' % (add_operation, method)].bind('<Enter>', '+MOUSE OVER+')
            window['%s %s' % (add_operation, method)].bind('<Leave>', '+MOUSE AWAY+')
    window.bind('<Escape>', '+ESCAPE+')


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
    # If the window is closed
    if event in [sg.WIN_CLOSED, '+ESCAPE+']:
        return

    # For automatic events, involving buttons etc.
    elif 'MOUSE' in event:
        if 'OVER' in event:
            mouse_type = '+MOUSE OVER+'
            color = darker_frame
        else:
            mouse_type = '+MOUSE AWAY+'
            color = 'white'
        if any([method in event for method in methods.values()]):
            if any([button in event for button in browse_operations]):
                pure_event = event.split(mouse_type)[0]
                method = None
                for type_button in browse_operations:
                    splitting = pure_event.split('%s ' % type_button)
                    if len(splitting) > 1:
                        method = splitting[1]
                window['BROWSE %s' % method].update(button_color=color)
                window['FIND %s' % method].update(button_color=color)
                window['FRAME %s' % method].Widget.config(background=color)
                window['FIND %s' % method].ParentRowFrame.config(background=color)
                window['BROWSE %s' % method].ParentRowFrame.config(background=color)
            elif any([button in event for button in add_operations]):
                pure_event = event.split(mouse_type)[0]
                method = None
                for type_button in add_operations:
                    splitting = pure_event.split('%s ' % type_button)
                    if len(splitting) > 1:
                        method = splitting[1]
                window['ADD %s' % method].update(button_color=color)
                window['ICON ADD %s' % method].update(button_color=color)
                window['BOX ADD %s' % method].Widget.config(background=color)
                window['ICON ADD %s' % method].ParentRowFrame.config(background=color)
                window['ADD %s' % method].ParentRowFrame.config(background=color)

    elif 'LOCATION' in event and 'MOUSE' not in event:
        method = event.split(' LOCATION')[0]
        window['BROWSE %s' % method].update(button_color='white')
        window['FIND %s' % method].update(button_color='white')
        window['FRAME %s' % method].Widget.config(background='white')
        window['FIND %s' % method].ParentRowFrame.config(background='white')

    # To add a new file or folder to the existing selected lists
    elif 'ADD' in event and 'MOUSE' not in event and 'TISSUE' not in event:
        method = event.split('ADD ')[1]
        files = '%s FILES' % method
        loc = '%s LOCATION' % method
        location = window[loc].get().replace('/', '\\')
        color = 'white'
        window['ADD %s' % method].update(button_color=color)
        window['ICON ADD %s' % method].update(button_color=color)
        window['BOX ADD %s' % method].Widget.config(background=color)
        window['ICON ADD %s' % method].ParentRowFrame.config(background=color)
        window['ADD %s' % method].ParentRowFrame.config(background=color)
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

            create_sibling_folder_window(location, method, window)
        folders_parameters[loc] = ''
        window[loc].update(folders_parameters[loc])

    # Functions for all events concerning the individual lists
    elif 'FILES' in event:
        method = event.split(' FILES')[0]
        files = '%s FILES' % method
        all_selected_indices = window[files].get_indexes()
        if not all_selected_indices:
            return
        index = all_selected_indices[0]
        selected_value = window[files].get_list_values()[index]
        current_location = folders_parameters[files][0][index]

        # Operation 1 = deleting an event from the lists
        if '+DELETE+' in event:
            if not window[method].get():
                return
            method_index = list_methods.index(method)
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
        switch_folder_method(window, event)

    elif event in ['Delete', 'Siblings']:
        method_values = list(folders_parameters.values())[0:3]
        method = list_methods[method_values.index(True)]
        files = '%s FILES' % method
        selected_indices = window[files].get_indexes()
        if not selected_indices:
            return
        if event == 'Delete':
            window.write_event_value('%s+DELETE+' % files, value)
        elif event == 'Siblings':
            index = selected_indices[0]
            selected_location = folders_parameters[files][0][index]
            create_sibling_folder_window(selected_location, method, window)

    return


def switch_folder_method(window, event):
    global folders_parameters
    if folders_parameters[event]:
        return
    else:
        switch_method = popup_yes_no('Are you sure you want to switch methods?')
        if switch_method:
            swipe_lists(window)
            db, sc, im = enable_lists[event]
            set_lists(window, db, sc, im)
            if event == 'IMAGE':
                window['PER SLICE'].update(True)
                window['PER SCAN'].update(False, disabled=True)
                window['GNL ALL SLICE'].update(True, disabled=True)
                window['GNL MID AX'].update(False, disabled=True)
                window['GNL 10 SLICE'].update(False, disabled=True)
                window['GNL X SLICE'].update(False, disabled=True)
                window['NB'].update(disabled=True)
                window['text'].update(text_color='grey')
            else:
                window['PER SCAN'].update(disabled=False)
        else:
            for method in list_methods:
                window[method].update(folders_parameters[method])

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
