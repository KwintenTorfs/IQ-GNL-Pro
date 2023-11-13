import PySimpleGUI as sg

list1 = ['a', 'b', 'c']
list2 = []

layout = [[sg.Text("Demo")],
          [sg.Listbox(values=list1, size=(30, 6), enable_events=True, key="-LIST-"),
           sg.Button("Add", enable_events=True, key="-BUTTON-"),
           sg.Button("Remove", enable_events=True, key="-BUTTON2-"),
           sg.Listbox(values=list2, size=(30, 6), key="-LIST2-")],
          [sg.Cancel("Exit")]]

window = sg.Window("Beta", layout=layout, background_color="#272533", size=(650, 450))

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-BUTTON-":
        INDEX = int(''.join(map(str, window["-LIST-"].get_indexes())))
        list2.append(list1.pop(INDEX))
        window["-LIST2-"].update(list2)
        window["-LIST-"].update(list1)

    if event == "-BUTTON2-":
        INDEX = int(''.join(map(str, window["-LIST2-"].get_indexes())))
        list1.append(list2.pop(INDEX))
        window["-LIST2-"].update(list2)
        window["-LIST-"].update(list1)

window.close()