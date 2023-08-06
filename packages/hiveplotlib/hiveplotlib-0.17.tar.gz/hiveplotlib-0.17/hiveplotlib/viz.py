# Gary Koplik
# gary<dot>koplik<at>geomdata<dot>com
# August, 2020
# viz.py

"""
Viz functions to be called on ``hiveplotlib.HivePlot`` or ``hiveplotlib.P2CP`` instances.
"""

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
from hiveplotlib.utils import polar2cartesian
import warnings


def axes_viz_mpl(instance: "HivePlot instance" or "P2CP instance",
                 fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                 buffer: float = 0.1, show_axes_labels: bool = True, axes_labels_buffer: float = 1.1,
                 axes_labels_fontsize: int = 16, figsize: tuple = (10, 10), center_plot: bool = True,
                 mpl_axes_off: bool = True, **axes_kwargs):
    """
    ``matplotlib`` visualization of axes in a ``HivePlot`` or ``P2CP`` instance.

    :param instance: ``HivePlot`` or ``P2CP`` instance for which we want to draw axes.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        axis. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g setting ``buffer`` to 0.1 will find
        the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``.
    :param show_axes_labels: whether to label the hive plot axes in the figure (uses ``Axis.long_name`` for each
        ``Axis``.)
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for axes labels.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that ``Axis`` instances
        can be drawn around.
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param axes_kwargs: additional params that will be applied to all axes. Note, these are kwargs that affect
        a ``plt.plot()`` call.
    :return: ``matplotlib`` figure, axis.
    """

    if "HivePlot" in instance.__repr__():
        hive_plot = instance.copy()
        if len(hive_plot.axes.values()) == 0:
            warnings.warn(
                "No axes have been added yet. " +
                "Axes can be added by running `HivePlot.add_axes()`",
                stacklevel=2)
            return None
    elif "P2CP" in instance.__repr__():
        hive_plot = instance._hiveplot.copy()
        if len(hive_plot.axes.values()) == 0:
            warnings.warn(
                "No axes have been set yet. " +
                "Nodes can be placed on axes by running `P2CP.set_axes()`",
                stacklevel=2)
            return None
    else:
        raise NotImplementedError("Can only handle `HivePlot` and `P2CP` instances")

    # allow for plotting onto specified figure, axis
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # some default kwargs for the axes
    if 'c' not in axes_kwargs:
        axes_kwargs['c'] = 'black'
    if 'alpha' not in axes_kwargs:
        axes_kwargs['alpha'] = 0.5

    for axis in hive_plot.axes.values():
        to_plot = np.vstack((axis.start, axis.end))
        ax.plot(to_plot[:, 0], to_plot[:, 1], **axes_kwargs)

    if center_plot:
        plt.axis("equal")
        # center plot at (0, 0)
        max_radius = max([axis.polar_end for axis in hive_plot.axes.values()])
        # throw in a minor buffer
        buffer_radius = buffer * max_radius
        max_radius += buffer_radius

        ax.set_xlim(-max_radius, max_radius)
        ax.set_ylim(-max_radius, max_radius)

    if show_axes_labels:
        label_axes_mpl(instance=hive_plot, fig=fig, ax=ax, center_plot=False,
                       axes_labels_buffer=axes_labels_buffer, axes_labels_fontsize=axes_labels_fontsize)
    if mpl_axes_off:
        ax.axis("off")

    return fig, ax


