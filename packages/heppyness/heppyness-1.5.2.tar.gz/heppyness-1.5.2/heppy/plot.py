import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import heppy.panel
import heppy.histogram
from copy import deepcopy
import textwrap
import inspect

# Do not use axis value offsets by default, i.e. do not pull out common
# factors or constant offsets and put them at the top of the axis
mpl.rcParams['axes.formatter.useoffset'] = False


def _filter_plot_attributes(function, plot_attributes):
    """Returns only the plot attributes that are valid for the function."""
    updated = deepcopy(plot_attributes)
    signature = str(inspect.signature(function))
    for a in plot_attributes:
        if not ' '+a+'=' in signature:
            del updated[a]
    return updated



def _get_greater_zorder(hl):
    '''
    @param hl tuple of legend (handle, label)
    '''
    #print(hl[1])
    try:
        #print(hl[0].get_zorder())
        return(hl[0].get_zorder())
    except AttributeError:
        #print(hl[0][0].get_zorder())
        return(hl[0][0].get_zorder())



def _stable_sort_by_zorder(handles, labels):
    return zip(*sorted(zip(handles, labels), key=lambda hl: _get_greater_zorder(hl), reverse=True))



def _combine_legend_entries_with_same_label(handles, labels):
    out_handles = []
    out_labels = []
    for label in labels:
        if label in out_labels:
            # already added this label --> skip
            continue
        indices_of_label = [i for i, l in enumerate(labels) if l == label]
        # if len(indices_of_label) > 1:
        #     print(f'Found multiple artists for label {label}, will combine them into one legend entry.')
        out_labels.append((label))
        out_handles.append(tuple([handles[i] for i in reversed(indices_of_label)]))
    return out_handles, out_labels



def _get_narrowest_bin_width_in_pixels(axis, histogram):
    index_of_narrowest_bin = np.argmin(histogram.binwidths)
    x_lower = histogram.binedges[index_of_narrowest_bin]
    x_upper = histogram.binedges[index_of_narrowest_bin + 1] # cannot go out of bounds, because len(binedges) == len(binwidths) + 1
    arbitrary_y = np.max(histogram.heights[np.isfinite(histogram.heights)]) # pick some (here: maximum) finite bin height from the histogram as y coordinate
    (a, _) = axis.transData.transform((x_lower, arbitrary_y))
    (b, _) = axis.transData.transform((x_upper, arbitrary_y))
    return (b - a)



