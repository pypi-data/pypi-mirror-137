# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PDSUtilities.plotly import apply_default
from PDSUtilities.plotly import get_font
from PDSUtilities.plotly import ColorblindSafeColormaps

def get_categories_and_counts(df, column, target, value):
    categories = df[column].unique()
    df = df[df[target] == value]
    counts = [df[df[column] == category][column].count() for category in categories]
    return categories, counts

# Plotly is too smart and converts strings to numbers when
# possible but we're smarter: wrap numbers in <span></span>!
def to_string(value):
    if isinstance(value, str):
        return value
    return f"<span>{value}</span>"

def get_categories_and_counts(df, column, target = None, value = None):
    categories = df[column].unique()
    if target is not None:
        df = df[df[target] == value]
    counts = [df[df[column] == category][column].count() for category in categories]
    categories = [to_string(category) for category in categories]
    return categories, counts

def get_width(index):
    WIDTHS = [0.0, 0.1, 0.23, 0.34, 0.46, 0.65, 0.8]
    width = WIDTHS[index] if index < len(WIDTHS) else WIDTHS[-1]
    return width

def get_bins(bins, column):
    if isinstance(bins, int):
        return bins
    return bins.get(column, 0)

def get_histogram(x, color, show_legend, name, cumulative, bins):
    return go.Histogram(
        x = x, marker_color = color, showlegend = show_legend,
        name = name, cumulative_enabled = cumulative, nbinsx = bins,
        legendgroup = name,
    )

def get_bar(categories, counts, color, show_legend, name):
    return go.Bar(
        x = categories, y = counts,
        marker_color = color,
        showlegend = show_legend,
        name = name,
        width = get_width(len(categories)),
        legendgroup = name,
    )

def get_rcwh(rows, cols, width, height, columns, values):
    columns = len(columns)
    w, h = 250, 200
    if rows is None and cols is None:
        cols = max(2, min(5, int(np.ceil(np.sqrt(columns)))))
        rows = int(np.ceil(columns/cols))
    elif cols is None:
        cols = int(np.ceil(columns/rows))
    elif rows is None:
        rows = int(np.ceil(columns/cols))
    if width is None:
        if cols > 2 or cols == 2 and len(values) < 4:
            width = w*cols
        else:
            width = w*(cols + 1)
    if height is None:
        if cols > 2 or cols == 2 and len(values) < 4:
            height = 100 + h*rows
        else:
            height = h*rows
    return rows, cols, width, height

