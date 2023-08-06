# -*- coding: utf-8 -*-
"""Collection of functions for the manipulation of time series."""

from __future__ import absolute_import, division, print_function

import warnings

import mando
from mando.rst_text_formatter import RSTHelpFormatter
from tstoolbox import tsutils

from .. import plotutils

warnings.filterwarnings("ignore")


@mando.command("autocorrelation", formatter_class=RSTHelpFormatter, doctype="numpy")
@tsutils.doc(plotutils.ldocstrings)
def autocorrelation_cli(
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
    xlim=None,
    ylim=None,
    grid=False,
    xlabel_rotation=0,
    ylabel_rotation=0,
    por=False,
    round_index=None,
    source_units=None,
    target_units=None,
    plot_styles="bright",
):
    r"""Autocorrelation plot.

    The "autocorrelation" creates an autocorrelation plot.

    The horizontal lines in the plot correspond to 95% and 99% confidence
    bands.

    The dashed line is 99% confidence band.

    Only available for a single time-series.

    {yone}

    Parameters
    ----------
    {input_ts}
    {columns}
    {start_date}
    {end_date}
    {clean}
    {skiprows}
    {index_type}
    {names}
    {ofilename}
    {xtitle}
    {ytitle}
    {title}
    {figsize}
    {xlim}
    {ylim}
    {grid}
    {xlabel_rotation}
    {ylabel_rotation}
    {por}
    {round_index}
    {source_units}
    {target_units}
    {plot_styles}
    """
    plt = autocorrelation(
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
        xlim=xlim,
        ylim=ylim,
        grid=grid,
        xlabel_rotation=xlabel_rotation,
        ylabel_rotation=ylabel_rotation,
        por=por,
        round_index=round_index,
        source_units=source_units,
        target_units=target_units,
        plot_styles=plot_styles,
    )


# @tsutils.validator(
#     ofilename=[str, ["pass", []], 1],
#     type=[str, ["domain", ["autocorrelation",],], 1,],
#     xtitle=[str, ["pass", []], 1],
#     ytitle=[str, ["pass", []], 1],
#     title=[str, ["pass", []], 1],
#     figsize=[float, ["range", [0, None]], 2],
#     subplots=[bool, ["domain", [True, False]], 1],
#     sharex=[bool, ["domain", [True, False]], 1],
#     sharey=[bool, ["domain", [True, False]], 1],
#     colors=[str, ["pass", []], None],
#     linestyles=[str, ["domain", ["auto", None, "", " ", "  "] + plotutils.LINE_LIST], None],
#     markerstyles=[str, ["domain", ["auto", None, "", " ", "  "] + plotutils.MARKER_LIST], None],
#     style=[str, ["pass", []], None],
#     xlim=[float, ["pass", []], 2],
#     ylim=[float, ["pass", []], 2],
#     secondary_y=[bool, ["domain", [True, False]], 1],
#     mark_right=[bool, ["domain", [True, False]], 1],
#     bootstrap_size=[int, ["range", [0, None]], 1],
#     grid=[bool, ["domain", [True, False]], 1],
#     label_rotation=[float, ["pass", []], 1],
#     drawstyle=[str, ["pass", []], 1],
#     por=[bool, ["domain", [True, False]], 1],
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
# )
@tsutils.transform_args(figsize=tsutils.make_list)
def autocorrelation(
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
    xlim=None,
    ylim=None,
    grid=False,
    xlabel_rotation=0,
    ylabel_rotation=0,
    por=False,
    round_index=None,
    source_units=None,
    target_units=None,
    plot_styles="bright",
    **kwds,
):
    r"""Plot data."""
    type = "autocorrelation"

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

    tsd, _ = plotutils.check(type, tsd, [""])

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
            short_freq = f"({pltfreq[beginstr:-1]})"
    except AttributeError:
        short_freq = ""

    plt.style.use(plot_styles)

    figsize = tsutils.make_list(figsize, n=2)
    _, ax = plt.subplots(figsize=figsize)

    from pandas.plotting import autocorrelation_plot

    autocorrelation_plot(tsd, ax=ax)
    xtitle = xtitle or f"Time Lag {short_freq}"

    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    plt.xticks(rotation=xlabel_rotation)
    plt.yticks(rotation=ylabel_rotation)

    plt.grid(grid)

    plt.title(title)

    plt.xlim(xlim)
    plt.ylim(ylim)

    plt.tight_layout()
    if ofilename is not None:
        plt.savefig(ofilename)
    return plt


autocorrelation.__doc__ = autocorrelation_cli.__doc__
