# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from pandas.api.types import is_integer_dtype
from PDSUtilities.pandas import get_numerical_columns
from PDSUtilities.plotly import get_colors
from PDSUtilities.plotly import apply_default
from PDSUtilities.plotly import get_font
from PDSUtilities.plotly import update_title
from PDSUtilities.plotly import update_width_and_height

def get_line(df, target, colors):
    line = dict(
        color = colors[0],
        showscale = False,
    )
    if target is not None:
        values = df[target]
        if df[target].dtypes == 'O':
            values = df[target].astype('category').cat.codes
        line['color'] = values
        line['colorscale'] = [
            colors[index] for index in range(len(np.unique(values)))
        ]
    return line

def get_dimension(df, column, labels):
    dimension = dict(
        values = df[column],
        label = labels.get(column, column),
        name = column,
    )
    if df[column].dtypes == 'O':
        categories = df[column].astype('category').cat
        dimension['values'] = categories.codes
        dimension['tickvals'] = np.sort(np.unique(categories.codes))
        dimension['ticktext'] = categories.categories
    elif is_integer_dtype(df[column]) and len(df[column].unique()) <= 8:
        dimension['tickvals'] = np.sort(df[column].unique())
        dimension['ticktext'] = np.sort(df[column].unique())
    return dimension

# TODO: #8 add template and misc args, comments and update README.md for plot_parallel functions...
def plot_parallel_coordinates(df, target = None, columns = None, labels = {},
    width = None, height = None, title = None, colors = 0,
    font = {}, tick_font = {}, axis_font = {}, title_font = {}):
    #
    font = apply_default(get_font(), font)
    #
    colors = get_colors(colors)
    columns = get_numerical_columns(df, columns)
    if target is not None and target not in columns:
        columns = [target] + columns
    #
    if target is not None and target not in columns:
        columns = [target] + columns
    fig = go.Figure(go.Parcoords(
        dimensions = list([
            get_dimension(df, column, labels)
            for column in columns
        ]),
        line = get_line(df, target, colors),
        labelfont = apply_default(font, axis_font),
        tickfont = apply_default(font, tick_font),
        # This eliminates the range! Set color to background!
        rangefont = { 'size': 1, 'color': "#FFFFFF" }
    ))
    fig = update_width_and_height(fig, width, height)
    fig = update_title(fig, title, title_font, font)
    # if template is not None:
    #     fig.update_layout(template = template)
    fig.update_layout(font = font)
    return fig