# produces histograms for all categorical and numerical columns in a pandas dataframe
def plot_histograms(df, target = None, columns = None, rows = None, cols = None, width = None, height = None,
    title = None, cumulative = None, barmode = "stack", opacity = 0.65, bins = 0,
    hovermode = "x unified", template = None, colors = 0, font = {}, title_font = {}, legend_font = {}):
    """
    plot_histograms produces histograms for all categorical and numerical columns in a pandas dataframe.

    Args:
        df (dataframe): the pandas dataframe to plot historgrams of.
        target (str, optional): the name of the target column whose values are used for grouping.
            Defaults to None.
        columns (list[str], optional): a list of column names to plot. Defaults to all columns.
        rows (int, optional): the number of rows in the grid the histograms are arranged in.
            Defaults to None.
        cols (int, optional): the number of columns in the grid the histograms are arranged in.
            Defaults to None.
        width (int, optional): the plot's width in pixels. Defaults to None.
        height (int, optional): the plot's height in pixels. Defaults to None.
        title (str or dict, optional): the title displayed at the top of the figure.
            Defaults to None.
        cumulative (bool, optional): produces cumulative histograms for each target variable, or the
            entire dataset if target = None. Defaults to None.
        barmode (str, optional): specifies whether the bars should be stacked, grouped or overlaid.
            Defaults to "stack".
        opacity (float, optional): set's the opacity of the bars when barmode = "overlay".
            Defaults to 0.65.
        bins (int or dict, optional): the number of bins for numerical colum histograms.
            Defaults to 0.
        hovermode (str, optional): specifies the style of hover popups.
            Defaults to "x unified".
        template (str, optional): the name of a plotly template to apply to the figure.
            Defaults to None.
        colors (int, str or list, optional): specifies the colors to be used for the bars.
            Defaults to 0.
        font (dict, optional): the font to be used in the histograms. Defaults to the default font.
        title_font (dict, optional): the font to be used for the figure title. Defaults to font.
        legend_font (dict, optional): the font to be used for the legend. Defaults to font.

    Returns:
        plotly.graph_objects.Figure: the plotly Figure encapsulating the histogram plots.
    """
    default_font = get_font()
    font = apply_default(default_font, font)
    legend_font = apply_default(font, legend_font)
    title_font = apply_default(
        apply_default(font, { 'size': font.get('size', 16) + 4 }),
        title_font
    )
    colors = 0 if colors is None else colors
    if isinstance(colors, int):
        colors = ColorblindSafeColormaps().get_colors(colors)
    #
    values = [] if target is None else [value for value in df[target].unique()]
        #
    if columns is None:
        columns = [column for column in df.columns if column != target]
    if not isinstance(columns, list):
        columns = [column for column in columns]
    if target is not None and target in columns:
        columns.remove(target)
    #
    rows, cols, width, height = get_rcwh(rows, cols, width, height, columns, values)
    fig = make_subplots(rows = rows, cols = cols,
        horizontal_spacing = 0.25/cols,
        vertical_spacing = 0.37/rows,
        subplot_titles = columns,
    )
    for index, column in enumerate(columns):
        for value in values:
            name = f"{target} = {value}"
            max_bins = get_bins(bins, column)
            color = colors[values.index(value) % len(colors)]
            if df[column].dtypes == object or len(df[column].unique()) <= len(colors):
                categories, counts = get_categories_and_counts(df, column, target, value)
                trace = get_bar(categories, counts, color, index == 0, name)
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
            else:
                x = df[df[target] == value][column]
                trace = get_histogram(x, color, index == 0, name, cumulative, max_bins)
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
        if target is None:
            if df[column].dtypes == object or len(df[column].unique()) <= len(colors):
                categories, counts = get_categories_and_counts(df, column)
                trace = get_bar(categories, counts, colors[0], False, column)
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
            else:
                trace = get_histogram(df[column], colors[0], False, column, cumulative, max_bins)
                fig.append_trace(trace, 1 + index // cols, 1 + index % cols)
    # barmode = ['stack', 'group', 'overlay', 'relative']
    # barmode = "stack"
    if barmode == "overlay":
        fig.update_traces(opacity = opacity)
    fig.update_annotations(font = font)
    fig.update_traces(marker_line_color = "#000000")
    fig.update_traces(marker_line_width = 0.5)
    if title is not None and isinstance(title, str):
        title = { 'text': title, 'x': 0.5, 'xanchor': "center" }
    if title is not None:
        fig.update_layout(title = title)
    if template is not None:
        fig.update_layout(template = template)
    if cols > 2 or cols == 2 and len(values) < 4:
        fig.update_layout(width = width, height = height, barmode = barmode,
            legend = dict(
                orientation = "h",
                yanchor = "bottom",
                y = 1.0 + 2.0*cols/100.0,
                xanchor = "center",
                x = 0.5
            ),
            margin = { 't': 160 },
        )
    fig.update_layout(hovermode = hovermode)
    fig.update_layout(width = width, height = height, barmode = barmode,
        font = font, title_font = title_font, legend_font = legend_font,
        # margin = { 't': 160 },
        # bargap = 0.2, # gap between bars of adjacent location coordinates
        # bargroupgap = 0*0.2, # gap between bars of the same location coordinates
    )
    # This is literally the dumbest thing I've seen in years...
    # This puts space between the ticks and tick labels. SMFH.
    fig.update_yaxes(ticksuffix = " ")
    return fig
