# -*- coding: utf-8 -*-
"""Collection of functions for the manipulation of time series."""

from __future__ import absolute_import, division, print_function

import itertools
import os
import warnings

import mando
import numpy as np
import pandas as pd
from mando.rst_text_formatter import RSTHelpFormatter
from tstoolbox import tsutils

from .. import plotutils

warnings.filterwarnings("ignore")


@mando.command("bar_stacked", formatter_class=RSTHelpFormatter, doctype="numpy")
@tsutils.doc(plotutils.ldocstrings)
def bar_stacked_cli(
    input_ts="-",
    columns=None,
    start_date=None,
    end_date=None,
    clean=False,
    skiprows=None,
    index_type="datetime",
    names=None,
    ofilename="plot.png",
    xtitle="",
    ytitle="",
    title="",
    figsize="10,6.0",
    legend=None,
    legend_names=None,
    subplots=False,
    sharex=True,
    sharey=False,
    colors="auto",
    linestyles="auto",
    markerstyles=" ",
    bar_hatchstyles="auto",
    style="auto",
    logx=False,
    logy=False,
    xaxis="arithmetic",
    yaxis="arithmetic",
    xlim=None,
    ylim=None,
    secondary_y=False,
    mark_right=True,
    scatter_matrix_diagonal="kde",
    bootstrap_size=50,
    bootstrap_samples=500,
    norm_xaxis=False,
    norm_yaxis=False,
    lognorm_xaxis=False,
    lognorm_yaxis=False,
    xy_match_line="",
    grid=False,
    label_rotation=None,
    label_skip=1,
    force_freq=None,
    drawstyle="default",
    por=False,
    invert_xaxis=False,
    invert_yaxis=False,
    round_index=None,
    plotting_position="weibull",
    prob_plot_sort_values="descending",
    source_units=None,
    target_units=None,
    lag_plot_lag=1,
    plot_styles="bright",
    hlines_y=None,
    hlines_xmin=None,
    hlines_xmax=None,
    hlines_colors=None,
    hlines_linestyles="-",
    vlines_x=None,
    vlines_ymin=None,
    vlines_ymax=None,
    vlines_colors=None,
    vlines_linestyles="-",
):
    r"""Stacked vertical bar, sometimes called a stacked column plot.

    "barh_stacked" creates a horizontal stacked bar plot.

    Parameters
    ----------
    {input_ts}
    {ofilename}
    {lag_plot_lag}
    {xtitle}
    {ytitle}
    {title}
    {figsize}
    {legend}
    {legend_names}
    {subplots}
    {sharex}
    {sharey}
    {colors}
    {linestyles}
    {markerstyles}
    {style}
    {bar_hatchstyles}
    {xlim}
    {ylim}
    {xaxis}
    {yaxis}
    secondary_x
        {secondary}
    {mark_right}
    {grid}
    {label_rotation}
    {label_skip}
    {por}
    {force_freq}
    {invert_xaxis}
    {columns}
    {start_date}
    {end_date}
    {clean}
    {skiprows}
    {index_type}
    {names}
    {source_units}
    {target_units}
    {round_index}
    {plot_styles}
    {vlines_x}
    {vlines_colors}
    {vlines_linestyles}
    """
    plt = bar_stacked(
        input_ts=input_ts,
        columns=columns,
        start_date=start_date,
        end_date=end_date,
        clean=clean,
        skiprows=skiprows,
        index_type=index_type,
        names=names,
        ofilename=ofilename,
        xtitle=xtitle,
        ytitle=ytitle,
        title=title,
        figsize=figsize,
        legend=legend,
        legend_names=legend_names,
        subplots=subplots,
        sharex=sharex,
        sharey=sharey,
        colors=colors,
        linestyles=linestyles,
        markerstyles=markerstyles,
        bar_hatchstyles=bar_hatchstyles,
        style=style,
        logx=logx,
        logy=logy,
        xaxis=xaxis,
        yaxis=yaxis,
        xlim=xlim,
        ylim=ylim,
        secondary_y=secondary_y,
        mark_right=mark_right,
        scatter_matrix_diagonal=scatter_matrix_diagonal,
        bootstrap_size=bootstrap_size,
        bootstrap_samples=bootstrap_samples,
        norm_xaxis=norm_xaxis,
        norm_yaxis=norm_yaxis,
        lognorm_xaxis=lognorm_xaxis,
        lognorm_yaxis=lognorm_yaxis,
        xy_match_line=xy_match_line,
        grid=grid,
        label_rotation=label_rotation,
        label_skip=label_skip,
        force_freq=force_freq,
        drawstyle=drawstyle,
        por=por,
        invert_xaxis=invert_xaxis,
        invert_yaxis=invert_yaxis,
        round_index=round_index,
        plotting_position=plotting_position,
        prob_plot_sort_values=prob_plot_sort_values,
        source_units=source_units,
        target_units=target_units,
        lag_plot_lag=lag_plot_lag,
        plot_styles=plot_styles,
        hlines_y=hlines_y,
        hlines_xmin=hlines_xmin,
        hlines_xmax=hlines_xmax,
        hlines_colors=hlines_colors,
        hlines_linestyles=hlines_linestyles,
        vlines_x=vlines_x,
        vlines_ymin=vlines_ymin,
        vlines_ymax=vlines_ymax,
        vlines_colors=vlines_colors,
        vlines_linestyles=vlines_linestyles,
    )


