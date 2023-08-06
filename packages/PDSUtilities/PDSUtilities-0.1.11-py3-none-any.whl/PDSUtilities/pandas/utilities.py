import pandas as pd

def get_numerical_columns(df, columns = None, remove = None):
    if columns is None:
        columns = [column for column in df.columns if df[column].dtypes != 'O']
    if not isinstance(columns, list):
        columns = [column for column in columns]
    if remove is not None and remove in columns:
        columns.remove(remove)
    return columns

def get_categorical_columns(df, columns = None, remove = None):
    if columns is None:
        columns = [column for column in df.columns if df[column].dtypes == 'O']
    if not isinstance(columns, list):
        columns = [column for column in columns]
    if remove is not None and remove in columns:
        columns.remove(remove)
    return columns
