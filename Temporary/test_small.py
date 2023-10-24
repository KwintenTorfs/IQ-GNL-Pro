import PySimpleGUI as sg
sg.theme('Dark Blue 3')
layout = [  [sg.Text('Move mouse over me', key='-TEXT-')],
            [sg.In(key='-IN-')],
            [sg.Button('Move mouse over me', key='-BUTTON-',border_width=0,button_color=('white','#2fa4e7'),font=('sans-serif',14)), sg.Button('Exit')] ]

window = sg.Window('Window Title', layout, finalize=True)
window['-BUTTON-'].bind('<Enter>', '+MOUSE OVER+')
window['-BUTTON-'].bind('<Leave>', '+MOUSE AWAY+')

while True:             # Event Loop
    event, values = window.read()
    if event=='-BUTTON-+MOUSE OVER+':
        window['-BUTTON-'].update(button_color = ('white','#178acc'))
    if event == '-BUTTON-+MOUSE AWAY+':
        window['-BUTTON-'].update(button_color=('white','#2fa4e7'))
    if event in (None, 'Exit'):
        break
window.close()