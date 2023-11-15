import PySimpleGUI as sg

from GUI.export import create_export_window, export_events
from GUI.folders import bind_folders, folders_events, folders_layout, folders_parameters, list_methods
from GUI.gnl import create_gnl_window, gnl_events
from GUI.exit_screen import sure_you_want_to_close, valid_save_files
from Constants.design_GUI import my_width, my_height, scaling, width, height, text, FrameFont, TextFont, MenuFont, \
    various
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

frame_border = 0
frame_color = 'white'
frame_text_color = text

menu = [['&File', ['Open...', 'Close']],
        ['&Settings', ['Export', 'Technique', 'GNL']],
        ]


layout_save = [[sg.OK()]]

column_left = [[sg.Text('Welcome to GNOME', justification='left', font='Calibri 30 bold', expand_x=True)],
               [sg.Frame('', layout=folders_layout(), border_width=frame_border, background_color=frame_color,
                         font=FrameFont, expand_x=True, expand_y=True, title_color=frame_text_color)],
               [sg.Frame('', layout=layout_save, border_width=frame_border, background_color=frame_color,
                         font=FrameFont, expand_x=True, title_color=frame_text_color)]
               ]

layout = [[sg.Menu(menu, text_color=text, font=MenuFont, background_color='white')],
          [sg.Column(column_left, expand_y=True)]]


# Window definition. Originally the GUI will not show the settings window, as it is only retrieved when the settings
#   button is invoked

window_main = sg.Window('IQ GNOME', layout, grab_anywhere=False, icon=GUI_ICON, finalize=True,
                        resizable=True)
window_main.Maximize()
window_export = None
window_gnl = None
window_technique = None
bind_folders(window_main)
# Things related to the plot window

plot_rows = []

folder_list = []
popup_win = None
browse_siblings = {}
previous_folder = None
save_table = None

while True:
    window, event, value = sg.read_all_windows()
    print(event, value)
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

    elif event == 'Technique':
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

    elif event == 'Open...':
        method_values = list(folders_parameters.values())[0:3]
        selected_method = list_methods[method_values.index(True)]
        if selected_method == 'IMAGE':
            folder = sg.popup_get_file('Will not see this message', no_window=True)
        else:
            folder = sg.popup_get_folder('', no_window=True)
        window['%s LOCATION' % selected_method].update(folder)
        # window.write_event_value('FIND %s' % selected_method, value)

    if window == window_export:
        export_events(window, event, value)
    elif window == window_gnl:
        gnl_events(window, event, value)
    elif window == window_technique:
        technique_events(window, event, value)
    else:
        folders_events(window, event, value)

window.close()
