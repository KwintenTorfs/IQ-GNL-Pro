import PySimpleGUI as sg

from Constants.design_GUI import text, default_button, scaling, light_accent, accent_button, \
    default_button_hover, accent_button_hover, TextFont
from configuration import GUI_ICON


def popup_yes_no(title='Are you sure?'):
    layout = [[sg.Text(title, text_color=text, font='Calibri 10', background_color=light_accent)],
              [sg.Push(background_color=light_accent),
               sg.Button('Yes', button_color=default_button, font=TextFont, size=(5, 1)),
               sg.Button('No', button_color=accent_button, font=TextFont, size=(5, 1))]]
    sg.set_options(scaling=scaling)
    sg.theme('GNL GUI Theme')
    window = sg.Window(title='', layout=layout, icon=GUI_ICON, finalize=True, keep_on_top=True, disable_minimize=True,
                       no_titlebar=True, background_color=light_accent)
    window['Yes'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes'].bind('<Leave>', '+MOUSE AWAY+')
    window['No'].bind('<Enter>', '+MOUSE OVER+')
    window['No'].bind('<Leave>', '+MOUSE AWAY+')
    while True:
        event, value = window.read()
        if event in ['Yes', 'No']:
            window.close()
            return {'Yes': True, 'No': False}[event]
        elif event == 'Yes+MOUSE OVER+':
            window['Yes'].update(button_color=default_button_hover)
        elif event == 'Yes+MOUSE AWAY+':
            window['Yes'].update(button_color=default_button)
        elif event == 'No+MOUSE OVER+':
            window['No'].update(button_color=accent_button_hover)
        elif event == 'No+MOUSE AWAY+':
            window['No'].update(button_color=accent_button)
