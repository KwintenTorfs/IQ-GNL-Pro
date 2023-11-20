import PySimpleGUI as sg

from GUI.export import create_export_window, export_events
from GUI.folders import folders_bindings, folders_events, folders_layout, folders_parameters, list_methods, method_names, \
    methods
from GUI.gnl import gnl_events, gnl_layout, gnl_bindings
from GUI.exit_screen import sure_you_want_to_close, valid_save_files
from Constants.design_GUI import my_width, my_height, scaling, width, height, text, FrameFont, MenuFont, \
    accent
from GUI.table import table_events, create_table_window
from GUI.technique import technique_events, technique_layout, technique_bindings
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
        ['&Settings', ['Export', 'Technique', 'GNL', '&Method', [method_names]]],
        ['&Table', ['Show data...']]
        ]


tab_open_files = sg.Tab('Open Files', [[sg.Frame('', layout=folders_layout(), border_width=frame_border,
                                                 background_color=frame_color, font=FrameFont, expand_x=True,
                                                 expand_y=True, title_color=frame_text_color)]],
                        key='OPEN FILES')
tab_gnl = sg.Tab('Set GNL', [[sg.Frame('', layout=gnl_layout(), border_width=frame_border,
                                       background_color=frame_color, font=FrameFont, expand_x=True,
                                       expand_y=True, title_color=frame_text_color)]], key='GNL TAB')

tab_technique = sg.Tab('Technique', [[sg.Frame('', layout=technique_layout(), border_width=frame_border,
                                               background_color=frame_color, font=FrameFont, expand_x=True,
                                               expand_y=True, title_color=frame_text_color)]], key='TECHNIQUE TAB')

column_left = [[sg.Text('Welcome to GNOME', justification='left', font='Calibri 30 bold', expand_x=True)],
               [sg.TabGroup([[tab_open_files, tab_gnl, tab_technique]],
                            expand_y=True, expand_x=True, font=MenuFont, title_color=text,
                            selected_title_color=accent, enable_events=True, key='TAB GROUP')],
               ]

column_right = [[]]

layout = [[sg.Menu(menu, text_color=text, font=MenuFont, background_color='white')],
          [sg.Column(column_left, expand_y=True)]]


# Window definition. Originally the GUI will not show the settings window, as it is only retrieved when the settings
#   button is invoked

window_main = sg.Window('IQ GNOME', layout, grab_anywhere=False, icon=GUI_ICON, finalize=True,
                        resizable=True)
window_main.Maximize()
window_export = None
window_table = None
technique_bindings(window_main)
gnl_bindings(window_main)
folders_bindings(window_main)
# Things related to the plot window

plot_rows = []

folder_list = []
popup_win = None
browse_siblings = {}
previous_folder = None
save_table = None

while True:
    window, event, value = sg.read_all_windows()
    print(event)
    if event in [sg.WIN_CLOSED, 'Exit', '+ESCAPE+']:
        if window == window_main:
            window_main.DisableClose = True
            close_program, save = sure_you_want_to_close()
            if close_program:
                window.close()
                if window_export:
                    window_export.close()
                if window_table:
                    window_table.close()
                break
            window_main.DisableClose = False
        elif window == window_export:
            window.close()
            window_export = None
        elif window == window_table:
            window.close()
            window_table = None

    if event == 'Export':
        if window_export:
            window_export.TKroot.focus_set()
        else:
            window_export = create_export_window()
        if window_table:
            window_table.close()
            window_table = None

    elif event == 'Show data...':
        if window_table:
            window_table.TKroot.focus_set()
        else:
            window_table = create_table_window()
        if window_export:
            window_export.close()
            window_export = None

    elif event == 'Open...':
        method_values = list(folders_parameters.values())[0:3]
        selected_method = list_methods[method_values.index(True)]
        if selected_method == 'IMAGE':
            folder = sg.popup_get_file('', no_window=True)
        else:
            folder = sg.popup_get_folder('', no_window=True)
        window['%s LOCATION' % selected_method].update(folder)

    elif event in method_names:
        method = methods[event]
        for m in list_methods:
            if m == method:
                window[m].update(True)
            else:
                window[m].update(False)
        window.write_event_value(method, value)

    elif window == window_export:
        export_events(window, event, value)
    # elif window == window_gnl:
    #     gnl_events(window, event, value)
    # elif window == window_technique:
    #     technique_events(window, event, value, window_main)
    elif window == window_table:
        table_events(window, event, value)
    else:
        tab = window_main['TAB GROUP'].get()
        if tab == 'OPEN FILES':
            folders_events(window, event, value)
        elif tab == 'GNL TAB':
            gnl_events(window, event, value)
        elif tab == 'TECHNIQUE TAB':
            technique_events(window, event, value, window_main)


window.close()
