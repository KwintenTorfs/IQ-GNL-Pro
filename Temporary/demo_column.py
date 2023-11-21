import numpy as np

from Constants.design_GUI import TextFont, TextFontBold, text
from GUI.export import tissue_parameters, nb_gnl_per_column, gnl_pre_text, box_color, frame_color, max_customisable_gnl
from Support.Hounsfield_Units import get_original_tissues
import PySimpleGUI as sg

original_tissues = get_original_tissues()
max_gnl_boxes = len(original_tissues) + max_customisable_gnl
nb_columns = np.ceil(max_gnl_boxes / nb_gnl_per_column).astype(int)
longest_word_gnl = max([len(i) for i in tissue_parameters.keys()])
size = (longest_word_gnl + 2, 1)
layout_columns = [[] for _ in range(nb_columns)]
# for i, tissue in enumerate(tissue_parameters.keys()):
#     column = np.floor(i / nb_gnl_per_column).astype(int)
#     font = TextFont
#     if tissue.split(gnl_pre_text)[1] in original_tissues:
#         font = TextFontBold
#     layout_columns[column].append([sg.Checkbox(text=tissue, default=tissue_parameters[tissue], size=size,
#                                                text_color=text, font=font, background_color=frame_color, key=tissue,
#                                                checkbox_color=box_color, enable_events=True, visible=False)])


i = 0
while i < max_gnl_boxes:
    column = np.floor(i / nb_gnl_per_column).astype(int)
    font = TextFont
    if i < len(tissue_parameters):
        tissue = list(tissue_parameters.keys())[i]
        if tissue.split(gnl_pre_text)[1] in original_tissues:
            font = TextFontBold
        layout_columns[column].append([sg.Checkbox(text=tissue, default=tissue_parameters[tissue], size=size,
                                                   text_color=text, font=font, background_color=frame_color, key=tissue,
                                                   checkbox_color=box_color, enable_events=True)])
    else:
        layout_columns[column].append([sg.Checkbox(text='', default=False, size=size, text_color=text, font=font,
                                                   background_color=frame_color, key='%i' % i, visible=False,
                                                   disabled=True, checkbox_color=box_color, enable_events=True)])
    i += 1


