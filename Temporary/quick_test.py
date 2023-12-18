import os

location = r'C:\Users\ktorfs5\KU Leuven\PhD\Projects - Data and Material\2023 Kwinten - GNL and scan length\NEw Test.xlsx'

file_base = os.path.basename(location)
location = os.path.dirname(location)
temporary = os.path.join(location, 'TEMP ' + file_base).split('.')[0] + '.txt'
