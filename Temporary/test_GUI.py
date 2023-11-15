import PySimpleGUI as sg

filename = sg.popup_get_file('Will not see this message', no_window=True)

sg.popup('You selected:', filename)