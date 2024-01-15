import os
import sys


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


project_name = 'GNL_GUI'

ROOT_DIR = resource_path(os.path.join(os.getcwd().split(project_name)[0], project_name))

GUI_ICON = resource_path(r'%s\assets\GUI Icon Orange.ico' % ROOT_DIR)

RESULTS_FOLDER = r'%s\Results' % ROOT_DIR
