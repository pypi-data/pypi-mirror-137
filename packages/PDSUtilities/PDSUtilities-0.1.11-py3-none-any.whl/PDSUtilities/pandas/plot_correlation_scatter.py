# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PDSUtilities.pandas import get_numerical_columns
from PDSUtilities.plotly import apply_default
from PDSUtilities.plotly import get_font
from PDSUtilities.plotly import get_marker
from PDSUtilities.plotly import get_colors
from PDSUtilities.plotly import update_layout
from PDSUtilities.plotly import update_title
from PDSUtilities.plotly import update_width_and_height

def get_labels(columns, labels):
    if isinstance(labels, list):
        message = "Length of labels list must match length of columns list..."
        assert len(columns) == len(labels), message
        labels = { f"{columns[c]}": labels[c] for c in range(len(columns))}
    return labels

def get_correlation_label(correlations, columns, labels, row, col, precision, align = "middle"):
    BR = "<br />"
    col_label = labels.get(columns[col], columns[col])
    row_label = labels.get(columns[row], columns[row])
    cor_label = f"<b>{np.round(correlations.iloc[row, col], precision)}</b>"
    if align == "top":
        return "<span>" + cor_label + BR + col_label + BR + row_label + "</span>"
    if align == "bottom":
        return "<span>" + col_label + BR + row_label + BR + cor_label + "</span>"
    return "<span>" + col_label + BR + cor_label + BR + row_label + "</span>"

def get_center(values):
    return (0.5*(min(values) + max(values)))

def get_scatter_text(x, y, text, font = {}):
    # TODO: Need to test for more than just list...
    x = x if isinstance(x, list) else [x]
    y = y if isinstance(y, list) else [y]
    return go.Scatter(x = x, y = y, text = text, textfont = font,
        mode = 'text', showlegend = False, hoverinfo = "skip",
    )

def plot_correlation_scatter(df, target = None, columns = None, labels = {},
    width = None, height = None, title = None, precision = 4,
    template = None, colors = 0, marker = {},
    font = {}, axis_font = {}, tick_font = {}, legend_font = {}, hover_font = {},
    label_font = {}, title_font = {}):
    #
    font = apply_default(get_font(), font)
    axis_font = apply_default(font, axis_font)
    tick_font = apply_default(font, tick_font)
    label_font = apply_default(font, label_font)
    legend_font = apply_default(font, legend_font)
    #
    marker = apply_default(get_marker(), marker)
    #
    colors = get_colors(colors)
    columns = get_numerical_columns(df, columns, target)
    labels = get_labels(columns, labels)
    rows = [columns[c] for c in range(len(columns))]
    cols = [columns[c] for c in range(len(columns))]
    correlations = df[columns].corr()
    #
    values = [] if target is None else [value for value in df[target].unique()]
    values = [] if target is None else df[target].unique()
    #
    fig = make_subplots(rows = len(rows), cols = len(cols),
        horizontal_spacing = 0.1/len(cols),
        vertical_spacing = 0.1/len(rows),
        shared_xaxes = True,
        shared_yaxes = True,
        # print_grid = True,
    )
    for r in range(len(rows)):
        for c in range(r):
            text = get_correlation_label(
                correlations, columns, labels, r, c, precision, "middle"
            )
            for value in values:
                selection = df[target] == value
                fig.append_trace(
                    go.Scatter(
                        x = df[selection][cols[c]],
                        y = df[selection][rows[r]],
                        mode = 'markers',
                        marker = get_marker(marker, color = colors[value]),
                        name = labels.get(target, target) + " = " + str(value),
                        legendgroup = target + " = " + str(value),
                        hoverlabel = dict(font = hover_font),
                        showlegend = r == 1 and c == 0,
                    ),
                    r + 1, c + 1
                )
            if target is None:
                fig.append_trace(
                    go.Scatter(
                        x = df[cols[c]],
                        y = df[rows[r]],
                        mode = 'markers',
                        marker = get_marker(marker, color = colors[0]),
                        name = rows[r] + "/" + cols[c],
                        hoverlabel = dict(font = hover_font),
                        showlegend = False,
                    ),
                    r + 1, c + 1
                )
            # Used to center correlation text in
            # the plot as plotly annotations...
            fig.append_trace(
                get_scatter_text(
                    get_center(df[cols[c]]), get_center(df[rows[r]]), text, label_font
                ),
                c + 1, r + 1
            )
    # Point axes in upper plots to the axes
    # in the corresponding lower plots...
    for r in range(len(rows)):
        for c in range(r):
            # (r, c) corresponds to who we are pointing at...
            x, y = (len(rows) - 1)*len(cols) + c, r*len(cols)
            # So (c, r) is who we are...
            fig.update_xaxes(matches = f"x{x+1}", row = c + 1, col = r + 1)
            fig.update_yaxes(matches = f"y{y+1}", row = c + 1, col = r + 1)
    for r in range(len(rows)):
        fig.update_yaxes(
            title_text = labels.get(rows[r], rows[r]), row = r + 1, col = 1
        )
    for c in range(len(cols)):
        fig.update_xaxes(
            title_text = labels.get(cols[c], cols[c]), row = len(rows), col = c + 1
        )
    for r in range(len(rows)):
        for c in range(r, len(cols)):
            fig.update_xaxes(showgrid = False, row = r + 1, col = c + 1)
            fig.update_yaxes(showgrid = False, row = r + 1, col = c + 1)
        for c in range(1, len(cols)):
            fig.update_yaxes(ticks = "", row = r + 1, col = c + 1)
    for r in range(len(rows) - 1):
        for c in range(len(cols)):
            fig.update_xaxes(ticks = "", row = r + 1, col = c + 1)
    fig.update_xaxes(title_font= axis_font, tickfont = tick_font, linecolor = "black")
    fig.update_yaxes(title_font= axis_font, tickfont = tick_font, linecolor = "black")
    fig.update_xaxes(linewidth = 0.5, mirror = True, zeroline = False)
    fig.update_yaxes(linewidth = 0.5, mirror = True, zeroline = False)
    #
    fig.update_layout(legend_font = legend_font)
    if target is not None:
        fig.update_layout(legend_itemsizing = 'constant')
        fig.update_layout(legend = dict(
            orientation = 'h', yanchor = 'top', xanchor = 'center', y = 1.07, x = 0.5
        ))
    #
    fig = update_width_and_height(fig, width, height)
    fig = update_title(fig, title, title_font, font)
    fig = update_layout(fig, font = font, template = template)
    return fig