def label_axes_mpl(instance: "HivePlot instance" or "P2CP instance",
                   fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                   axes_labels_buffer: float = 1.1, axes_labels_fontsize: int = 16, buffer: float = 0.1,
                   figsize: tuple = (10, 10), center_plot: bool = True, mpl_axes_off: bool = True):
    """
    ``matplotlib`` visualization of axis labels in a ``HivePlot`` or ``P2CP`` instance. For ``HivePlot`` instances,
    each axis' ``long_name`` attribute will be used. For ``P2CP`` instances, column names in the ``data`` attribute
    will be used.

    :param instance: ``HivePlot`` or ``P2CP`` instance for which we want to draw nodes.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        axis. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for axes labels.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g setting ``buffer`` to 0.1 will find
        the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that ``Axis`` instances
        can be drawn around.
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :return: ``matplotlib`` figure, axis.
    """

    if "HivePlot" in instance.__repr__():
        hive_plot = instance.copy()
        if len(hive_plot.axes.values()) == 0:
            warnings.warn(
                "No axes have been added yet. " +
                "Axes can be added by running `HivePlot.add_axes()`",
                stacklevel=2)
            return None
    elif "P2CP" in instance.__repr__():
        hive_plot = instance._hiveplot.copy()
        if len(hive_plot.axes.values()) == 0:
            warnings.warn(
                "No axes have been set yet. " +
                "Nodes can be placed on axes by running `P2CP.set_axes()`",
                stacklevel=2)
            return None
    else:
        raise NotImplementedError("Can only handle `HivePlot` and `P2CP` instances")

    # allow for plotting onto specified figure, axis
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    for axis in hive_plot.axes.values():
        # choose horizontal and vertical alignment based on axis angle in [0, 360)
        # range in each direction from 0, 180 to specify horizontal alignment
        horizontal_angle_span = 60
        if axis.angle >= 360 - horizontal_angle_span or axis.angle <= 0 + horizontal_angle_span:
            horizontalalignment = "left"
        elif 180 + horizontal_angle_span >= axis.angle >= 180 - horizontal_angle_span:
            horizontalalignment = "right"
        else:
            horizontalalignment = "center"

        # range in each direction from 90, 270 to specify vertical alignment
        vertical_angle_span = 60
        if 90 + vertical_angle_span >= axis.angle >= 90 - vertical_angle_span:
            verticalalignment = "bottom"
        elif 270 - vertical_angle_span <= axis.angle <= 270 + vertical_angle_span:
            verticalalignment = "top"
        else:
            verticalalignment = "center"

        x, y = polar2cartesian(axes_labels_buffer * axis.polar_end, axis.angle)
        ax.text(x, y, axis.long_name, fontsize=axes_labels_fontsize,
                horizontalalignment=horizontalalignment, verticalalignment=verticalalignment)

    if center_plot:
        plt.axis("equal")
        # center plot at (0, 0)
        max_radius = max([axis.polar_end for axis in hive_plot.axes.values()])
        # throw in a minor buffer
        buffer_radius = buffer * max_radius
        max_radius += buffer_radius

        ax.set_xlim(-max_radius, max_radius)
        ax.set_ylim(-max_radius, max_radius)

    if mpl_axes_off:
        ax.axis("off")

    return fig, ax


def node_viz_mpl(instance: "HivePlot instance" or "P2CP instance",
                 fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                 figsize: tuple = (10, 10), center_plot: bool = True, buffer: float = 0.1,
                 mpl_axes_off: bool = True, **scatter_kwargs):
    """
    ``matplotlib`` visualization of nodes in a ``HivePlot`` or ``P2CP`` instance that have been placed on its axes.

    :param instance: ``HivePlot`` or ``P2CP`` instance for which we want to draw nodes.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        axis. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that ``Axis`` instances
        can be drawn around.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g setting ``buffer`` to 0.1 will find
        the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``.
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param scatter_kwargs: additional params that will be applied to all hive plot nodes. Note, these are kwargs that
        affect a ``plt.scatter()`` call.
    :return: ``matplotlib`` figure, axis.
    """

    if "HivePlot" in instance.__repr__():
        hive_plot = instance.copy()
        is_hive_plot = True
    elif "P2CP" in instance.__repr__():
        hive_plot = instance._hiveplot.copy()
        is_hive_plot = False
    else:
        raise NotImplementedError("Can only handle `HivePlot` and `P2CP` instances")

    # allow for plotting onto specified figure, axis
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # some default kwargs for the axes
    if 'c' not in scatter_kwargs:
        scatter_kwargs['c'] = 'black'
    if 'alpha' not in scatter_kwargs:
        scatter_kwargs['alpha'] = 0.8
    if 's' not in scatter_kwargs:
        scatter_kwargs["s"] = 20

    # p2cp warning only happens when axes don't exist
    if len(hive_plot.axes.values()) == 0:
        if not is_hive_plot:
            warnings.warn(
                "No axes have been set yet, thus no nodes have been placed on axes. " +
                "Nodes can be placed on axes by running `P2CP.set_axes()`",
                stacklevel=2)
            return None
    else:
        for axis in hive_plot.axes.values():
            to_plot = axis.node_placements.values[:, :2]
            if to_plot.shape[0] > 0:
                ax.scatter(to_plot[:, 0], to_plot[:, 1], **scatter_kwargs)
            else:
                if is_hive_plot:
                    warnings.warn(
                        "At least one of your axes has no nodes placed on it yet. " +
                        "Nodes can be placed on axes by running `HivePlot.place_nodes_on_axis()`",
                        stacklevel=2)

        if center_plot:
            plt.axis("equal")
            # center plot at (0, 0)
            max_radius = max([a.polar_end for a in hive_plot.axes.values()])
            # throw in a minor buffer
            buffer_radius = buffer * max_radius
            max_radius += buffer_radius

            ax.set_xlim(-max_radius, max_radius)
            ax.set_ylim(-max_radius, max_radius)
    if mpl_axes_off:
        ax.axis("off")

    return fig, ax


