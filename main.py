import PySimpleGUI as sg

from GUI.export import create_export_window, export_events
from GUI.folders import create_folders_window, folders_events
from GUI.gnl import create_gnl_window, gnl_events
from GUI.exit_screen import sure_you_want_to_close, valid_save_files
from Constants.design_GUI import my_width, my_height, scaling, width, height
from GUI.technique import create_technique_window, technique_events
from configuration import GUI_ICON


sg.set_options(scaling=scaling)


# Switch to use your newly created theme
sg.theme('GNL GUI Theme')

# Current Values
save_type = valid_save_files[0]


save_frame_size = (int(1 * my_width), int(0.08 * my_height))
frame_calculation = (int(0.4 * my_width), int(0.5 * my_height))
frame_plot = (int(0.6 * width), int(0.5 * height))
frame_table = (int(1 * my_width), int(0.45 * my_height))


layout = [[sg.Text('Welcome to GNOME',
                   justification='left', font='Calibri 30 bold', expand_x=True)],
          [sg.Push(), sg.Button('Export'), sg.Button('GNL'), sg.Button('TECHNIQUE'), sg.Button('FOLDERS')]]


# Window definition. Originally the GUI will not show the settings window, as it is only retrieved when the settings
#   button is invoked

window_main = sg.Window('IQ GNOME', layout, grab_anywhere=False, icon=GUI_ICON, finalize=True,
                        resizable=True)
window_main.Maximize()
window_export = None
window_gnl = None
window_technique = None
window_folders = None

# Things related to the plot window

plot_rows = []

folder_list = []
popup_win = None
browse_siblings = {}
previous_folder = None
save_table = None

while True:
    window, event, value = sg.read_all_windows()
    if event in [sg.WIN_CLOSED, 'Exit', '+ESCAPE+']:
        if window == window_main:
            window_main.DisableClose = True
            close_program, save = sure_you_want_to_close()
            if close_program:
                window.close()
                if window_export:
                    window_export.close()
                if window_gnl:
                    window_gnl.close()
                if window_technique:
                    window_technique.close()
                if window_folders:
                    window_folders.close()
                break
            window_main.DisableClose = False
        elif window == window_export:
            window.close()
            window_export = None
        elif window == window_gnl:
            window.close()
            window_gnl = None
        elif window == window_technique:
            window.close()
            window_technique = None
        elif window == window_folders:
            window.close()
            window_folders = None
    if event == 'Export':
        if window_export:
            window_export.TKroot.focus_set()
        else:
            window_export = create_export_window()
        if window_technique:
            window_technique.close()
            window_technique = None
        if window_gnl:
            window_gnl.close()
            window_gnl = None
        if window_folders:
            window_folders.close()
            window_folders = None
    elif event == 'GNL':
        if window_gnl:
            window_gnl.TKroot.focus_set()
        else:
            window_gnl = create_gnl_window()
        if window_technique:
            window_technique.close()
            window_technique = None
        if window_export:
            window_export.close()
            window_export = None
        if window_folders:
            window_folders.close()
            window_folders = None
    elif event == 'TECHNIQUE':
        if window_technique:
            window_technique.TKroot.focus_set()
        else:
            window_technique = create_technique_window()
        if window_gnl:
            window_gnl.close()
            window_gnl = None
        if window_export:
            window_export.close()
            window_export = None
        if window_folders:
            window_folders.close()
            window_folders = None
    elif event == 'FOLDERS':
        if window_folders:
            window_folders.TKroot.focus_set()
        else:
            window_folders = create_folders_window()
        if window_gnl:
            window_gnl.close()
            window_gnl = None
        if window_export:
            window_export.close()
            window_export = None
        if window_technique:
            window_technique.close()
            window_technique = None
    if window == window_export:
        export_events(window, event, value)
    elif window == window_gnl:
        gnl_events(window, event, value)
    elif window == window_technique:
        technique_events(window, event, value)
    elif window == window_folders:
        folders_events(window, event, value)

window.close()
