import numpy as np


def change_column_to_data_type(df, column, data_type):
    try:
        col = np.array(df[column])
        for i, element in enumerate(col):
            col[i] = data_type(element)
        df[column] = col
    except (ValueError, OverflowError, KeyError, TypeError):
        pass
