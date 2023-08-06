# -*- coding: utf-8 -*-
"""Collection of functions for the manipulation of time series."""

from __future__ import absolute_import, division, print_function

import itertools
import os
import warnings

import mando
import numpy as np
import sklearn
from mando.rst_text_formatter import RSTHelpFormatter
from tstoolbox import tsutils

from .. import plotutils

warnings.filterwarnings("ignore")


@mando.command("kde_time", formatter_class=RSTHelpFormatter, doctype="numpy")
@tsutils.doc(plotutils.ldocstrings)
def kde_time_cli(
    input_ts="-",
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
    style="auto",
    logx=False,
    logy=False,
    xaxis="arithmetic",
    yaxis="arithmetic",
    xlim=None,
    ylim=None,
    secondary_y=False,
    mark_right=True,
    norm_xaxis=False,
    norm_yaxis=False,
    lognorm_xaxis=False,
    lognorm_yaxis=False,
    xy_match_line="",
    grid=False,
    label_rotation=None,
    label_skip=1,
    drawstyle="default",
    por=False,
    force_freq=None,
    invert_xaxis=False,
    invert_yaxis=False,
    columns=None,
    start_date=None,
    end_date=None,
    clean=False,
    skiprows=None,
    index_type="datetime",
    names=None,
    source_units=None,
    target_units=None,
    round_index=None,
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
    r"""A time-series plot with a kernel density estimation (KDE) plot.

    This plot is an estimation of the probability density function based on the
    data called kernel density estimation (KDE) combined with a time-series
    plot.

    Parameters
    ----------
    {input_ts}

    ofilename : str
        [optional, defaults to 'plot.png']

        Output filename for the plot.  Extension defines
        the type, for example 'filename.png' will create a PNG file.

        If used within Python, and `ofilename` is None will return the
        Matplotlib figure that can then be changed or added to as
        needed.

    xtitle : str
        [optional, default depends on ``type``]

        Title of x-axis.

    ytitle : str
        [optional, default depends on ``type``]

        Title of y-axis.

    title : str
        [optional, defaults to '']

        Title of chart.

    figsize : str
        [optional, defaults to '10,6.5']

        The 'width,height' of plot in inches.

    legend
        [optional, defaults to True]

        Whether to display the legend.

    legend_names : str
        [optional, defaults to None]

        Legend would normally use the time-series names associated with
        the input data.  The 'legend_names' option allows you to
        override the names in the data set.  You must supply a comma
        separated list of strings for each time-series in the data set.

    subplots
        [optional, defaults to False]

        Make separate subplots for each time series.

    sharex
        [optional, default to True]

        In case subplots=True, share x axis.

    sharey
        [optional, default to False]

        In case subplots=True, share y axis.

    colors
        [optional, default is 'auto']

        The default 'auto' will cycle through matplotlib colors in the chosen
        style.

        At the command line supply a comma separated matplotlib
        color codes, or within Python a list of color code strings.

        Can identify colors in four different ways.

        1. Use 'CN' where N is a number from 0 to 9 that gets the Nth color
        from the current style.

        2. Single character code from the table below.

        +------+---------+
        | Code | Color   |
        +======+=========+
        | b    | blue    |
        +------+---------+
        | g    | green   |
        +------+---------+
        | r    | red     |
        +------+---------+
        | c    | cyan    |
        +------+---------+
        | m    | magenta |
        +------+---------+
        | y    | yellow  |
        +------+---------+
        | k    | black   |
        +------+---------+

        3. Number between 0 and 1 that represents the level of gray, where 0 is
        white an 1 is black.

        4. Any of the HTML color names.

        +------------------+
        | HTML Color Names |
        +==================+
        | red              |
        +------------------+
        | burlywood        |
        +------------------+
        | chartreuse       |
        +------------------+
        | ...etc.          |
        +------------------+

        Color reference:
        http://matplotlib.org/api/colors_api.html

    linestyles
        [optional, default to 'auto']

        If 'auto' will iterate through the available matplotlib line types.
        Otherwise on the command line a comma separated list, or a list of
        strings if using the Python API.

        To not display lines use a space (' ') as the linestyle code.

        Separated 'colors', 'linestyles', and 'markerstyles' instead of using
        the 'style' keyword.

        +---------+--------------+
        | Code    | Lines        |
        +=========+==============+
        | ``-``   | solid        |
        +---------+--------------+
        | --      | dashed       |
        +---------+--------------+
        | -.      | dash_dot     |
        +---------+--------------+
        | :       | dotted       |
        +---------+--------------+
        | None    | draw nothing |
        +---------+--------------+
        | ' '     | draw nothing |
        +---------+--------------+
        | ''      | draw nothing |
        +---------+--------------+

        Line reference:
        http://matplotlib.org/api/artist_api.html

    markerstyles
        [optional, default to ' ']

        The default ' ' will not plot a marker.  If 'auto' will iterate through
        the available matplotlib marker types.  Otherwise on the command line
        a comma separated list, or a list of strings if using the Python API.

        Separated 'colors', 'linestyles', and 'markerstyles' instead of using
        the 'style' keyword.

        +-------+----------------+
        | Code  | Markers        |
        +=======+================+
        | .     | point          |
        +-------+----------------+
        | o     | circle         |
        +-------+----------------+
        | v     | triangle down  |
        +-------+----------------+
        | ^     | triangle up    |
        +-------+----------------+
        | <     | triangle left  |
        +-------+----------------+
        | >     | triangle right |
        +-------+----------------+
        | 1     | tri_down       |
        +-------+----------------+
        | 2     | tri_up         |
        +-------+----------------+
        | 3     | tri_left       |
        +-------+----------------+
        | 4     | tri_right      |
        +-------+----------------+
        | 8     | octagon        |
        +-------+----------------+
        | s     | square         |
        +-------+----------------+
        | p     | pentagon       |
        +-------+----------------+
        | ``*`` | star           |
        +-------+----------------+
        | h     | hexagon1       |
        +-------+----------------+
        | H     | hexagon2       |
        +-------+----------------+
        | ``+`` | plus           |
        +-------+----------------+
        | x     | x              |
        +-------+----------------+
        | D     | diamond        |
        +-------+----------------+
        | d     | thin diamond   |
        +-------+----------------+
        | _     | hlines_y       |
        +-------+----------------+
        | None  | nothing        |
        +-------+----------------+
        | ' '   | nothing        |
        +-------+----------------+
        | ''    | nothing        |
        +-------+----------------+

        Marker reference:
        http://matplotlib.org/api/markers_api.html

    style
        [optional, default is None]

        Still available, but if None is replaced by 'colors', 'linestyles', and
        'markerstyles' options.  Currently the 'style' option will override the
        others.

        Comma separated matplotlib style strings per time-series.  Just
        combine codes in 'ColorMarkerLine' order, for example 'r*--' is
        a red dashed line with star marker.

    logx
        DEPRECATED: use '--xaxis="log"' instead.

    logy
        DEPRECATED: use '--yaxis="log"' instead.

    xlim
        [optional, default is based on range of x values]

        Comma separated lower and upper limits for the x-axis of the
        plot.  For example, '--xlim 1,1000' would limit the plot from
        1 to 1000, where '--xlim ,1000' would base the lower limit on
        the data and set the upper limit to 1000.

    ylim
        [optional, default is based on range of y values]

        Comma separated lower and upper limits for the y-axis of the
        plot.  See `xlim` for examples.

    xaxis : str
        [optional, default is 'arithmetic']

        Defines the type of the xaxis.  One of 'arithmetic', 'log'.

    yaxis : str
        [optional, default is 'arithmetic']

        Defines the type of the yaxis.  One of 'arithmetic', 'log'.

    secondary_y
        [optional, default is False]

        Whether to plot on the secondary y-axis. If a list/tuple, which
        time-series to plot on secondary y-axis.

    mark_right
        [optional, default is True]

        When using a secondary_y axis, should the legend label the axis of the
        various time-series automatically.

    norm_xaxis
        DEPRECATED: use '--type="norm_xaxis"' instead.

    norm_yaxis
        DEPRECATED: use '--type="norm_yaxis"' instead.

    lognorm_xaxis
        DEPRECATED: use '--type="lognorm_xaxis"' instead.

    lognorm_yaxis
        DEPRECATED: use '--type="lognorm_yaxis"' instead.

    xy_match_line : str
        [optional, defaults is '']

        Will add a match line where x == y. Set to a line style code.

    grid
        [optional, default is False]

        Whether to plot grid lines on the major ticks.

    label_rotation : int
        [optional]

        Rotation for major labels for bar plots.

    label_skip : int
        [optional]

        Skip for major labels for bar plots.

    drawstyle : str
        [optional, default is 'default']

        'default' connects the points with lines. The
        steps variants produce step-plots. 'steps' is equivalent to 'steps-pre'
        and is maintained for backward-compatibility.

        ACCEPTS::

         ['default' | 'steps' | 'steps-pre' | 'steps-mid' | 'steps-post']

    por
        [optional]

        Plot from first good value to last good value.  Strips NANs
        from beginning and end.

    {force_freq}

    invert_xaxis
        [optional, default is False]

        Invert the x-axis.

    invert_yaxis
        [optional, default is False]

        Invert the y-axis.

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

    plot_styles: str
        [optional, default is "default"]

        Set the style of the plot.  One or more of Matplotlib styles "classic",
        "Solarize_Light2", "bmh", "dark_background", "fast", "fivethirtyeight",
        "ggplot", "grayscale", "seaborn", "seaborn-bright",
        "seaborn-colorblind", "seaborn-dark", "seaborn-dark-palette",
        "seaborn-darkgrid", "seaborn-deep", "seaborn-muted",
        "seaborn-notebook", "seaborn-paper", "seaborn-pastel",
        "seaborn-poster", "seaborn-talk", "seaborn-ticks", "seaborn-white",
        "seaborn-whitegrid", "tableau-colorblind10", and

        SciencePlots styles "science", "grid", "ieee", "scatter", "notebook",
        "high-vis", "bright", "vibrant", "muted", and "retro".

        If multiple styles then each over rides some or all of the
        characteristics of the previous.

        Color Blind Appropriate Styles

        The styles "seaborn-colorblind", "tableau-colorblind10", "bright",
        "vibrant", and "muted" are all styles that are setup to be able to be
        distinguished by someone with color blindness.

        Black, White, and Gray Styles

        The "ieee" style is appropriate for black, white, and gray, however the
        "ieee" also will change the chart size to fit in a column of the "IEEE"
        journal.

        The "grayscale" is another style useful for photo-copyable black,
        white, nd gray.

        Matplotlib styles:
            https://matplotlib.org/3.3.1/gallery/style_sheets/style_sheets_reference.html

        SciencePlots styles:
            https://github.com/garrettj403/SciencePlots

    hlines_y:
        [optional, defaults to None]

        Number or list of y values where to place a horizontal line.

    hlines_xmin:
        [optional, defaults to None]

        List of minimum x values to start the horizontal line.  If a list must
        be same length as `hlines_y`.  If a single number will be used as the
        minimum x values for all horizontal lines.  A missing value or None
        will start at the minimum x value for the entire plot.

    hlines_xmax:
        [optional, defaults to None]

        List of maximum x values to end each horizontal line.  If a list must
        be same length as `hlines_y`.  If a single number will be the maximum
        x value for all horizontal lines.  A missing value or None will end at
        the maximum x value for the entire plot.

    hlines_colors:
        [optional, defaults to None]

        List of colors for the horizontal lines.  If a single color then will
        be used as the color for all horizontal lines.  If a list must be same
        length as `hlines_y`.  If None will take from the color pallette in the
        current plot style.

    hlines_linestyles:
        [optional, defaults to None]

        List of linestyles for the horizontal lines.  If a single linestyle
        then will be used as the linestyle for all horizontal lines.  If a list
        must be same length as `hlines_y`.  If None will take for the standard
        linestyles list.

    vlines_x:
        [optional, defaults to None]

        List of x values where to place a vertical line.

    vlines_ymin:
        [optional, defaults to None]

        List of minimum y values to start the vertical line.  If a list must be
        same length as `vlines_x`.  If a single number will be used as the
        minimum x values for all vertical lines.  A missing value or None will
        start at the minimum x value for the entire plot.

    vlines_ymax:
        [optional, defaults to None]

        List of maximum x values to end each vertical line.  If a list must be
        same length as `vlines_x`.  If a single number will be the maximum
        x value for all vertical lines.  A missing value or None will end at
        the maximum x value for the entire plot.

    vlines_colors:
        [optional, defaults to None]

        List of colors for the vertical lines.  If a single color then will be
        used as the color for all vertical lines.  If a list must be same
        length as `vlines_x`.  If None will take from the color pallette in the
        current plot style.

    vlines_linestyles:
        [optional, defaults to None]

        List of linestyles for the vertical lines.  If a single linestyle then
        will be used as the linestyle for all vertical lines.  If a list must
        be same length as `vlines_x`.  If None will take for the standard
        linestyles list.
    """
    plt = kde_time(
        input_ts=input_ts,
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
        columns=columns,
        colors=colors,
        linestyles=linestyles,
        markerstyles=markerstyles,
        style=style,
        logx=logx,
        logy=logy,
        xlim=xlim,
        ylim=ylim,
        xaxis=xaxis,
        yaxis=yaxis,
        secondary_y=secondary_y,
        mark_right=mark_right,
        start_date=start_date,
        end_date=end_date,
        clean=clean,
        skiprows=skiprows,
        index_type=index_type,
        names=names,
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
        source_units=source_units,
        target_units=target_units,
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
#     type=[str, ["domain", ["kde_time",],], 1,],
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
#     style=[str, ["pass", []], None],
#     xlim=[float, ["pass", []], 2],
#     ylim=[float, ["pass", []], 2],
#     xaxis=[str, ["domain", ["arithmetic", "log"]], 1],
#     yaxis=[str, ["domain", ["arithmetic", "log"]], 1],
#     secondary_y=[bool, ["domain", [True, False]], 1],
#     mark_right=[bool, ["domain", [True, False]], 1],
#     xy_match_line=[str, ["pass", []], 1],
#     grid=[bool, ["domain", [True, False]], 1],
#     label_rotation=[float, ["pass", []], 1],
#     label_skip=[int, ["range", [1, None]], 1],
#     drawstyle=[str, ["pass", []], 1],
#     por=[bool, ["domain", [True, False]], 1],
#     invert_xaxis=[bool, ["domain", [True, False]], 1],
#     invert_yaxis=[bool, ["domain", [True, False]], 1],
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
def kde_time(
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
    style="auto",
    logx=False,
    logy=False,
    xaxis="arithmetic",
    yaxis="arithmetic",
    xlim=None,
    ylim=None,
    secondary_y=False,
    mark_right=True,
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
    source_units=None,
    target_units=None,
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

    _, (ax0, ax1) = plt.subplots(
        nrows=1,
        ncols=2,
        sharey=True,
        figsize=figsize,
        gridspec_kw={"width_ratios": [1, 4]},
    )
    tsd.plot(
        legend=legend,
        subplots=subplots,
        sharex=sharex,
        sharey=sharey,
        style=None,
        logx=logx,
        logy=logy,
        xlim=xlim,
        ylim=ylim,
        secondary_y=secondary_y,
        mark_right=mark_right,
        figsize=figsize,
        drawstyle=drawstyle,
        ax=ax1,
    )
    for index, line in enumerate(ax1.lines):
        if icolors is not None:
            c = next(icolors)
        else:
            c = None
        if imarkerstyles is not None:
            m = next(imarkerstyles)
        else:
            m = None
        if ilinestyles is not None:
            l = next(ilinestyles)
        else:
            l = None
        if c is not None:
            plt.setp(line, color=c)
        plt.setp(line, marker=m)
        plt.setp(line, linestyle=l)
    xtitle = xtitle or "Time"
    ylimits = ax1.get_ylim()
    ny = np.linspace(ylimits[0], ylimits[1], 1000)

    # reset to beginning of iterator
    if icolors is not None:
        icolors = itertools.cycle(colors)
    else:
        icolors = None
    imarkerstyles = itertools.cycle(markerstyles)
    ilinestyles = itertools.cycle(linestyles)
    for col in range(len(tsd.columns)):
        xvals = tsd.iloc[:, col].dropna().values
        pdf = sklearn.neighbors.KernelDensity().fit(np.array(xvals).reshape(-1, 1))
        if icolors is not None:
            c = next(icolors)
        ax0.plot(
            pdf.score_samples(np.array(ny).reshape(-1, 1)),
            ny,
            linestyle=next(ilinestyles),
            color=c,
            marker=next(imarkerstyles),
            label=tsd.columns[col],
            drawstyle=drawstyle,
        )
    ax0.set(xlabel="Probability Density", ylabel=ytitle)

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

        maxt = max(nxlim[1], nylim[1])
        mint = min(nxlim[0], nylim[0])
        ax.plot([mint, maxt], [mint, maxt], xymsty, zorder=1)
        ax.set_ylim(nylim)
        ax.set_xlim(nxlim)

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


kde_time.__doc__ = kde_time_cli.__doc__
