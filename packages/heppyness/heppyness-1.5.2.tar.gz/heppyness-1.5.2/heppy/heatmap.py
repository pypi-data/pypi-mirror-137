import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from .histogram import histogram2d
import heppy.panel
import heppy.plot



class TextFormatter:
    '''
    Predefined functions to format bin content text printed on heatmap. The user can alternatively write their own such functions.

    Contents will be printed with a precision of (up to) three significant digits. If you want to set a different precision, you can
    create your own adapted formatting function as the following example illustrates:

    .. code-block:: python

        import functools
        # set the number of significant digits (e.g. to 4)
        formatter = functools.partial(TextFormatter.nominal, significants=4)
        # or set the fixed absolute precision (e.g. to 3 digits after the decimal point)
        formatter = functools.partial(TextFormatter.nominal, fixedprec=3)
        # then use as: heppy.make_heatmap(..., text_format=formatter, ...)

    Here :code:`significants` represents the maximum number of significant digits considered (default: 3), while :code:`fixedprec`
    represents the fixed absolute precision considered, e.g. :code:`1` for a precision of 0.1 or :code:`-1` for a precision of 10
    (default: :code:`None`). If :code:`fixedprec` is given, :code:`significants` is ignored.

    Hint: when writing a custom formatting function, any unnecessary keyword arguments can be absorbed into
    a :code:`**kwargs` catch-all parameter to keep the function signature shorter and tidier.
    '''

    @staticmethod
    def _to_str(val, significants=3, fixedprec=None, suppress_zero=True):
        '''
        Auxiliary function to get a string representation of the value with a given
        number of significant digits or with a given fixed precision

        Is suppress_zero is True, texts that round to a number mathematically equivalent to zero
        are not printed
        '''
        if fixedprec is not None:
            fixedprec = int(fixedprec)
            if fixedprec >= 0:
                string = np.format_float_positional(val, precision=fixedprec, trim='-')
                return '' if suppress_zero and set(string) <= {'-', '.', '0'} else string
            val = round(val, fixedprec)
            return '{:g}'.format(val)
            #return '{:.<digits>f}'.replace('<digits>', str(max(0, fixedprec))).format(val)
        string = np.format_float_positional(float('{:.<sig>g}'.replace('<sig>', str(significants)).format(val)), precision=20, trim='-')
        return '' if suppress_zero and set(string) <= {'-', '.', '0'} else string



    @staticmethod
    def _pm_uncertainty(up, down):
        '''
        Return "+/- up" if up == down, else return "^{+u}_{-d}"
        '''
        return r'\pm {up}'.format(up=up) if up == down else r'^{{+{up}}}_{{-{down}}}'.format(up=up, down=down)



    @staticmethod
    def nominal(significants=3, fixedprec=None, nominal=None, **ignore):
        """Returns LaTeX string of nominal value."""
        return TextFormatter._to_str(nominal, significants=significants, fixedprec=fixedprec)



    @staticmethod
    def brief(significants=3, fixedprec=None, nominal=None, uncert_up=None, uncert_down=None, **ignore):
        r"""Returns LaTeX string of nominal value and total uncertainty.

        The format is :math:`\mathrm{nominal} \pm \sigma`,
        where :math:`\sigma` is the uncertainty from the uncorrelated variations and
        the correlated variations.
        Asymmetric uncertainties are supported and will be shown as
        :math:`^{\sigma^{\mathrm{up}}}_{\sigma^{\mathrm{down}}}`.
        """
        n = TextFormatter._to_str(nominal, significants=significants, fixedprec=fixedprec)
        u = TextFormatter._to_str(uncert_up, significants=significants, fixedprec=fixedprec)
        d = TextFormatter._to_str(uncert_down, significants=significants, fixedprec=fixedprec)
        # If _all_ of `n`, `u`, `d` rounded to zero and were suppressed, return empty string.
        if not any([n, u, d]):
            return ''
        # If _some but not all_ of `n`, `u`, `d` rounded to zero and were suppressed,
        # remake them all without suppression. Otherwise we get awkward texts like "± 0.1" or
        # "5.0 ±" with missing numbers.
        if any([n, u, d]) and not all([n, u, d]):
            n = TextFormatter._to_str(nominal, significants=significants, fixedprec=fixedprec, suppress_zero=False)
            u = TextFormatter._to_str(uncert_up, significants=significants, fixedprec=fixedprec, suppress_zero=False)
            d = TextFormatter._to_str(uncert_down, significants=significants, fixedprec=fixedprec, suppress_zero=False)
        return r'${n}{pm_uncert}$'.format(n=n, pm_uncert=TextFormatter._pm_uncertainty(u, d))



    @staticmethod
    def statsyst(significants=3, fixedprec=None, nominal=None, stat_up=None, stat_down=None, syst_up=None, syst_down=None, **ignore):
        r"""Returns LaTeX string of nominal value and statistical and systematic uncertainty.

        The format is :math:`\mathrm{nominal} \pm \sigma_{\mathrm{stat}} \pm \sigma_{\mathrm{syst}}`,
        where :math:`\sigma_{\mathrm{stat}}` is the uncertainty from the uncorrelated variations and
        :math:`\sigma_{\mathrm{syst}}` is the uncertainty from the correlated variations.
        Asymmetric uncertainties are supported and will be shown as
        :math:`^{\sigma_{\mathrm{syst}}^{\mathrm{up}}}_{\sigma_{\mathrm{syst}}^{\mathrm{down}}}` etc.
        """
        n = TextFormatter._to_str(nominal, significants=significants, fixedprec=fixedprec)
        stat_u = TextFormatter._to_str(stat_up, significants=significants, fixedprec=fixedprec)
        stat_d = TextFormatter._to_str(stat_down, significants=significants, fixedprec=fixedprec)
        syst_u = TextFormatter._to_str(syst_up, significants=significants, fixedprec=fixedprec)
        syst_d = TextFormatter._to_str(syst_down, significants=significants, fixedprec=fixedprec)
        if all([s == '' for s in [n, stat_u, stat_d, syst_u, syst_d]]): return ''
        return r'${n}{pm_stat_uncert}{{}}{pm_syst_uncert}$'.format(n=n, pm_stat_uncert=TextFormatter._pm_uncertainty(stat_u, stat_d), pm_syst_uncert=TextFormatter._pm_uncertainty(syst_u, syst_d))





