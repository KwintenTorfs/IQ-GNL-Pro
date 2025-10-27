import FreeSimpleGUI as sg


def get_scaling():
    # called before window created
    root = sg.tk.Tk()
    scaling_factor = root.winfo_fpixels('1i')/72
    root.destroy()
    return scaling_factor


# Get the number for new screen
scaling_old = get_scaling()
width, height = sg.Window.get_screen_size()


# Find the number in original screen when GUI designed.
# call sg.Window.get_screen_size()
my_scaling = 1.334646962233169    # call get_scaling()
my_width, my_height = (1536, 864)
scaling = scaling_old * min(width / my_width, height / my_height)


# ORANGES
color = '#E9B453'
light = '#FFF0D4'
text_color = '#191E13'
darker = '#C69943'
various = '#F3F3F3'
background_color = 'white'
text_transparent = '#A3A3A3'
color_theme = {'BACKGROUND': background_color,
               'TEXT': text_color,
               'INPUT': various,
               'TEXT_INPUT': text_color,
               'SCROLL': light,
               'BUTTON': (text_color, various),
               'PROGRESS': (various, color),
               'BORDER': 1,
               'SLIDER_DEPTH': 0,
               'PROGRESS_DEPTH': 0}


background = color_theme.get('BACKGROUND')
text = color_theme.get('TEXT')
default_text = 'grey'
accent = color_theme.get('PROGRESS')[1]
light_accent = color_theme.get('SCROLL')
inverse = color_theme.get('INPUT')
darker_grey = '#dbdbdb'

sg.LOOK_AND_FEEL_TABLE['GNL GUI Theme'] = color_theme

FrameFont = 'Calibri 10 bold'
HighlightFont = 'Calibri 8 bold underline'
TitleFont = 'Calibri 16'
SmallFont = 'Calibri 4'
ButtonFont = 'Calibri 8'
TextFont = 'Calibri 8'
MenuFont = 'Calibri 9'
LargeFont = 'Calibri 11'
DefaultTextFont = 'Calibri 8 italic'

SpinSize = (10, 1)
default_button = (text, various)
default_button_hover = (text, light_accent)
accent_button = ('white', accent)
accent_button_hover = ('white', darker)
window_size = sg.Window.get_screen_size()
