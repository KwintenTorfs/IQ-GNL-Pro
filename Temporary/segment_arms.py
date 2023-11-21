import PySimpleGUI as sg

layout = [[sg.Checkbox('HALLO', key='BOX')],
          [sg.Button('YES'), sg.Button('NO')]]
window = sg.Window('Checkbox Example', layout, size=(715, 250))
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    elif event == 'NO':
        window['BOX'].update(visible=False)
    elif event == 'YES':
        window['BOX'].update(visible=True, text='BONJOUR')


window.close()
