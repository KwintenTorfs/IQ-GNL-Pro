import PySimpleGUI as sg
import numpy as np

from Constants.design_GUI import text, various, accent, light_accent, FrameFont, TitleFont, ButtonFont, TextFont, \
    default_button, default_button_hover, accent_button, accent_button_hover, window_size
from configuration import GUI_ICON
from Support.Hounsfield_Units import get_original_hu_ranges, get_hounsfield_dictionary, add_hounsfield_range, \
    drop_hounsfield_tissue, hu_str2float, hu_float2str, infinity

settings_window_size = (int(0.45 * window_size[0]), int(0.4 * window_size[1]))
max_gnl_tissue_input = 5
max_name_input = 20
default_hu = {'LOW': 0,
              'HIGH': 170}
allowed_hu = '-0123456789∞'
frame_border = 1
frame_text_color = text
frame_color = 'white'
max_customisable_gnl = 25


def tissue_hu_files_to_table_input(hu_file):
    # Transform the data in the Tissue HU files to input for the GUI table
    hu_table = []
    default_tissues = get_original_hu_ranges().keys()
    for tissue in hu_file:
        if tissue in default_tissues:
            continue
        lo, hi = hu_file[tissue]
        lo, hi = hu_float2str(lo, hi)
        hu_table.append([tissue, lo, hi])
    return hu_table


def gnl_layout():
    original_tissues = get_original_hu_ranges()
    col1, col2, col3, col4, col5 = [], [], [], [], []
    for tissue in original_tissues.keys():
        hu_lo, hu_hi = original_tissues[tissue]
        hu_lo, hu_hi = hu_float2str(hu_lo, hu_hi)
        col1.append([sg.Text('%s' % tissue, font=TextFont, text_color=text, background_color=frame_color)])
        col2.append([sg.Text('%s' % hu_lo, font=TextFont, text_color=text, background_color=frame_color)])
        col3.append([sg.Text('-', font=TextFont, text_color=text, background_color=frame_color)])
        col4.append([sg.Text('%s' % hu_hi, font=TextFont, text_color=text, background_color=frame_color)])
        col5.append([sg.Text('HU', font=TextFont, text_color=text, background_color=frame_color)])

    layout_standard_gnl = [[sg.Column(col1, expand_x=True, expand_y=True, background_color=frame_color),
                            sg.Column(col2, expand_x=True, expand_y=True, background_color=frame_color),
                            sg.Column(col3, expand_x=True, expand_y=True, background_color=frame_color),
                            sg.Column(col4, expand_x=True, expand_y=True, background_color=frame_color),
                            sg.Column(col5, expand_x=True, expand_y=True, background_color=frame_color)]]

    standard_gnl = [sg.Frame('Default Tissues', layout=layout_standard_gnl, border_width=frame_border,
                             background_color=frame_color, expand_y=False, expand_x=True, font=FrameFont,
                             title_color=frame_text_color)]

    left_input = [[sg.Input(key='LOW', enable_events=True, font=TextFont, text_color=text, disabled=False,
                            size=(max_gnl_tissue_input, 1),  justification='center', background_color=various,
                            border_width=1, default_text=default_hu['LOW'])],
                  [sg.Button('-Inf', font=ButtonFont, button_color=default_button, size=(max_gnl_tissue_input - 1, 1),
                             key='-INF')]]

    right_input = [[sg.Input(key='HIGH', enable_events=True, font=TextFont, text_color=text, disabled=False,
                             size=(max_gnl_tissue_input, 1), justification='center', background_color=various,
                             border_width=1, default_text=default_hu['HIGH'])],
                   [sg.Button('Inf', font=ButtonFont, button_color=default_button, size=(max_gnl_tissue_input - 1, 1),
                              key='INF')]]

    layout_new_gnl = [[sg.Text('Name & HU range', font=TextFont, text_color=text, justification='left',
                               background_color=frame_color),
                       sg.Push(background_color=frame_color),
                       sg.Button('Add', key='ADD TISSUE', button_color=accent_button, font=ButtonFont,
                                 size=(4, 1))],
                      [sg.Input(key='NAME', enable_events=True, font=TextFont, text_color=text, disabled=False,
                                size=(max_name_input, 1), justification='left', background_color=various,
                                border_width=1)],
                      [sg.Column(left_input, background_color=frame_color),
                       sg.Column([[sg.Text('-', font=TextFont, text_color=text, background_color=frame_color)],
                                  [sg.Text('', expand_y=True, background_color=frame_color)]],
                                 background_color=frame_color),
                       sg.Column(right_input, background_color=frame_color),
                       sg.Column([[sg.Text('HU', font=TextFont, text_color=text, background_color=frame_color)],
                                  [sg.Text('', expand_y=True, background_color=frame_color)]],
                                 background_color=frame_color)
                       ],
                      ]

    current_hu_ranges = get_hounsfield_dictionary()
    available_hu_ranges = tissue_hu_files_to_table_input(current_hu_ranges)
    header = ['Name', 'Lower Limit (HU)', 'Upper Limit (HU)']
    max_values = [max_name_input, len(header[1]), len(header[2])]
    available_gnl_range = [[sg.Table(values=available_hu_ranges, headings=header, text_color=text,
                                     key='TABLE', tooltip='Ctrl+ Click for multiple (de)-select',
                                     font=TextFont, auto_size_columns=False,
                                     col_widths=np.array(max_values) + 2, expand_y=True, expand_x=True,
                                     selected_row_colors=(text, light_accent), hide_vertical_scroll=True,
                                     enable_events=False, enable_click_events=True)],
                           [sg.Push(background_color=frame_color),
                            sg.Button('Remove', key='REMOVE TISSUE', button_color=default_button, font=ButtonFont,
                                      size=(6, 1))]]

    right_column = [[sg.Frame('Custom Tissues', layout=available_gnl_range, border_width=frame_border,
                              background_color=frame_color, font=FrameFont, expand_x=True, expand_y=True,
                              title_color=frame_text_color)]]
    left_column = [standard_gnl,
                   [sg.Frame('Add New Tissue', layout=layout_new_gnl, border_width=frame_border,
                             background_color=frame_color, font=FrameFont, expand_x=True,
                             title_color=frame_text_color)]]

    layout = [[sg.Text('Select GNL tissues', font=TitleFont, text_color=accent, justification='left')],
              [sg.Column(left_column, expand_y=True),
               sg.Column(right_column, expand_y=True)],
              [sg.Text('', expand_y=True, expand_x=True)]]
    return layout