def edge_viz_mpl(instance: "HivePlot instance" or "P2CP instance",
                 fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                 figsize: tuple = (10, 10), mpl_axes_off: bool = True, **edge_kwargs):
    """
    ``matplotlib`` visualization of constructed edges in a ``HivePlot`` or ``P2CP`` instance.

    :param instance: ``HivePlot`` or ``P2CP`` instance for which we want to draw edges.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        axis. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param edge_kwargs: additional params that will be applied to all edges on all axes (but kwargs specified beforehand
        in ``HivePlot.connect_axes()`` / ``P2CP.build_edges`` or ``HivePlot.add_edge_kwargs()`` /
        ``P2CP.add_edge_kwargs()`` will take priority).
        To overwrite previously set kwargs, see ``HivePlot.add_edge_kwargs()`` / ``P2CP.add_edge_kwargs()`` for more.
        Note, these are kwargs that affect a ``plt.plot()`` call.
    :return: ``matplotlib`` figure, axis.
    """

    if "HivePlot" in instance.__repr__():
        hive_plot = instance.copy()
        is_hive_plot = True
    elif "P2CP" in instance.__repr__():
        hive_plot = instance._hiveplot.copy()
        is_hive_plot = False
    else:
        raise NotImplementedError("Can only handle `HivePlot` and `P2CP` instances")

    # make sure edges have already been created
    if len(list(hive_plot.edges.keys())) == 0:
        if is_hive_plot:
            warnings.warn(
                "Your `HivePlot` instance does not have any specified edges yet. " +
                "Edges can be created for plotting by running `HivePlot.connect_axes()`",
                stacklevel=2)
            return None
        else:
            warnings.warn(
                "Your `P2CP` instance does not have any specified edges yet. " +
                "Edges can be created for plotting by running `P2CP.build_edges()`",
                stacklevel=2)
            return None

    # allow for plotting onto specified figure, axis
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # p2cp warnings only need to happen once per tag
    #  because all axes behave in unison
    already_warned_p2cp_tags = []

    for a0 in hive_plot.edges.keys():
        for a1 in hive_plot.edges[a0].keys():
            for tag in hive_plot.edges[a0][a1].keys():
                temp_edge_kwargs = edge_kwargs.copy()

                # only run plotting of edges that exist
                if "curves" in hive_plot.edges[a0][a1][tag]:

                    # create edge_kwargs key if needed
                    if "edge_kwargs" not in hive_plot.edges[a0][a1][tag]:
                        hive_plot.edges[a0][a1][tag]["edge_kwargs"] = dict()

                    # don't use kwargs specified in this function call if already specified
                    for k in list(temp_edge_kwargs.keys()):
                        if k in hive_plot.edges[a0][a1][tag]["edge_kwargs"]:
                            if is_hive_plot:
                                warnings.warn(f"Specified kwarg {k} but already set as kwarg for edge tag {tag} "
                                              f"going from edges {a0} to {a1}. Preserving kwargs already set.\n"
                                              "(These kwargs can be changed using the `add_edge_kwargs()` method "
                                              "for your `HivePlot` instance)", stacklevel=2)
                            else:
                                # only warn once per tag over all axes
                                if tag not in already_warned_p2cp_tags:
                                    warnings.warn(f"Specified kwarg {k} but already set as kwarg for edge tag {tag}. "
                                                  f"Preserving kwargs already set.\n"
                                                  "(These kwargs can be changed using the `add_edge_kwargs()` method "
                                                  "for your `P2CP` instance)", stacklevel=2)
                                    already_warned_p2cp_tags.append(tag)
                            del temp_edge_kwargs[k]

                    # some default kwargs for the axes if not specified anywhere
                    if 'c' not in hive_plot.edges[a0][a1][tag]["edge_kwargs"] and 'c' not in temp_edge_kwargs:
                        temp_edge_kwargs['c'] = 'black'
                    if 'alpha' not in hive_plot.edges[a0][a1][tag]["edge_kwargs"] and 'alpha' not in temp_edge_kwargs:
                        temp_edge_kwargs['alpha'] = 0.5

                    # grab the requested array of discretized curves
                    edge_arr = hive_plot.edges[a0][a1][tag]["curves"]
                    ax.plot(edge_arr[:, 0], edge_arr[:, 1],
                            **hive_plot.edges[a0][a1][tag]["edge_kwargs"], **temp_edge_kwargs)

    if mpl_axes_off:
        ax.axis("off")

    return fig, ax