# @tsutils.validator(
#     ofilename=[str, ["pass", []], 1],
#     type=[str, ["domain", ["bar_stacked",],], 1,],
#     lag_plot_lag=[int, ["range", [1, None]], 1],
#     xtitle=[str, ["pass", []], 1],
#     ytitle=[str, ["pass", []], 1],
#     title=[str, ["pass", []], 1],
#     figsize=[float, ["range", [0, None]], 2],
#     legend=[bool, ["domain", [True, False]], 1],
#     legend_names=[str, ["pass", []], 1],
#     subplots=[bool, ["domain", [True, False]], 1],
#     sharex=[bool, ["domain", [True, False]], 1],
#     sharey=[bool, ["domain", [True, False]], 1],
#     colors=[str, ["pass", []], None],
#     linestyles=[str, ["domain", ["auto", None, "", " ", "  "] + plotutils.LINE_LIST], None],
#     markerstyles=[str, ["domain", ["auto", None, "", " ", "  "] + plotutils.MARKER_LIST], None],
#     bar_hatchstyles=[str, ["domain", ["auto", None, "", " ", "  "] + plotutils.HATCH_LIST], None],
#     style=[str, ["pass", []], None],
#     xlim=[float, ["pass", []], 2],
#     ylim=[float, ["pass", []], 2],
#     xaxis=[str, ["domain", ["arithmetic", "log"]], 1],
#     yaxis=[str, ["domain", ["arithmetic", "log"]], 1],
#     secondary_y=[bool, ["domain", [True, False]], 1],
#     mark_right=[bool, ["domain", [True, False]], 1],
#     scatter_matrix_diagonal=[str, ["domain", ["kde", "hist"]], 1],
#     bootstrap_size=[int, ["range", [0, None]], 1],
#     xy_match_line=[str, ["pass", []], 1],
#     grid=[bool, ["domain", [True, False]], 1],
#     label_rotation=[float, ["pass", []], 1],
#     label_skip=[int, ["range", [1, None]], 1],
#     drawstyle=[str, ["pass", []], 1],
#     por=[bool, ["domain", [True, False]], 1],
#     invert_xaxis=[bool, ["domain", [True, False]], 1],
#     invert_yaxis=[bool, ["domain", [True, False]], 1],
#     plotting_position=[
#         str,
#         [
#             "domain",
#             ["weibull", "benard", "tukey", "gumbel", "hazen", "cunnane", "california"],
#         ],
#         1,
#     ],
#     prob_plot_sort_values=[str, ["domain", ["ascending", "descending"]], 1],
#     plot_styles=[
#         str,
#         [
#             "domain",
#             [
#                 "classic",
#                 "Solarize_Light2",
#                 "bmh",
#                 "dark_background",
#                 "fast",
#                 "fivethirtyeight",
#                 "ggplot",
#                 "grayscale",
#                 "seaborn",
#                 "seaborn-bright",
#                 "seaborn-colorblind",
#                 "seaborn-dark",
#                 "seaborn-dark-palette",
#                 "seaborn-darkgrid",
#                 "seaborn-deep",
#                 "seaborn-muted",
#                 "seaborn-notebook",
#                 "seaborn-paper",
#                 "seaborn-pastel",
#                 "seaborn-poster",
#                 "seaborn-talk",
#                 "seaborn-ticks",
#                 "seaborn-white",
#                 "seaborn-whitegrid",
#                 "tableau-colorblind10",
#                 "science",
#                 "grid",
#                 "ieee",
#                 "scatter",
#                 "notebook",
#                 "high-vis",
#                 "bright",
#                 "vibrant",
#                 "muted",
#                 "retro",
#             ],
#         ],
#         None,
#     ],
#     hlines_y=[float, ["pass", []], None],
#     hlines_xmin=[float, ["pass", []], None],
#     hlines_xmax=[float, ["pass", []], None],
#     hlines_colors=[str, ["pass", []], None],
#     hlines_linestyles=[
#         str,
#         ["domain", ["auto", None, "", " ", "  "] + plotutils.LINE_LIST],
#         None,
#     ],
#     vlines_x=[float, ["pass", []], None],
#     vlines_ymin=[float, ["pass", []], None],
#     vlines_ymax=[float, ["pass", []], None],
#     vlines_colors=[str, ["pass", []], None],
#     vlines_linestyles=[
#         str,
#         ["domain", ["auto", None, "", " ", "  "] + plotutils.LINE_LIST],
#         None,
#     ],
# )
def bar_stacked(
    input_ts="-",
    columns=None,
    start_date=None,
    end_date=None,
    clean=False,
    skiprows=None,
    index_type="datetime",
    names=None,
    ofilename="plot.png",
    xtitle="",
    ytitle="",
    title="",
    figsize="10,6.0",
    legend=None,
    legend_names=None,
    subplots=False,
    sharex=True,
    sharey=False,
    colors="auto",
    linestyles="auto",
    markerstyles=" ",
    bar_hatchstyles="auto",
    style="auto",
    logx=False,
    logy=False,
    xaxis="arithmetic",
    yaxis="arithmetic",
    xlim=None,
    ylim=None,
    secondary_y=False,
    mark_right=True,
    scatter_matrix_diagonal="kde",
    bootstrap_size=50,
    bootstrap_samples=500,
    norm_xaxis=False,
    norm_yaxis=False,
    lognorm_xaxis=False,
    lognorm_yaxis=False,
    xy_match_line="",
    grid=False,
    label_rotation=None,
    label_skip=1,
    force_freq=None,
    drawstyle="default",
    por=False,
    invert_xaxis=False,
    invert_yaxis=False,
    round_index=None,
    plotting_position="weibull",
    prob_plot_sort_values="descending",
    source_units=None,
    target_units=None,
    lag_plot_lag=1,
    plot_styles="bright",
    hlines_y=None,
    hlines_xmin=None,
    hlines_xmax=None,
    hlines_colors=None,
    hlines_linestyles="-",
    vlines_x=None,
    vlines_ymin=None,
    vlines_ymax=None,
    vlines_colors=None,
    vlines_linestyles="-",
    **kwds,
):
    r"""Plot data."""
    # Need to work around some old option defaults with the implementation of
    # mando
    legend = bool(legend == "" or legend == "True" or legend is None)

    type = "bar_stacked"

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator

    tsd = tsutils.common_kwds(
        input_ts,
        skiprows=skiprows,
        names=names,
        index_type=index_type,
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna="all",
        source_units=source_units,
        target_units=target_units,
        clean=clean,
        por=por,
    )

    tsd, lnames = plotutils.check(type, tsd, legend_names)

    # This is to help pretty print the frequency
    try:
        try:
            pltfreq = str(tsd.index.freq, "utf-8").lower()
        except TypeError:
            pltfreq = str(tsd.index.freq).lower()
        if pltfreq.split(" ")[0][1:] == "1":
            beginstr = 3
        else:
            beginstr = 1
        if pltfreq == "none":
            short_freq = ""
        else:
            # short freq string (day) OR (2 day)
            short_freq = "({})".format(pltfreq[beginstr:-1])
    except AttributeError:
        short_freq = ""

    if colors == "auto":
        colors = None
    else:
        colors = tsutils.make_list(colors)

    if linestyles == "auto":
        linestyles = plotutils.LINE_LIST
    else:
        linestyles = tsutils.make_list(linestyles)

    if bar_hatchstyles == "auto":
        bar_hatchstyles = plotutils.HATCH_LIST
    else:
        bar_hatchstyles = tsutils.make_list(bar_hatchstyles)

    if markerstyles == "auto":
        markerstyles = plotutils.MARKER_LIST
    else:
        markerstyles = tsutils.make_list(markerstyles)
        if markerstyles is None:
            markerstyles = " "

    if style != "auto":

        nstyle = tsutils.make_list(style)
        if len(nstyle) != len(tsd.columns):
            raise ValueError(
                tsutils.error_wrapper(
                    """
You have to have the same number of style strings as time-series to plot.
You supplied '{}' for style which has {} style strings,
but you have {} time-series.
""".format(
                        style, len(nstyle), len(tsd.columns)
                    )
                )
            )
        colors = []
        markerstyles = []
        linestyles = []
        for st in nstyle:
            colors.append(st[0])
            if len(st) == 1:
                markerstyles.append(" ")
                linestyles.append("-")
                continue
            if st[1] in plotutils.MARKER_LIST:
                markerstyles.append(st[1])
                try:
                    linestyles.append(st[2:])
                except IndexError:
                    linestyles.append(" ")
            else:
                markerstyles.append(" ")
                linestyles.append(st[1:])
    if linestyles is None:
        linestyles = [" "]
    else:
        linestyles = [" " if i in ["  ", None] else i for i in linestyles]
    markerstyles = [" " if i is None else i for i in markerstyles]

    if colors is not None:
        icolors = itertools.cycle(colors)
    else:
        icolors = None
    imarkerstyles = itertools.cycle(markerstyles)
    ilinestyles = itertools.cycle(linestyles)

    # Only for bar, barh, bar_stacked, and barh_stacked.
    ibar_hatchstyles = itertools.cycle(bar_hatchstyles)

    if (
        logx is True
        or logy is True
        or norm_xaxis is True
        or norm_yaxis is True
        or lognorm_xaxis is True
        or lognorm_yaxis is True
    ):
        warnings.warn(
            """
*
*   The --logx, --logy, --norm_xaxis, --norm_yaxis, --lognorm_xaxis, and
*   --lognorm_yaxis options are deprecated.
*
*   For --logx use --xaxis="log"
*   For --logy use --yaxis="log"
*   For --norm_xaxis use --type="norm_xaxis"
*   For --norm_yaxis use --type="norm_yaxis"
*   For --lognorm_xaxis use --type="lognorm_xaxis"
*   For --lognorm_yaxis use --type="lognorm_yaxis"
*
"""
        )

    if xaxis == "log":
        logx = True
    if yaxis == "log":
        logy = True

    xlim = plotutils.know_your_limits(xlim, axis=xaxis)
    ylim = plotutils.know_your_limits(ylim, axis=yaxis)

    plot_styles = tsutils.make_list(plot_styles) + ["no-latex"]
    style_loc = os.path.join(
        os.path.dirname(__file__), os.pardir, "SciencePlots_styles"
    )
    plot_styles = [
        os.path.join(style_loc, i + ".mplstyle")
        if os.path.exists(os.path.join(style_loc, i + ".mplstyle"))
        else i
        for i in plot_styles
    ]
    plt.style.use(plot_styles)

    figsize = tsutils.make_list(figsize, n=2)
    _, ax = plt.subplots(figsize=figsize)

    if type in ("bar", "bar_stacked", "barh", "barh_stacked"):
        stacked = False
        if type[-7:] == "stacked":
            stacked = True
        kind = "bar"
        if type[:4] == "barh":
            kind = "barh"
        if icolors is not None:
            c = [next(icolors) for i in range(len(tsd.columns))]
        else:
            c = None
        tsd.plot(
            ax=ax,
            kind=kind,
            legend=legend,
            stacked=stacked,
            logx=logx,
            logy=logy,
            xlim=xlim,
            ylim=ylim,
            figsize=figsize,
            linestyle=None,
            color=c,
        )

        hatches = [next(ibar_hatchstyles) for i in range(len(tsd.columns))]
        hatches = "".join(h * len(tsd.index) for h in hatches)
        for patch, hatch in zip(ax.patches, hatches):
            patch.set_hatch(hatch)

        freq = tsutils.asbestfreq(tsd, force_freq=force_freq).index.freqstr
        if freq is not None:
            if "A" in freq:
                endchar = 4
            elif "M" in freq:
                endchar = 7
            elif "D" in freq:
                endchar = 10
            elif "H" in freq:
                endchar = 13
            else:
                endchar = None
            nticklabels = []
            if kind == "bar":
                taxis = ax.xaxis
            else:
                taxis = ax.yaxis
            for index, i in enumerate(taxis.get_majorticklabels()):
                if index % label_skip:
                    nticklabels.append(" ")
                else:
                    nticklabels.append(i.get_text()[:endchar])
            taxis.set_ticklabels(nticklabels)
            plt.setp(taxis.get_majorticklabels(), rotation=label_rotation)
        if legend is True:
            plt.legend(loc="best")

    if hlines_y is not None:
        hlines_y = tsutils.make_list(hlines_y)
        hlines_xmin = tsutils.make_list(hlines_xmin)
        hlines_xmax = tsutils.make_list(hlines_xmax)
        hlines_colors = tsutils.make_list(hlines_colors)
        hlines_linestyles = tsutils.make_list(hlines_linestyles)
        nxlim = ax.get_xlim()
        if hlines_xmin is None:
            hlines_xmin = nxlim[0]
        if hlines_xmax is None:
            hlines_xmax = nxlim[1]
    if vlines_x is not None:
        vlines_x = tsutils.make_list(vlines_x)
        vlines_ymin = tsutils.make_list(vlines_ymin)
        vlines_ymax = tsutils.make_list(vlines_ymax)
        vlines_colors = tsutils.make_list(vlines_colors)
        vlines_linestyles = tsutils.make_list(vlines_linestyles)
        nylim = ax.get_ylim()
        if vlines_ymin is None:
            vlines_ymin = nylim[0]
        if vlines_ymax is None:
            vlines_ymax = nylim[1]
    if type in [
        "time",
        "xy",
        "bar",
        "bar_stacked",
        "histogram",
        "norm_xaxis",
        "lognorm_xaxis",
        "weibull_xaxis",
        "norm_yaxis",
        "lognorm_yaxis",
        "weibull_yaxis",
    ]:
        if hlines_y is not None:
            if type in ["norm_yaxis", "lognorm_yaxis", "weibull_yaxis"]:
                hlines_y = ppf(tsutils.make_list(hlines_y))
            plt.hlines(
                hlines_y,
                hlines_xmin,
                hlines_xmax,
                colors=hlines_colors,
                linestyles=hlines_linestyles,
            )
        if vlines_x is not None:
            if type in ["norm_xaxis", "lognorm_xaxis", "weibull_xaxis"]:
                vlines_x = ppf(tsutils.make_list(vlines_x))
            plt.vlines(
                vlines_x,
                vlines_ymin,
                vlines_ymax,
                colors=vlines_colors,
                linestyles=vlines_linestyles,
            )

    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    if invert_xaxis is True:
        plt.gca().invert_xaxis()
    if invert_yaxis is True:
        plt.gca().invert_yaxis()

    plt.grid(grid)

    plt.title(title)
    plt.tight_layout()
    if ofilename is not None:
        plt.savefig(ofilename)
    return plt


bar_stacked.__doc__ = bar_stacked_cli.__doc__