def create_gnl_window():
    layout = gnl_layout()
    window_gnl = sg.Window(title='', layout=layout, size=settings_window_size, icon=GUI_ICON, finalize=True)
    gnl_bindings(window_gnl)
    return window_gnl


def gnl_bindings(window):
    window['-INF'].bind('<Enter>', '+MOUSE OVER+')
    window['-INF'].bind('<Leave>', '+MOUSE AWAY+')
    window['INF'].bind('<Enter>', '+MOUSE OVER+')
    window['INF'].bind('<Leave>', '+MOUSE AWAY+')
    window['ADD TISSUE'].bind('<Enter>', '+MOUSE OVER+')
    window['ADD TISSUE'].bind('<Leave>', '+MOUSE AWAY+')
    window['REMOVE TISSUE'].bind('<Enter>', '+MOUSE OVER+')
    window['REMOVE TISSUE'].bind('<Leave>', '+MOUSE AWAY+')
    window['TABLE'].bind('<Delete>', '+DELETE+')
    window['TABLE'].bind('<Control_R><a>', '+CTRL+A+')
    window['TABLE'].bind('<Control_L><a>', '+CTRL+A+')
    window.bind('<Escape>', '+ESCAPE+')
    window['LOW'].widget.config(selectbackground=light_accent, selectforeground=text)
    window['HIGH'].widget.config(selectbackground=light_accent, selectforeground=text)
    window['NAME'].widget.config(selectbackground=light_accent, selectforeground=text)


def find_in_string(word, character):
    return [i for i, letter in enumerate(word) if letter == character]


def check_valid_tissue_range(tissue, low, high):
    return len(tissue) and type(tissue) == str \
        and all([i in allowed_hu for i in low]) and all([i in allowed_hu for i in high])


