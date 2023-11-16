import PySimpleGUI as sg

from Constants.design_GUI import accent, light_accent, text, various, FrameFont, window_size
from GUI.export import patient_parameters, tissue_parameters, slice_parameters, scanner_parameters, study_parameters
from GUI.technique import technique_parameters
from configuration import GUI_ICON

settings_window_size = (int(0.45 * window_size[0]), int(0.4 * window_size[1]))


def table_header(measure_per_scan):
    header = []
    for parameter in scanner_parameters.keys():
        if scanner_parameters[parameter]:
            header.append(parameter)
    for parameter in patient_parameters.keys():
        if patient_parameters[parameter]:
            header.append(parameter)
    for parameter in study_parameters.keys():
        if study_parameters[parameter]:
            header.append(parameter)
    if measure_per_scan:
        for parameter in slice_parameters.keys():
            if slice_parameters[parameter]:
                header.append('AVG %s' % parameter)
                header.append('STD %s' % parameter)
    else:
        for parameter in slice_parameters.keys():
            if slice_parameters[parameter]:
                header.append(parameter)

    for parameter in tissue_parameters.keys():
        if tissue_parameters[parameter]:
            header.append(parameter)
    header.append('Calculation technique')
    return header


def create_table_header():
    measure_per_scan = technique_parameters['PER SCAN']
    header = table_header(measure_per_scan)
    header_file = None
    if not measure_per_scan:
        header_file = table_header(not measure_per_scan)
    return header, header_file


def table_layout():
    headers, _ = create_table_header()
    widths = []
    for param in headers:
        widths.append(len(param) + 4)
    layout = [[sg.Table(values=[], headings=headers, auto_size_columns=False, max_col_width=30,
                        display_row_numbers=True, justification='center', col_widths=widths,
                        vertical_scroll_only=False, background_color='white', header_text_color='white',
                        header_background_color=accent, text_color=text, header_font=FrameFont,
                        alternating_row_color=light_accent, sbar_trough_color=light_accent,
                        sbar_arrow_color=accent,
                        sbar_background_color=various,
                        expand_x=True, expand_y=True, key='TABLE',
                        metadata=headers, select_mode="browse")]]
                        # right_click_menu=['&Right', right_click]
    return layout


def create_table_window():
    layout = table_layout()
    window_table = sg.Window(title='', layout=layout, size=settings_window_size, icon=GUI_ICON, finalize=True)
    window_table.bind('<Escape>', '+ESCAPE+')
    return window_table


def table_events(window, event, value):
    if '+MOUSE OVER+' in event:
        table_layout()
    return