def hive_plot_viz_mpl(hive_plot: "HivePlot instance",
                      fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                      figsize: tuple = (10, 10), center_plot: bool = True, buffer: float = 0.1,
                      show_axes_labels: bool = True, axes_labels_buffer: float = 1.1,
                      axes_labels_fontsize: int = 16, mpl_axes_off: bool = True,
                      node_kwargs: dict or None = None, axes_kwargs: dict or None = None, **edge_kwargs):
    """
    Default ``matplotlib`` visualization of a ``HivePlot`` instance.

    :param hive_plot: ``HivePlot`` instance for which we want to draw edges.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        axis. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that ``Axis`` instances
        can be drawn around.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g setting ``buffer`` to 0.1 will find
        the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``.
    :param show_axes_labels: whether to label the hive plot axes in the figure (uses ``Axis.long_name`` for each
        ``Axis``.)
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for hive plot axes labels.
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param node_kwargs: additional params that will be applied to all hive plot nodes. Note, these are kwargs that
        affect a ``plt.scatter()`` call.
    :param axes_kwargs: additional params that will be applied to all axes. Note, these are kwargs that affect
        a ``plt.plot()`` call.
    :param edge_kwargs: additional params that will be applied to all edges on all axes (but kwargs specified beforehand
        in ``HivePlot.connect_axes()`` or ``HivePlot.add_edge_kwargs()`` will take priority).
        To overwrite previously set kwargs, see ``HivePlot.add_edge_kwargs()`` for more. Note, these are kwargs that
        affect a ``plt.plot()`` call.
    :return: ``matplotlib`` figure, axis.
    """

    if node_kwargs is None:
        node_kwargs = dict()

    if axes_kwargs is None:
        axes_kwargs = dict()

    fig, ax = axes_viz_mpl(instance=hive_plot, fig=fig, ax=ax, figsize=figsize, center_plot=center_plot,
                           buffer=buffer, show_axes_labels=show_axes_labels, axes_labels_buffer=axes_labels_buffer,
                           axes_labels_fontsize=axes_labels_fontsize, mpl_axes_off=mpl_axes_off, zorder=5,
                           **axes_kwargs)
    node_viz_mpl(instance=hive_plot, fig=fig, ax=ax, zorder=5, **node_kwargs)
    edge_viz_mpl(instance=hive_plot, fig=fig, ax=ax, **edge_kwargs)

    return fig, ax