def _make_text(text_format, input_dict):
    '''
    Create a string from the values in input dictionary according to the specified formatting string or function

    :param text_format: string template or function returning the text to be printed inside each bin
    :type text_format: `str` or `function`

    :param input_dict: dictionary containing the following keys: `'nominal'`, `'uncert_up'`, `'uncert_down'`, `'stat_up'`, `'stat_down'`, `'syst_up'`, `'syst_down'`
    :type input_dict: `dict`
    '''
    if isinstance(text_format, str):
        return text_format.format(**input_dict)
    # Assume it's a function and call it with the contents of input_dict as keyword arguments
    return text_format(**input_dict)



def _map_to_equispaced(array):
    '''
    Map each value in the array to an integer-and-a-half value such that the minimum value gets
    mapped to 0.5 and the highest value to len(array) - 0.5, and all other values fall in between
    in a sorted manner.
    '''
    # NB: np.unique returns the _sorted_ unique values
    translate = { val : i + 0.5 for i, val in enumerate(np.unique(array)) }
    return np.array( [translate[val] for val in array] )



def make_heatmap(histogram, areas=False, title='', figsize=(8, 5), colorbar=True, text_format=TextFormatter.brief, text_precision=3, text_autocolor=True, black_text_below=None, monowidth=False, write='', xmax=None, **kwargs):
    '''
    Make a heatmap plot of a two-dimensional histogram

    :param histogram: two-dimensional histogram to visualise
    :type histogram: :py:class:`heppy.histogram2d`
    :param title: plot title
    :type title: :code:`str`
    :param figsize: figure size
    :type figsize: :code:`tuple` of :code:`float`
    :param colorbar: show color bar or not
    :type colorbar: ``bool``
    :param text_format: string template or function returning the text to be printed inside each bin. The following format keys (if string) or keyword arguments \
    (if function) will be provided: {nominal}, {uncert_up} and {uncert_down} for total uncertainty, {stat_up} and {stat_down} for statistical uncertainty, \
    {syst_up} and {syst_down} for systematic uncertainty. All uncertainties are given as non-negative numbers. The class :py:class:`heppy.TextFormatter` provides \
    a set of useful and somewhat adaptable predefined formatter functions.
    :type text_format: :code:`str`, :code:`function` or :code:`None`
    :param monowidth: if True, all bins are shown as equally wide/high, with the bin edges written in the label.
    :type monowidth: :code:`bool`
    :param write: may be changed to a filename, which will result in the figure being rendered and saved to disk
    :type write: :code:`str`
    :param **kwargs: keyword arguments that get passed on to :code:`plt.hist2d`

    The following keys in :code:`histogram.plot_attributes` can be used to set axis labels:

    - :code:`"xlabel"` – x-axis label
    - :code:`"ylabel"` – y-axis label
    '''
    if not isinstance(histogram, histogram2d):
        raise TypeError('Heatmaps can only be made for a 2D histogram (heppy.histogram2d), got instance of type {type}'.format(type=type(histogram)))

    fig, axes = plt.subplots(1, figsize=figsize)

    midx, midy, heights = histogram.points()


    # Visualised bin edges and midpoints
    vis_binedges = histogram.binedges
    vis_midx = midx
    vis_midy = midy
    # If monowidth visualisation is desired, the actual bin edges and midpoints are mapped to equidistant
    # visualised ones:
    if monowidth:
        # Bin edges at integers from zero:
        vis_binedges = (np.array([i for i, _ in enumerate(histogram.binedges[0])]), np.array([i for i, _ in enumerate(histogram.binedges[1])]))
        # Bin midpoints at integers from zero PLUS 0.5 (to make them midpoints w.r.t. the edges):
        vis_midx = _map_to_equispaced(midx)
        vis_midy = _map_to_equispaced(midy)


    # Set default plot options and override them with the ones the user provided
    plot_options = {'norm' : LogNorm(), 'cmap' : 'Blues', **kwargs}

    # midx and midy are used here as "dummy" fill values at the bin centres.
    # The histogram is filled "with" these values with the actual bin height (or optionally area) as "weight"
    nominals = np.ravel(histogram.areas) if areas else heights
    uncertups, uncertdowns = histogram.net_variations(variations='all', subtract_nominal=True, relative=False)
    uncertups = np.ravel(uncertups) if areas else np.ravel(uncertups/histogram.binsizes)
    uncertdowns = np.abs(np.ravel(uncertdowns)) if areas else np.abs(np.ravel(uncertdowns/histogram.binsizes))
    systups, systdowns = histogram.net_variations(variations=list(histogram.corr_variations.keys()), subtract_nominal=True, relative=False)
    systups = np.ravel(systups) if areas else np.ravel(systups/histogram.binsizes)
    systdowns = np.abs(np.ravel(systdowns)) if areas else np.abs(np.ravel(systdowns/histogram.binsizes))
    statups, statdowns = histogram.net_variations(variations=list(histogram.uncorr_variations.keys()), subtract_nominal=True, relative=False)
    statups = np.ravel(statups) if areas else np.ravel(statups/histogram.binsizes)
    statdowns = np.abs(np.ravel(statdowns)) if areas else np.abs(np.ravel(statdowns/histogram.binsizes))

    h2d = plt.hist2d(vis_midx, vis_midy, weights=nominals, bins=vis_binedges, **plot_options)
    if colorbar:
        fig.colorbar(h2d[3])

    max_value_of_heatmap = np.max(nominals)
    if text_format is not None:
        # Write bin contents as text onto the plot
        for x, y, nominal, uncert_up, uncert_down, syst_up, syst_down, stat_up, stat_down in zip(vis_midx, vis_midy, nominals, uncertups, uncertdowns, systups, systdowns, statups, statdowns):
            values = {
                'nominal' : nominal,
                'uncert_up' : uncert_up,
                'uncert_down' : uncert_down,
                'syst_up' : syst_up,
                'syst_down' : syst_down,
                'stat_up' : stat_up,
                'stat_down' : stat_down,
            }
            text = _make_text(text_format, values)
            if black_text_below is None:
                color = 'black' if (nominal / max_value_of_heatmap < 0.03) else 'white'
            else:
                color = 'black' if (nominal < black_text_below) else 'white'
            if not text_autocolor:
                color = 'black'
            axes.text(x, y, text, verticalalignment='center', horizontalalignment='center', color=color, fontsize=8)

    # Set proper tick labels for monowidth plots:
    if monowidth:
        axes.set_xticks(vis_binedges[0])
        axes.set_yticks(vis_binedges[1])
        # Nicely format the actual binedges: drop any trailing decimal points and zeros
        # if all have integer values by converting the values to ints:
        actual_binedges_x = histogram.binedges[0].astype(int) if np.all(np.equal(np.mod(histogram.binedges[0], 1), 0)) else np.around(histogram.binedges[0], 5)
        actual_binedges_y = histogram.binedges[1].astype(int) if np.all(np.equal(np.mod(histogram.binedges[1], 1), 0)) else np.around(histogram.binedges[1], 5)
        axes.set_xticklabels(actual_binedges_x)
        axes.set_yticklabels(actual_binedges_y)

    # Make the plot prettier
    if title:
        axes.set_title(title, x=0., ha='left', size='x-large')
    if 'xlabel' in histogram.plot_attributes:
        axes.set_xlabel(histogram.plot_attributes['xlabel'], ha='right', x=1., size='x-large')
    if 'ylabel' in histogram.plot_attributes:
        axes.set_ylabel(histogram.plot_attributes['ylabel'], ha='right', y=1., size='x-large')
    axes.tick_params(which='both', bottom=True, top=True, left=True, right=True, direction='in')
    fig.subplots_adjust(top=0.9, hspace=0.02)

    # Maybe save it to file
    if write:
        fig.savefig(write)

    return fig, axes