def gnl_events(window, event, value):
    if event in [sg.WIN_CLOSED, '+ESCAPE+']:
        return

    # Following events make sure that the input for HU is correct
    elif event in ['LOW', 'HIGH']:
        current_value = value[event]
        # - can only be the first character
        if len(current_value) > 1 and current_value[-1] == '-':
            current_value = current_value[:-1]
        minuses = find_in_string(current_value, '-')
        # no more than one - in any HU
        if len(minuses) > 1:
            if len(minuses) > 1 and max(minuses) != 0:
                current_value = str(default_hu[event])
        # If the last added value is not allowed, it is not added
        if len(current_value) and current_value[-1] not in allowed_hu:
            current_value = current_value[:-1]
        # If you copy a text and not all characters are allowed. The value is set to default
        if not all([character in allowed_hu for character in current_value]) and len(value):
            current_value = str(default_hu[event])
        window[event].update(current_value)
        # If the HU is too long for the text space, it is shortened
        if len(value[event]) > max_gnl_tissue_input:
            window[event].update(value[event][:-1])

    # If the name exceeds the space, it is shortened
    elif event == 'NAME':
        while len(window[event].get()) > max_name_input:
            window[event].update(window[event].get()[:-1])

    # These events are for automatic functions of buttons etc
    elif event == '-INF+MOUSE OVER+':
        window['-INF'].update(button_color=default_button_hover)
    elif event == '-INF+MOUSE AWAY+':
        window['-INF'].update(button_color=default_button)
    elif event == 'INF+MOUSE OVER+':
        window['INF'].update(button_color=default_button_hover)
    elif event == 'INF+MOUSE AWAY+':
        window['INF'].update(button_color=default_button)
    elif event == 'ADD TISSUE+MOUSE OVER+':
        window['ADD TISSUE'].update(button_color=accent_button_hover)
    elif event == 'ADD TISSUE+MOUSE AWAY+':
        window['ADD TISSUE'].update(button_color=accent_button)
    elif event == 'REMOVE TISSUE+MOUSE OVER+':
        window['REMOVE TISSUE'].update(button_color=default_button_hover)
    elif event == 'REMOVE TISSUE+MOUSE AWAY+':
        window['REMOVE TISSUE'].update(button_color=default_button)
    elif event == 'INF':
        window['HIGH'].update(infinity)
    elif event == '-INF':
        window['LOW'].update('-%s' % infinity)

    # Following Event will add a new custom tissue to the database
    elif event == 'ADD TISSUE':
        tissue = value['NAME']
        low = value['LOW']
        high = value['HIGH']
        if check_valid_tissue_range(tissue, low, high):
            if len(get_hounsfield_dictionary()) - len(get_original_hu_ranges()) < max_customisable_gnl:
                low, high = hu_str2float(low, high)
                add_hounsfield_range(tissue, [low, high])
                table_values = tissue_hu_files_to_table_input(get_hounsfield_dictionary())
                window['TABLE'].update(values=table_values)
            else:
                sg.popup('Custom tissue limit exceeded: %i' % max_customisable_gnl, icon=GUI_ICON, text_color=text,
                         button_color=accent_button, no_titlebar=True, background_color=light_accent)
                pass
            window['NAME'].update('')
            window['LOW'].update(default_hu['LOW'])
            window['HIGH'].update(default_hu['HIGH'])

    # Following Event will remove a custom tissue to the database
    elif event in ['REMOVE TISSUE', 'TABLE+DELETE+']:
        selected_rows = list(value['TABLE'])
        table = window['TABLE'].get()
        for row in selected_rows:
            tissue = table[row][0]
            drop_hounsfield_tissue(tissue)
        new_table_values = tissue_hu_files_to_table_input(get_hounsfield_dictionary())
        window['TABLE'].update(values=new_table_values)

    elif event == 'TABLE+CTRL+A+':
        nb_rows = len(window['TABLE'].get())
        window['TABLE'].update(select_rows=[i for i in range(nb_rows)])

    elif type(event) is tuple and len(event) == 3:
        if event[1] == '+CLICKED+' and event[2][0] is None:
            window['TABLE'].update(select_rows=[])