def p2cp_viz_mpl(p2cp: "P2CP instance",
                 fig: "matplotlib figure" or None = None, ax: "matplotlib axis" or None = None,
                 figsize: tuple = (10, 10), center_plot: bool = True, buffer: float = 0.1,
                 show_axes_labels: bool = True, axes_labels_buffer: float = 1.1,
                 axes_labels_fontsize: int = 16, mpl_axes_off: bool = True,
                 node_kwargs: dict or None = None, axes_kwargs: dict or None = None, **edge_kwargs):
    """
    Default ``matplotlib`` visualization of a ``P2CP`` instance.

    :param p2cp: ``P2CP`` instance we want to visualize.
    :param fig: default ``None`` builds new figure. If a figure is specified, ``Axis`` instances will be
        drawn on that figure. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param ax: default ``None`` builds new axis. If an axis is specified, ``Axis`` instances will be drawn on that
        axis. Note: ``fig`` and ``ax`` must BOTH be ``None`` to instantiate new figure and axes.
    :param figsize: size of figure. Note: only works if instantiating new figure and axes (e.g. ``fig`` and ``ax`` are
        ``None``).
    :param center_plot: whether to center the figure on ``(0, 0)``, the currently fixed center that ``Axis`` instances
        can be drawn around.
    :param buffer: fraction of the axes past which to buffer x and y dimensions (e.g setting ``buffer`` to 0.1 will find
        the maximum radius spanned by any ``Axis`` instance and set the x and y bounds as
        ``(-max_radius - buffer * max_radius, max_radius + buffer * max_radius)``.
    :param show_axes_labels: whether to label the hive plot axes in the figure (uses ``Axis.long_name`` for each
        ``Axis``.)
    :param axes_labels_buffer: fraction which to radially buffer axes labels (e.g. setting ``axes_label_buffer`` to 1.1
        will be 10% further past the end of the axis moving from the origin of the plot).
    :param axes_labels_fontsize: font size for hive plot axes labels.
    :param mpl_axes_off: whether to turn off Cartesian x, y axes in resulting ``matplotlib`` figure (default ``True``
        hides the x and y axes).
    :param node_kwargs: additional params that will be applied to all points on axes. Note, these are kwargs that
        affect a ``plt.scatter()`` call.
    :param axes_kwargs: additional params that will be applied to all axes. Note, these are kwargs that affect
        a ``plt.plot()`` call.
    :param edge_kwargs: additional params that will be applied to all edges on all axes (but kwargs specified beforehand
        in ``P2CP.build_edges()`` or ``P2CP.add_edge_kwargs()`` will take priority).
        To overwrite previously set kwargs, see ``P2CP.add_edge_kwargs()`` for more. Note, these are kwargs that
        affect a ``plt.plot()`` call.
    :return: ``matplotlib`` figure, axis.
    """

    if node_kwargs is None:
        node_kwargs = dict()

    if axes_kwargs is None:
        axes_kwargs = dict()

    fig, ax = axes_viz_mpl(instance=p2cp, fig=fig, ax=ax, figsize=figsize, center_plot=center_plot,
                           buffer=buffer, show_axes_labels=show_axes_labels, axes_labels_buffer=axes_labels_buffer,
                           axes_labels_fontsize=axes_labels_fontsize, mpl_axes_off=mpl_axes_off, zorder=5,
                           **axes_kwargs)
    node_viz_mpl(instance=p2cp, fig=fig, ax=ax, zorder=5, **node_kwargs)
    edge_viz_mpl(instance=p2cp, fig=fig, ax=ax, **edge_kwargs)

    return fig, ax


def p2cp_legend_mpl(p2cp: "P2CP instance", fig: "matplotlib figure", ax: "matplotlib axis",
                    tags_to_include: list or str = "all",
                    title: str = "Tags", line_kwargs: dict or None = None, **legend_kwargs):
    """
    Generate a legend for a ``P2CP`` instance, where entries in the legend will be tags of data added to the instance.

    :param p2cp: ``P2CP`` instance we want to visualize.
    :param fig: ``matplotlib`` figure on which we will draw the legend.
    :param ax: ``matplotlib`` axis on which we will draw the legend.
    :param tags_to_include: which tags of data to include in the legend. Default "all" uses all tags under
        ``p2cp.tags``. This can be ignored unless explicitly wanting to _exclude_ certain tags from the legend.
    :param title: title of the legend. Default "Tags".
    :param line_kwargs: keyword arguments that will add to / overwrite _all_ of the legend line markers from the
        defaults used in the original ``P2CP`` instance plot. For example, if one plots a large number of lines with low
        ``alpha`` and / or a small ``lw``, one will likely want to include ``line_kwargs=dict(alpha=1, lw=2)`` so the
        representative lines in the legend are legible.
    :param legend_kwargs: additional params that will be applied to the legend. Note, these are kwargs that affect a
        ``plt.legend()`` call. Default is to plot the legend in the upper right outside of the bounding box (e.g.
        ``loc="upper left", bbox_to_anchor=(1, 1)``).
    :return: ``matplotlib`` figure, axis.
    """

    # tags are on every 2 axis pair
    t1, t2 = p2cp.axes_list[:2]

    if line_kwargs is None:
        line_kwargs = dict()

    if tags_to_include == "all":
        tags_to_include = p2cp.tags[:]

    kwargs = [p2cp._hiveplot.edges[t1][t2][key]["edge_kwargs"].copy()
              for key in tags_to_include]

    # add / overwrite line kwargs with any additionally supplied kwargs
    for kwarg in kwargs:
        for k in line_kwargs:
            kwarg[k] = line_kwargs[k]

    leg = [Line2D([0, 0], [0, 0], label=key, **kwargs[k])
           for k, key in enumerate(tags_to_include)]
    if "loc" not in legend_kwargs:
        legend_kwargs["loc"] = "upper left"
    if "bbox_to_anchor" not in legend_kwargs:
        legend_kwargs["bbox_to_anchor"] = (1, 1)
    legend_kwargs["title"] = title

    ax.legend(handles=leg, **legend_kwargs)

    return fig, ax