def make_figure(panels, title='', figsize=(8, 5), write='', xlims=None, xmax=None, legend_outside=False):
    '''
    :param panels: panel(s) to visualise in the plot
    :type panels: :py:class:`heppy.panel` or ``list`` of :py:class:`heppy.panel`
    :param title: plot title
    :type title: str
    :param write: may be changed to a filename, which will result in the figure being rendered and saved at the given location
    :type write: str
    :param legend_outside: option to move the legend next to the plot panels. It also changes the legend style to try to make it look better next to the plot: no box, text wrapped at 30 characters (not tested with LaTeX rendering --- proceed with caution), smaller text (fontsize='small')
    :type legend_outside: bool
    :param xlims: can be used to manually set lower and upper x-axis limits, e.g. xlims=(0.0, 2.0)
    :type xlims: `tuple` of `float`, or `None`

    :returns: tuple of the created plt.figure object and plt.axes objects. These can be assigned to variables by the user to allow further manipulations of the plot (style, contents, etc.)
    '''
    if isinstance(panels, heppy.panel):
        panels = [panels]

    if len(panels) > 1:
        fig, axes = plt.subplots(len(panels), sharex=True, gridspec_kw={'height_ratios' : [p.height for p in panels]}, figsize=figsize)
    else:
        fig, ax = plt.subplots(1, figsize=figsize)
        axes = [ax]

    artists = {}
    x = None # used to set the x-axis range later

    for i, p in enumerate(panels):

        if p.stack:
            for histogram, band in zip(p.stack.histograms, p.stack.iterbands()):
                x = band[0]
                plot_attributes = deepcopy(histogram.plot_attributes)
                if not 'label' in plot_attributes:
                    plot_attributes['label'] = histogram.name
                artists[histogram.name] = axes[i].fill_between(*band, **plot_attributes)

        for histogram in p.curves:
            x = histogram.curve()[0]
            plot_attributes = deepcopy(histogram.plot_attributes)
            if not 'label' in plot_attributes:
                plot_attributes['label'] = histogram.name
            # Filter out plot attributes that are invalid for curves
            plot_attributes = _filter_plot_attributes(mpl.lines.Line2D, plot_attributes)
            if 'label' in histogram.plot_attributes.keys():
                plot_attributes['label'] = histogram.plot_attributes['label']

            # If a histogram of the same name was already previously plotted, plot this one in the same colour.
            # Otherwise just plot it in the next colour in the sequence as usual.
            # If the histogram has an explicitly specified color, that one is always used.
            try:
                if 'color' in histogram.plot_attributes.keys():
                    raise KeyError
                previous = artists[histogram.name]
                artists[histogram.name] = axes[i].plot(*histogram.curve(), color=previous[0].get_color(), **plot_attributes)
            except (KeyError, TypeError):
                artists[histogram.name] = axes[i].plot(*histogram.curve(), **plot_attributes)

        for scatter in p.scatters:
            x = scatter.binedges[:-1]
            y = scatter.areas
            # for scatter_index in range(len(x)):
            #     print(x[scatter_index], y[scatter_index])
            plot_attributes = deepcopy(scatter.plot_attributes)
            if not 'label' in plot_attributes:
                raise RuntimeError('Please provide a label for scatter!')
            # Filter out plot attributes that are invalid for curves
            plot_attributes = _filter_plot_attributes(mpl.lines.Line2D, plot_attributes)
            if 'label' in scatter.plot_attributes.keys():
                plot_attributes['label'] = scatter.plot_attributes['label']
            # If a scatter of the same name was already previously plotted, plot this one in the same colour.
            # Otherwise just plot it in the next colour in the sequence as usual.
            # If the scatter has an explicitly specified color, that one is always used.
            try:
                if 'color' in scatter.plot_attributes.keys():
                    raise KeyError
                previous = artists[scatter.name]
                artists[scatter.name] = axes[i].plot(x, y, color=previous[0].get_color(), **plot_attributes)
            except (KeyError, TypeError):
                artists[scatter.name] = axes[i].plot(x, y, **plot_attributes)

        for histogram in p.bands:
            x = histogram.curve()[0]
            plot_attributes = deepcopy(histogram.plot_attributes)
            if not 'label' in plot_attributes:
                plot_attributes['label'] = histogram.name
            #edgecolor = '0.5' if not 'edgecolor' in plot_attributes.keys() else plot_attributes['edgecolor']
            color = plot_attributes.get('color', '0.75')
            hatch = plot_attributes.get('hatch', 'xxxxxx')
            alpha = plot_attributes.get('alpha', 0.3)
            facecolor = plot_attributes.get('color', 'none')
            artists[histogram.name] = axes[i].fill_between(*histogram.errorband(), facecolor=facecolor, edgecolor=color, alpha=alpha, linewidth=0, hatch=hatch, label=plot_attributes['label'])
            # TODO: give bands different colours and hatches


        pointshift = 0. - ((len(p.points) - 1) // 2) * p.pointshift # points may be shifted horizonally consecutively to prevent them from overlapping
        for histogram in p.points:
            label = histogram.plot_attributes['label'] if 'label' in histogram.plot_attributes else histogram.name
            # If a histogram of the same name was already previously plotted, plot this one in the same colour.
            # Otherwise just plot it in the next colour in the sequence as usual.
            # If the histogram has an explicitly specified color, that one is always used.
            try:
                if 'color' in histogram.plot_attributes:
                    raise KeyError
                previous = artists[histogram.name]
                #print(previous)
                #print(previous.properties())
                #color = previous[0].get_color()
                color = 'black'
            except KeyError:
                color = histogram.plot_attributes.get('color', 'k')

            marker = histogram.plot_attributes.get('marker', 'o')
            capsize = histogram.plot_attributes.get('capsize', None)

            x = histogram.curve()[0]
            errorbars = histogram.errorbars()

            # Shrink markers if bins are narrow, so that they do not overlap -->
            axes[i].set_xlim((min(x), max(x))) # need to specify axis limits first, so that we can convert minimum binwidth to axis pixels
            minwidth = _get_narrowest_bin_width_in_pixels(axes[i], histogram)
            markersize = histogram.plot_attributes.get('markersize', min(minwidth/2.3, 3.0)) # minwidth /= 2.3 needed to avoid overlapping markers
            # <-- finished picking marker size

            if np.count_nonzero(errorbars[0]) == 0 and np.count_nonzero(errorbars[1]) == 0:
                # Error bar sizes are all zero, do not draw error bars (this may mean that there were no variations in the histogram to begin with)
                artists[histogram.name] = axes[i].plot(*histogram.points(shift=pointshift, abs_shift=True), label=label, linestyle='None', marker=marker, color=color, markersize=markersize)
            else:
                import warnings
                warnings.warn('Doing HACK to flip errorbars due to an inconsistency in Heppy! --- please fix this in ISSUE #23')
                artists[histogram.name] = axes[i].errorbar(*histogram.points(shift=pointshift, abs_shift=True), yerr=(errorbars[1], errorbars[0]), label=label, linestyle='None', marker=marker, color=color, markersize=markersize, elinewidth=1, capsize=capsize, zorder=9999)

            pointshift += p.pointshift


        if p.title:  axes[i].set_title(p.title, x=0., y=1., va='top', ha='left', transform=axes[i].transAxes, size='large')
        if p.xlabel: axes[i].set_xlabel(p.xlabel, ha='right', x=1., size='x-large')
        if p.ylabel: axes[i].set_ylabel(p.ylabel, ha='right', y=1., size='x-large')
        if p.logx: axes[i].set_xscale('log', nonpositive='clip')
        if p.logy: axes[i].set_yscale('log', nonpositive='clip')
        if p.ylims: axes[i].set_ylim(p.ylims)

        axes[i].tick_params(which='both', bottom=True, top=True, left=True, right=True, direction='in')
        axes[i].set_xlim((min(x), max(x)))
        if xmax:
            axes[i].set_xlim((min(x), xmax))
        if xlims:
            axes[i].set_xlim(xlims)
        legend_handles, legend_labels = axes[i].get_legend_handles_labels()
        try:
            legend_handles, legend_labels = _stable_sort_by_zorder(legend_handles, legend_labels) # do this BEFORE combining entries with same label
        except:
            pass
        legend_handles, legend_labels = _combine_legend_entries_with_same_label(legend_handles, legend_labels)
        #axes[i].legend(legend_handles[::-1], legend_labels[::-1])
        if not p.nolegend:
            # print('Updating plot legend.')
            if legend_outside:
                # Also wraps the legend labels to make the legend high and narrow --- fits well on the side of the plot
                #legend_labels = [textwrap.fill(label, width=30) for label in legend_labels]
                # Attempt to make this work better with LaTeX-rendered labels by only
                # line-breaking such labels that do not contain LaTeX math:
                legend_labels = [label if '$' in label else textwrap.fill(label, width=30) for label in legend_labels]
                axes[i].legend( legend_handles, legend_labels, bbox_to_anchor=(1.01, 1.0), fontsize='small', frameon=False, title=p.legend_title)
            else:
                axes[i].legend(legend_handles, legend_labels, title=p.legend_title)



    if title: axes[0].set_title(title, x=0., ha='left', size='x-large')
    fig.subplots_adjust(top=0.9, hspace=0.02)
    # fig.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1, hspace=0.02)
    if legend_outside:
        fig.subplots_adjust(right=0.7)

    if write:
        fig.savefig(write)

    return fig, axes



def make_uncertainty_breakdown(histogram, separator='__', ylims=None, xlabel='', **kwargs):
    '''
    @histogram: heppy.histogram object for which the uncertainty breakdown figure will be made
    @separator: string that separates high/low (up/down, ...) indictator from the rest of the uncertainty name, e.g.
                "jet_energy_scale__1up" and "jet_energy_scale__1down" uses the separator "__"
    @ylims: may be set to a tuple/list of lower and upper y-axis limits, e.g. ylims=(0.0, 2.0)
    @**kwargs: get passed on to make_figure()
    '''
    all_variations = {**histogram.corr_variations, **histogram.uncorr_variations}
    # Make a list of unique uncertainty names that differ only by suffix (= everything after @separator), without suffixes
    uncertainty_names = sorted(list(set([key.split(separator)[0] for key in all_variations])))
    # Make a list of all the breakdown histograms
    breakdown_histograms = []
    linestyles = ['-', '--', '-.', ':']
    for i, name in enumerate(uncertainty_names):
        # There are 10 different colours in the default sequence, so change line style every 10 uncertainties to keep them distinguishable
        linestyle = linestyles[(i % 40) // 10] # index switches 0, 1, 2, 3, 0, 1, 2, 3, 0 etc. every 10 steps
        # Pick the variations corresponding to this name and make a histogram for each, but all with the same histogram name
        # (so that they will later get plotted with the same colour and get a common legend label)
        for variation in all_variations.keys():
            if not variation.startswith(name + separator):
                continue
            # Histogram whose nominal reflects the relative uncertainty in percent:
            bh = deepcopy(heppy.histdiv(histogram.extract_variation_histogram(variation), histogram, ignore_denominator_uncertainty=True))
            bh.name = name
            bh.plot_attributes = {'linestyle' : linestyle, 'label' : name}
            breakdown_histograms.append(bh)
    histogram_for_total_uncertainty = (heppy.histdiv(histogram, histogram, ignore_denominator_uncertainty=True))
    histogram_for_total_uncertainty.name = 'Total'
    histogram_for_total_uncertainty.plot_attributes = {'edgecolor' : '0.8', 'label' : 'Total'}
    line_at_100 = deepcopy(histogram_for_total_uncertainty)
    line_at_100.name = ''
    line_at_100.plot_attributes = {'color' : 'k', 'linewidth' : 1, 'linestyle' : '--'}
    # Make a panel for the figure
    panel = heppy.panel(ylabel='Ratio to nominal', curves=breakdown_histograms + [line_at_100], bands=[histogram_for_total_uncertainty], xlabel=xlabel, ylims=ylims)
    return make_figure(panel, **kwargs)



def make_roc_figure(signal, background, ylims=None, **kwargs):
    """Plots ROC curve(s) based on the given input histograms.

    :param signal: one or more histograms with "cumulative" signal efficiencies
    (= each bin contains the efficiency obtained by cutting above the lower edge
    of the bin in question)
    :type signal: :py:class:`heppy.histogram1d` or iterable thereof
    :param background: one or more histograms with "cumulative" background
    efficiencies (see `signal`). If multiple are given, they must correspond to
    the ones for signal in the same order.
    :type background: :py:class:`heppy.histogram1d` or iterable thereof
    :param **kwargs: get passed on to :py:func:`heppy.make_figure`

    Note: plot stylings and labels are taken from the _signal_ histogram(s), so
    make sure that those are set as you want them. The ones of the _background_
    histogram(s) are ignored.
    """
    rocs = []
    for sig, bkg in zip(signal, background):
        roc = deepcopy(sig)
        roc.binedges = np.append(sig.heights[::-1], np.max(sig.heights+1.0)) * 100.0 # the uppermost bin edge doesn't matter at all
        roc.areas = bkg.heights[::-1] * 100.0
        # print(roc.binedges)
        # print('SIG HEIGHTS')
        # print(roc.areas)
        # print('BKG HEIGHTS')
        # raise RuntimeError
        rocs.append(roc)
    panel = heppy.panel(scatters=rocs, ylims=ylims, xlabel='Signal efficiency (%)', ylabel='Background efficiency (%)')
    return make_figure(panel, **kwargs)
