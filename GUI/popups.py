# import PySimpleGUI as sg
import FreeSimpleGUI as sg
from Constants.Images.images_b64 import WARNING, image_rescale, QUESTION
from Constants.design_GUI import text, scaling, TextFont, MenuFont
from configuration import GUI_ICON


def popup_yes_no(message='Sure?', title='Sure?'):
    """
    Popup window that asks the user a yes-or-no question

    Parameters
    -----------
    message: str
        Message directed to the user
    title: str
        Title of the popup window

    Returns
    ---------
    boolean:
        A boolean depending on user input yes-or-no
    """
    bck_button = '#E1E1E1'
    highlight = '#0077D8'
    bck_high = '#E5F1FB'
    frame = '#C0C0C0'
    sg.set_options(scaling=scaling)
    sg.theme('GNL GUI Theme')
    yes = sg.Frame('', layout=[[sg.Text('', background_color=bck_button, key='Yes left', expand_x=True,
                                        enable_events=True),
                                sg.Button('Yes', border_width=0, enable_events=True, button_color=bck_button,
                                          font=MenuFont),
                                sg.Text('', background_color=bck_button, key='Yes right', expand_x=True,
                                        enable_events=True)]],
                   border_width=0, key='Yes FRAME', size=(70, 22), background_color=bck_button)

    no = sg.Frame('', layout=[[sg.Text('', background_color=bck_button, key='No left', expand_x=True,
                                       enable_events=True),
                               sg.Button('No', border_width=0, enable_events=True, button_color=bck_button,
                                         font=MenuFont),
                               sg.Text('', background_color=bck_button, key='No right', expand_x=True,
                                       enable_events=True)]],
                  border_width=0, key='No FRAME', size=(70, 22), background_color=bck_button)
    frame_under = '#F0F0F0'
    layout = [[sg.Column(layout=[[sg.Image(data=image_rescale(WARNING, 30, 30))]]),
               sg.Column(layout=[[sg.Text(message, text_color=text, font=TextFont)]])
               ],
              [sg.VPush()],
              [sg.Frame('', layout=[[sg.VPush(background_color=frame_under)],
                                    [sg.Push(background_color=frame_under), yes, no],
                                    [sg.VPush(background_color=frame_under)]], expand_x=True,
                        background_color=frame_under, pad=(0, 0), key='FRAME UNDER', border_width=0, size=(70, 40))]
              ]
    window = sg.Window(title, layout=layout, icon=GUI_ICON, finalize=True, keep_on_top=True,
                       grab_anywhere=True, disable_minimize=True, no_titlebar=False, size=(350, 100),
                       disable_close=True, margins=(0, 0), modal=True)

    window['FRAME UNDER'].Widget.configure(highlightbackground=bck_button, highlightcolor=bck_button,
                                           highlightthickness=1)
    window['Yes FRAME'].Widget.configure(highlightbackground=frame, highlightcolor=frame, highlightthickness=1)
    window['No FRAME'].Widget.configure(highlightbackground=highlight, highlightcolor=highlight, highlightthickness=2)

    window['No FRAME'].bind('<Enter>', '+MOUSE OVER+')
    window['No FRAME'].bind('<Leave>', '+MOUSE AWAY+')
    window['No'].bind('<Enter>', '+MOUSE OVER+')
    window['No'].bind('<Leave>', '+MOUSE AWAY+')
    window['No left'].bind('<Enter>', '+MOUSE OVER+')
    window['No left'].bind('<Leave>', '+MOUSE AWAY+')
    window['No right'].bind('<Enter>', '+MOUSE OVER+')
    window['No right'].bind('<Leave>', '+MOUSE AWAY+')
    window['Yes FRAME'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes FRAME'].bind('<Leave>', '+MOUSE AWAY+')
    window['Yes'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes'].bind('<Leave>', '+MOUSE AWAY+')
    window['Yes left'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes left'].bind('<Leave>', '+MOUSE AWAY+')
    window['Yes right'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes right'].bind('<Leave>', '+MOUSE AWAY+')
    window.bind('<Escape>', '+ESCAPE+')
    while True:
        event, value = window.read()
        if event in ['Yes', 'No', '+ESCAPE+']:
            window.close()
            return {'Yes': True, 'No': False, '+ESCAPE+': False}[event]

        elif 'MOUSE' in event:
            answer = 'No'
            if 'Yes' in event:
                answer = 'Yes'
            if 'OVER' in event:
                color = bck_high
                window[answer + ' FRAME'].Widget.configure(highlightbackground=highlight, highlightcolor=highlight,
                                                           highlightthickness=1)
            else:
                color = bck_button
                if answer == 'No':
                    window[answer + ' FRAME'].Widget.configure(highlightthickness=2)
                else:
                    window[answer + ' FRAME'].Widget.configure(highlightbackground=frame, highlightcolor=frame)
            window[answer].update(button_color=color)
            window[answer].ParentRowFrame.config(background=color)
            window[answer + ' FRAME'].Widget.configure(background=color)
            window[answer + ' left'].update(background_color=color)
            window[answer + ' right'].update(background_color=color)


def popup_close():
    """
    A popup window that asks the user to close the current program with a yes-or-no-question

    Returns
    ---------
    boolean:
        A boolean depending on user input yes-or-no
    """
    bck_button = '#E1E1E1'
    highlight = '#0077D8'
    bck_high = '#E5F1FB'
    frame = '#C0C0C0'
    sg.set_options(scaling=scaling)
    sg.theme('GNL GUI Theme')
    yes = sg.Frame('', layout=[[sg.Text('', background_color=bck_button, key='Yes left', expand_x=True,
                                        enable_events=True),
                                sg.Button('Yes', border_width=0, enable_events=True, button_color=bck_button,
                                          font=MenuFont),
                                sg.Text('', background_color=bck_button, key='Yes right', expand_x=True,
                                        enable_events=True)]],
                   border_width=0, key='Yes FRAME', size=(70, 22), background_color=bck_button)

    no = sg.Frame('', layout=[[sg.Text('', background_color=bck_button, key='No left', expand_x=True,
                                       enable_events=True),
                               sg.Button('No', border_width=0, enable_events=True, button_color=bck_button,
                                         font=MenuFont),
                               sg.Text('', background_color=bck_button, key='No right', expand_x=True,
                                       enable_events=True)]],
                  border_width=0, key='No FRAME', size=(70, 22), background_color=bck_button)
    frame_under = '#F0F0F0'
    layout = [[sg.Column(layout=[[sg.Image(data=image_rescale(QUESTION, 30, 30))]]),
               sg.Column(layout=[[sg.Text('Do you really want to close this program?\n'
                                          'All unprocessed data will be lost!', text_color=text, font=TextFont)]])
               ],
              [sg.VPush()],
              [sg.Frame('', layout=[[sg.VPush(background_color=frame_under)],
                                    [sg.Push(background_color=frame_under), yes, no],
                                    [sg.VPush(background_color=frame_under)]], expand_x=True,
                        background_color=frame_under, pad=(0, 0), key='FRAME UNDER', border_width=0, size=(70, 40))]
              ]
    window = sg.Window('Confirm Exit', layout=layout, icon=GUI_ICON, finalize=True, keep_on_top=True,
                       grab_anywhere=True, disable_minimize=True, no_titlebar=False, size=(350, 100),
                       disable_close=True, margins=(0, 0), modal=True)

    window['FRAME UNDER'].Widget.configure(highlightbackground=bck_button, highlightcolor=bck_button,
                                           highlightthickness=1)
    window['Yes FRAME'].Widget.configure(highlightbackground=frame, highlightcolor=frame, highlightthickness=1)
    window['No FRAME'].Widget.configure(highlightbackground=highlight, highlightcolor=highlight, highlightthickness=2)

    window['No FRAME'].bind('<Enter>', '+MOUSE OVER+')
    window['No FRAME'].bind('<Leave>', '+MOUSE AWAY+')
    window['No'].bind('<Enter>', '+MOUSE OVER+')
    window['No'].bind('<Leave>', '+MOUSE AWAY+')
    window['No left'].bind('<Enter>', '+MOUSE OVER+')
    window['No left'].bind('<Leave>', '+MOUSE AWAY+')
    window['No right'].bind('<Enter>', '+MOUSE OVER+')
    window['No right'].bind('<Leave>', '+MOUSE AWAY+')
    window['Yes FRAME'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes FRAME'].bind('<Leave>', '+MOUSE AWAY+')
    window['Yes'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes'].bind('<Leave>', '+MOUSE AWAY+')
    window['Yes left'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes left'].bind('<Leave>', '+MOUSE AWAY+')
    window['Yes right'].bind('<Enter>', '+MOUSE OVER+')
    window['Yes right'].bind('<Leave>', '+MOUSE AWAY+')
    window.bind('<Escape>', '+ESCAPE+')
    while True:
        event, value = window.read()
        if event in ['Yes', 'No', '+ESCAPE+']:
            window.close()
            return {'Yes': True, 'No': False, '+ESCAPE+': False}[event]

        elif 'MOUSE' in event:
            answer = 'No'
            if 'Yes' in event:
                answer = 'Yes'
            if 'OVER' in event:
                color = bck_high
                window[answer + ' FRAME'].Widget.configure(highlightbackground=highlight, highlightcolor=highlight,
                                                           highlightthickness=1)
            else:
                color = bck_button
                if answer == 'No':
                    window[answer + ' FRAME'].Widget.configure(highlightthickness=2)
                else:
                    window[answer + ' FRAME'].Widget.configure(highlightbackground=frame, highlightcolor=frame)
            window[answer].update(button_color=color)
            window[answer].ParentRowFrame.config(background=color)
            window[answer + ' FRAME'].Widget.configure(background=color)
            window[answer + ' left'].update(background_color=color)
            window[answer + ' right'].update(background_color=color)
