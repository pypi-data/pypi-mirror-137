import numpy as np
import numbers
import operator
import warnings
from copy import deepcopy
from functools import partial
from textwrap import dedent
import pandas as pd

from . import Value



def _calculate_bin_sizes(binedges):
    '''
    Auxiliary function for calculating bin sizes (widths in the 1D case, surface areas in the 2D case).

    :param binedges: bin edges
    :type binedges: Numpy array, tuple of two Numpy arrays
    :returns: Numpy array of bin sizes

    For a one-dimensional histogram, returns an array of dimension (N, 1), where N is the number of bins.
    The elements represent the width of each bin.

    For a two-dimensional histogram, returns an array of dimension (N, M), where N is the number of bins
    along the first axis ("x-axis") and M is the number of bins along the second axis ("y-axis"). The
    elements represent the surface area of each bin.

    '''
    if isinstance(binedges, tuple):
        if len(binedges) > 2:
            raise NotImplementedError('Calculating bin areas is only implemented for 1- and 2-dimensional histograms')
        # Calculate bin widths along each axis:
        binwidths = (np.diff(edges) for edges in binedges)
        return np.outer(*binwidths)
    return np.diff(binedges)



def _get_bin_index(binedges, value, label='x'):
    """Returns the index of the bin that contains the given value.

    Lower bin edges are included in a bin, upper bin edges are excluded (same as in the `ROOT <https://root.cern>`_ convention).

    :param binedges: the bin edges
    :type binegdes: ``np.array`` of ``float``
    :param value: value
    :type value: ``float``
    :param label: a label that makes error messages, if any, more useful. Typically the axis that the binedges and value correspond to.
    :type label: ``str``

    :returns: index of bin that contains the value
    :rtype: ``int``

    :raises ValueError: if value lies outside of the outer bin edges
    """
    if value < np.min(binedges) or value >= np.max(binedges):
        raise ValueError('Cannot find index of bin containing {label} = {val}, which is outside of histogram {label}-boundaries [{valmin}, {valmax})'.format(val=value, label=label, valmin=np.min(binedges), valmax=np.max(binedges)))
    return np.searchsorted(binedges, value, side='right') - 1





class basehistogram(object):
    '''
    Base class for one-dimensional and two-dimensional histograms that keep track of their various uncertainty contributions and arbitrary attributes (useful for labeling and plotting).

    :param binedges: bin edges, including uppermost. For 1D histograms, a :code:`numpy.array`. For 2D histograms, a :code:`tuple` of two :code:`numpy.array` (in the x and y direction, respectively).
    :type binedges: :code:`numpy.array`, or :code:`tuple` of :code:`numpy.array`
    :param contents: the "bin contents", which are either bin areas (= what ROOT calls "bin contents") or bin heights (= bin areas / bin sizes). See also argument :code:`areas`.
    :type contents: :code:`numpy.array`
    :param areas: if True, interpret given contents as bin areas, else as bin heights
    :type areas: :code:`bool`
    :param name: a name for the histogram. This is only separate from the other attributes because it is so commonly used and is automatically created for histograms produced by mathematically combining two histograms. E.g. dividing two histograms with names :code:`'foo'` and :code:`'bar'` will return a histogram with name :code:`'foo / bar'`.
    :type name: :code:`str`
    :param uncorr_variations: dictionary of variations that are uncorrelated between bins (e.g. statistical uncertainty). Keys are variation names, values are :code:`np.array` objects of the same dimension as the nominal :code:`contents`.
    :type uncorr_variations: :code:`dict`
    :param corr_variations: dictionary of variations that are fully correlated between bins (e.g. systematic uncertainty). Keys are variation names, values are :code:`np.array` objects of the same dimension as the nominal :code:`contents`.
    :type corr_variations: :code:`dict`
    :param attributes: dictionary of completely arbitrary attributes that the user can provide/change/access. E.g. information about the data sample that produced the histogram.
    :type attributes: :code:`dict`
    :param plot_attributes: dictionary of completely arbitrary that the user can provide/change/access. This one is more intended for information on how to visualise/plot the histogram. It is especially useful if working with `heppy.make_figure`, which will *assume* that all the plot_attributes correspond to keyword arguments that are understood by Matplotlib's :code:`plot()` and/or :code:`fill_between()` functions
    :type plot_attributes: :code:`dict`
    '''
    def __init__(self, binedges, contents, areas=False, name='', uncorr_variations={}, corr_variations={}, attributes={}, plot_attributes={}):
        super(basehistogram, self).__init__()
        self.binedges = deepcopy(binedges)
        binsizes = _calculate_bin_sizes(binedges)
        self.areas = np.array(deepcopy(contents)) if areas else np.array(deepcopy(contents)) * binsizes
        self.name = deepcopy(name)
        self.uncorr_variations = deepcopy(uncorr_variations) if areas else {key : deepcopy(heights) * binsizes for key, heights in uncorr_variations.items()}
        self.corr_variations = deepcopy(corr_variations) if areas else {key : deepcopy(heights) * binsizes for key, heights in corr_variations.items()}
        self.attributes = deepcopy(attributes)
        self.plot_attributes = deepcopy(plot_attributes)



    def __str__(self):
        '''
        Human-readable string showing the contents and properties of the histogram.
        '''
        properties = {
            'name' : self.name,
            'type' : type(self),
            'attributes' : '\n  '.join([key+' : '+val.__str__() for key, val in self.attributes.items()]),
            'plot_attributes' : '\n  '.join([key+' : '+val.__str__() for key, val in self.plot_attributes.items()]),
            'binedges' : self.binedges.__str__(),
            'binsizes' : self.binsizes.__str__(),
            'areas' : self.areas.__str__(),
            'uncorr_variations' : '\n  '.join([key+' : '+val.__str__() for key, val in self.uncorr_variations.items()]),
            'corr_variations' : '\n  '.join([key+' : '+val.__str__() for key, val in self.corr_variations.items()]),
            }
        for key in properties.keys():
            if properties[key] == '': properties[key] = '(none)'
        form = '\n'.join([
            'Name: {name}',
            'Type: {type}',
            'Attributes:',
            '  {attributes}',
            'Plot attributes:',
            '  {plot_attributes}',
            'Bin edges:',
            '  {binedges}',
            'Bin sizes:',
            '  {binsizes}',
            'Nominal areas:',
            '  {areas}',
            'Uncorrelated variation areas:',
            '  {uncorr_variations}',
            'Correlated variation areas:',
            '  {corr_variations}',
            ])
        return form.format(**properties)



    def extract_variation_histogram(self, variation, **kwargs):
        '''
        Get a new histogram object that has a given variation as nominal.
        Useful e.g. for studying a particular systematic variation.

        :param variation: name of the variation
        :type variation: :code:`str`
        :param **kwargs: get passed on to constructor of new histogram, e.g. useful to set a :code:`name` for the new histogram.

        :returns: new :py:class:`heppy.histogram` that has a given :code:`variation` as nominal
        :raises KeyError: if variation not found in either uncorrelated or correlated variations
        :raises RuntimeError: if variation found in both uncorrelated or correlated variations
        '''
        if variation in self.uncorr_variations.keys() and variation in self.corr_variations.keys():
            raise RuntimeError('Cannot resolve ambiguity: a variation of name "{variation}" was found in both the uncorrelated and correlated variation dictionary.'.format(variation=variation))
        try:
            return type(self)(self.binedges, self.corr_variations[variation], areas=True, **kwargs)
        except KeyError:
            try:
                return type(self)(self.binedges, self.uncorr_variations[variation], areas=True, **kwargs)
            except KeyError:
                raise KeyError('Variation "{variation}" was not found in either the uncorrelated or correlated variation dictionary.'.format(variation=variation))



    @property
    def binsizes(self):
        '''
        Bin sizes.

        For a one-dimensional histogram, returns an array of dimension (N, 1), where N is the number of bins.
        The elements represent the width of each bin.

        For a two-dimensional histogram, returns an array of dimension (N, M), where N is the number of bins
        along the first axis ("x-axis") and M is the number of bins along the second axis ("y-axis"). The
        elements represent the area of each bin.
        '''
        # For 2D histograms, self.binedges is a tuple of arrays that describe the bin edges along each axis
        return _calculate_bin_sizes(self.binedges)


    @property
    def heights(self):
        '''
        Bin heights, equal to bin areas divided by the corresponding bin sizes
        '''
        return self.areas / self.binsizes



    def set_heights(self, heights):
        '''
        Set bin heights to an array of the same dimension as the current areas or to a scalar
        '''
        assert heights.shape == self.binsizes.shape or isinstance(heights, numbers.Number)
        self.areas = self.binsizes * heights



    def integral(self, variations=None, **kwargs):
        '''
        Calculate the integral of the histogram.

        :param variations: if given, a tuple of the nominal integral and its upper and lower variation is calculated. \
        This argument is passed to :py:func:`histogram1d.net_variations` and should be a list of considered variation \
        names or the string :code:`'all'`.
        :type variations: :code:`list` of :code:`str` or :code:`str`
        :param **kwargs: additional keyword arguments that get passed to :py:func:`histogram1d.net_variations`

        :returns: the integral (as well as upper and lower variation if :code:`variations` is given)
        :rtype: :code:`float`, or if :code:`variations` are given, :code:`tuple` of nominal as well as upper and lower variation
        '''
        if not variations:
            return np.sum(self.areas)
        one_bin_histogram = deepcopy(self)
        one_bin_histogram.rebin(np.array([self.binedges[0], self.binedges[-1]]))
        up, down = one_bin_histogram.net_variations(variations=variations, **kwargs)
        return self.integral(), up[0], down[0]



    def net_variations(self, variations='all', subtract_nominal=False, relative=False):
        '''
        Return upper and lower net heights variation of the histogram as a tuple.

        @variations should be a sequence of considered variation names or the string 'all'
        @subtract_nominal: if True, return the differences with respect to the nominal heights
        @relative: if True, divide by the nominal heights

        CAUTION: this method cannot yet deal with systematic uncertainties for which the up- and down-shift lie on the same side of the nominal.
        This is because the variations are fundamentally treated independently of each other, so there is no sense of the up- and down-shift
        being related to the same underlying uncertainty source.
        '''
        all_variations = {**self.uncorr_variations, **self.corr_variations} # correlated/uncorrelated only matters for rebinning so far...
        if variations == 'all':
            variations = all_variations.keys()
        if not variations:
            return (np.zeros_like(self.areas), np.zeros_like(self.areas))
        v = np.array([all_variations[name] for name in all_variations if name in variations])
        #print('variations array')
        #print(v)
        shifts = v - self.areas
        lower = self.areas - np.sqrt(np.sum(shifts.clip(max=0)**2, axis=0)) # add negative shifts from nominal in quadrature
        #print('lower')
        #print(lower)
        upper = self.areas + np.sqrt(np.sum(shifts.clip(min=0)**2, axis=0)) # add positive shifts from nominal in quadrature
        #print('upper')
        #print(upper)
        if subtract_nominal:
            lower = lower - self.areas
            upper = upper - self.areas
        if relative:
            # If height == 0, division would give NaN. Using nan_to_num, this is replaced by zero.
            lower = np.nan_to_num(lower / self.areas)
            upper = np.nan_to_num(upper / self.areas)
        return upper, lower



    def errorbars(self, variations='all'):
        '''
        Returns upper and lower error bars, defined as the absolute net variations (taking into account
        the given variations) with the nominal values subtracted.
        '''
        upper, lower = self.net_variations(variations, subtract_nominal=True, relative=False)
        return np.abs(upper)/self.binsizes, np.abs(lower)/self.binsizes



    # Mathematical operations for combining multiple histograms are defined in the following



    def _infer_shift_directions(self, self_shifts, other_shifts):
        '''
        Auxiliary function that infers the direction of shifts when combining them for two histograms

        Robust under some shifts being zero (and hence having no direction, np.sign(0) = 0). This led
        to a bug in the past!
        '''
        self_signs = np.sign(self_shifts)
        other_signs = np.sign(other_shifts)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning) # do not warn about NaNs in the division in the following line
            return np.nan_to_num((self_signs + other_signs) / (np.abs(self_signs) + np.abs(other_signs)))



    def _modify_areas(self, other, operation, symbol):
        '''
        Backend function that internally implements the mathematical operations between two histograms
        Alternatively, @other may be a scalar (float or int)

        NOTE: if @operation is truediv, the bin heights rather than areas are set.

        Behaviour for combining UNCORRELATED uncertainties:

        '''
        scalar = False
        if isinstance(other, (int, float)):
            scalar = True
            other = type(self)(self.binedges, np.zeros_like(self.areas) + other, areas=True, name='{0}'.format(other))
        # NB: array_equal also works for a tuple of Numpy arrays, as we have for a 2D histogram!
        if isinstance(self.binedges, np.ndarray):
            if not np.allclose(self.binedges, other.binedges):
                raise RuntimeError('Cannot perform mathematical operation on histograms, binegdes differ:\n{a}\n{b}'.format(a=self.binedges, b=other.binedges))
        else:
            if not np.allclose(self.binedges[0], other.binedges[0]) or not np.allclose(self.binedges[1], other.binedges[1]):
                raise RuntimeError('Cannot perform mathematical operation on histograms, binegdes differ:\n{a}\n{b}'.format(a=self.binedges, b=other.binedges))
        selfname = '({0})'.format(self.name) if ' ' in self.name else self.name
        othername = '({0})'.format(other.name) if ' ' in other.name else other.name
        resultname = '{0} {1} {2}'.format(selfname, symbol, othername)
        attributes = {**other.attributes, **self.attributes}
        plot_attributes = {**other.plot_attributes, **self.plot_attributes}
        binedges = self.binedges
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning) # do not warn about NaNs in the division in the following line
            areas = operation(self.areas, other.areas)
        # Constructing uncorrelated variations of the new histogram
        uncorr_variations = {}
        if scalar:
            # for name, array in self.uncorr_variations.items():
            #     print(name, array, other.areas, operation(array, other.areas))
            uncorr_variations = {name : operation(array, other.areas) for name, array in self.uncorr_variations.items()}
        elif not operation in [operator.add, operator.sub, operator.truediv]:
            # CAUTION: calculation of uncorrelated uncertainty is not implemented in this case
            pass
        else:
            # TODO: factor this else clause into a separate method!
            all_uncorr_variations = list(set(list(self.uncorr_variations.keys()) + list(other.uncorr_variations.keys())))
            for name in all_uncorr_variations:
                try:
                    self_shifts = self.uncorr_variations[name] - self.areas
                except KeyError:
                    self_shifts = np.zeros_like(self.areas)
                try:
                    other_shifts = other.uncorr_variations[name] - other.areas
                except KeyError:
                    other_shifts = np.zeros_like(other.areas)
                # CAUTION: the direction information (i.e. + or -) of the shifts is lost when summing in quadrature / dividing,
                # so it is ASSUMED that it can be taken from the direction of self_shifts. This is only true if all
                # the direction of a given shift for a given variation is the same for self and other.
                shift_directions = self._infer_shift_directions(self_shifts, other_shifts)
                if operation == operator.truediv:
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore', RuntimeWarning) # do not warn about NaNs in the division in the following line
                        uncorr_variations[name] = areas + shift_directions * np.sqrt((self_shifts / other.areas)**2 + (self.areas * other_shifts / other.areas**2)**2)
                else:
                    uncorr_variations[name] = areas + shift_directions * np.sqrt((self_shifts**2 + other_shifts**2))


        # Constructing correlated variations of the new histogram
        corr_variations = {}
        if scalar:
            corr_variations = {name : operation(array, other.areas) for name, array in self.corr_variations.items()}
        else:
            # TODO: factor this else clause into a separate method!
            all_corr_variations = list(set(list(self.corr_variations.keys()) + list(other.corr_variations.keys())))
            for name in all_corr_variations:
                try:
                    self_var = self.corr_variations[name]
                except KeyError:
                    # this variation was not found for histogram @self, use its nominals instead
                    self_var = self.areas
                try:
                    other_var = other.corr_variations[name]
                except KeyError:
                    # this variation was not found for histogram @other, use its nominals instead
                    other_var = other.areas
                # CAUTION: the direction information (i.e. + or -) of the shifts is lost when summing in quadrature,
                # so it is ASSUMED that it can be taken from the direction of self_shifts. This is only true if all
                # the direction of a given shift for a given variation is the same for self and other.
                corr_variations[name] = operation(self_var, other_var)

        #print('TODO: add support for combining variations in histogram manipulation')
        return type(self)(binedges, areas, name=resultname, areas=True, uncorr_variations=uncorr_variations, corr_variations=corr_variations, attributes=attributes, plot_attributes=plot_attributes)



    def __add__(self, other):
        '''
        Add another histogram or a scalar to this histogram.

        Returns the result of the addition as a histogram.

        Correlated variations are treated as fully correlated among the two histograms if they have the same
        name, otherwise they are treated as uncorrelated. Uncorrelated variations are treated as uncorrelated
        between the two histograms.
        '''
        return self._modify_areas(other, operator.add, '+')

    def __sub__(self, other):
        '''
        Subtract another histogram or a scalar from this histogram.

        Returns the result of the subtraction as a histogram.

        Correlated variations are treated as fully correlated among the two histograms if they have the same
        name, otherwise they are treated as uncorrelated. Uncorrelated variations are treated as uncorrelated
        between the two histograms.
        '''
        return self._modify_areas(other, operator.sub, '-')

    def __mul__(self, other):
        '''
        Multiply another histogram or a scalar binwise with this histogram.

        Returns the result of the binwise multiplication as a histogram.

        Correlated variations are treated as fully correlated among the two histograms if they have the same
        name, otherwise they are treated as uncorrelated. Uncorrelated variations are treated as uncorrelated
        between the two histograms.
        '''
        return self._modify_areas(other, operator.mul, '*')

    def __truediv__(self, other):
        '''
        Divide by another histogram or a scalar binwise.

        Returns the result of the binwise division as a histogram.

        Correlated variations are treated as fully correlated among the two histograms if they have the same
        name, otherwise they are treated as uncorrelated.

        CAUTION: Uncorrelated variations are treated as uncorrelated between the two histograms. If the
        uncorrelated variations represent statistical uncertainties, this means that the division treats
        the two histograms as statistically uncorrelated.

        See also
        :py:func:`histdiv`
        '''
        return self._modify_areas(other, operator.truediv, '/')



    def apply_inplace(self, function, new_binedges=None):
        r'''
        Call a function on the nominal areas as well as all varied areas (in :code:`corr_variations` and :code:`uncorr_variations`),
        modifying the existing histogram.

        It is possible to convert the histogram to a different type (e.g. :py:class:`histogram2d` :math:`\to` :py:class:`histogram1d`)
        by giving new binedges of the desired new dimensionality. If the new binedges have a dimension other than 1D or 2D,
        the type will become :py:class:`basehistogram`.

        For a version of this method that leaves the original histogram unchanged and returns a copy with the function applied (and
        optionally new bin edges), see :py:func:`basehistogram.apply`. I HIGHLY recommend using that if the new histogram will be of
        different type to avoid confusion!

        Caution: if you change the binning, it is your responsibility that uncertainties encoded in the variations are handled correctly.

        :param function: function taking a :code:`numpy.array` as argument
        :type function: :code:`function`
        :param new_binedges: optional argument to set new binedges. If the binedges change the dimension of the histogram (e.g. from 2D to 1D), the histograms' type is changed accordingly
        :type function: :code:`function`

        Example 1: taking the sine of the areas

        .. code-block:: python

            import heppy as hp
            import numpy as np
            foo = hp.histogram1d(np.array([0., 1., 2., 3.]), [5., 6., 7])
            foo.apply_inplace(np.sin)

        Example 2: projecting a 2D histogram to its x-axis (integrating over the y-axis)

        .. code-block:: python

            import heppy as hp
            import numpy as np
            binedges = (np.array([0., 10., 20.]), np.array([10., 20., 30.]))
            areas = [[0.1, 0.2], [0.3, 0.4]]
            foo = hp.histogram2d(binedges, areas, areas=True)
            from functools import partial
            project_x = partial(np.sum, axis=1)
            foo.apply_inplace(project_x, new_binedges=foo.binedges[0])

        :raises: :code:`ValueError` if the shape of the areas after the function is called on them does not match the shape of the bin edges (after setting them to :code:`new_binedges` if given)
        '''
        # Check that the shape of the areas matches the shape of the bin sizes (possibly after changing binning)
        if function(self.areas).shape != (self.binsizes.shape if new_binedges is None else _calculate_bin_sizes(new_binedges).shape):
            raise ValueError('Binedges do not match after applying function to areas')
        change_type = (new_binedges is not None and _calculate_bin_sizes(new_binedges).shape != self.binsizes.shape)
        if new_binedges is not None:
            self.binedges = deepcopy(new_binedges)
        self.areas = function(self.areas)
        for key, areas in self.corr_variations.items():
            self.corr_variations[key] = function(areas)
        for key, areas in self.uncorr_variations.items():
            self.uncorr_variations[key] = function(areas)
        # Cast the histogram to the right type based on what its bin dimensionality is now:
        if change_type:
            args = [self.binedges, self.heights]
            kwargs = {
                'name' : self.name,
                'uncorr_variations' : self.uncorr_variations,
                'corr_variations' : self.corr_variations,
                'attributes' : self.attributes,
                'plot_attributes' : self.plot_attributes,
            }
            if isinstance(new_binedges, np.ndarray):
                self.__class__ = histogram1d
            if isinstance(new_binedges, tuple) and len(new_binedges) == 2:
                self.__class__ = histogram2d
            else:
                self.__class__ = basehistogram



    def apply(self, function, new_binedges=None):
        '''
        Same as :py:func:`basehistogram.apply_inplace`, except that the resulting histogram is returned (as an independent object) with
        the function applied, while the original histogram is not modified.

        :returns: histogram with function applied and possibly new bin edges (:py:class:`histogram1d`, :py:class:`histogram2d`, or :py:class:`basehistogram`)
        '''
        new = deepcopy(self)
        new.apply_inplace(function, new_binedges=new_binedges)
        return new



    def clip(self, minimum=None, maximum=None):
        """Clips the bin areas at a minimum and/or maximum value.

        Similar to ``numpy.clip`` (see `here <https://numpy.org/doc/stable/reference/generated/numpy.clip.html>`_).

        Both the nominals and all correlated and uncorrelated variations of the histogram are clipped.
        *Note that the net variation of multiple individual variations considered together may still lie
        outside of the clip range!*

        :param minimum: minimum accepted value; areas below this value will be set to the value.
        If ``None``, no minimum is imposed.
        :type minimum: ``float`` or ``None``
        :param maximum: maximum accepted value; areas above this value will be set to the value.
        If ``None``, no maximum is imposed.
        :type maximum: ``float`` or ``None``

        The behaviour is like that of ``numpy.clip``, e.g. with regards to what happens if ``minimum`` is
        greater than ``maximum``.

        **"Undocumented" feature:** you can actually pass a Numpy ``array_like`` as ``minimum`` or ``maximum``,
        not just a single ``float``!
        """
        def clip_function(array):
            return np.clip(array, minimum, maximum)
        self.apply_inplace(clip_function)



    def __repr__(self):
        '''
        String representation of the histogram that can be used to recreate it, e.g. with the following code:

        .. code-block:: python

            from heppy import histogram1d
            from numpy import array
            foo = histogram1d(array([0., 1., 2., 3.]), array([5., 6., 7.])) # constructed with arbitrary options
            bar = eval(repr(foo)) # bar is equivalent to foo

        :returns: :code:`str` representation of the object
        '''
        histogram_type = 'histogram1d' if 'histogram1d' in str(type(self)) else 'histogram2d'
        return histogram_type + '(' + ', '.join([
            repr(self.binedges),
            repr(self.areas),
            'areas=True',
            'name={}'.format(repr(self.name)),
            'attributes={}'.format(repr(self.attributes)),
            'plot_attributes={}'.format(repr(self.plot_attributes)),
            'uncorr_variations={}'.format(repr(self.uncorr_variations)),
            'corr_variations={}'.format(repr(self.corr_variations)),
            ]).replace('\n', ' ') + ')'



    def to_file(self, outfilename, key, recreate=False):
        '''
        Write histogram to text file. Multiple histograms with different keys
        can be written to the same file.

        :param outfilename: name of the file that the histogram is written to
        :type outfilename: :code:`str`
        :param key: name/key of the histogram inside the output file
        :type key: :code:`str`
        :param recreate: option to recreate the output file rather than append to it
        :type key: :code:`bool`
        '''
        mode = 'w' if recreate else 'a'
        with open(outfilename, mode) as outfile:
            outfile.write(key + ' : ' + repr(self) + '\n')





class histogram1d(basehistogram):
    '''
    Heppy one-dimensional histogram.
    This has functionality for rebinning, getting various representations for plotting (curve, points, errorbars, errorbands), as well as
    performing mathematical operations (these have only been implemented for one-dimensional histograms so far).
    '''
    def __init__(self, *args, **kwargs):
        super(histogram, self).__init__(*args, **kwargs)



    @property
    def nbins(self):
        """Returns the number of bins in the histogram.

        :returns: number of bins in the histogram
        :rtype: ``int``
        """
        return len(self.binedges) - 1



    @property
    def binwidths(self):
        '''
        Bin widths is an alias for bin sizes in the case of a one-dimensional histogram
        '''
        return super(histogram1d, self).binsizes



    def bin_index(self, x):
        """Returns the index of the bin that contains the given x-value.

        Lower bin edges are included in a bin, upper bin edges are excluded (same as in the `ROOT <https://root.cern>`_ convention).

        :param x: x-value
        :type x: ``float``

        :returns: index of bin that contains the x-value
        :rtype: ``int``

        :raises ValueError: if x-value lies outside of the outer bin edges of the histogram

        Example:

        .. code-block:: python

            >>> h = histogram1d([0., 1., 2.], [10., 11.])
            >>> h.bin_index(0.5)
            0
            >>> h.bin_index(0.)
            0
            >>> h.bin_index(1.0)
            1
            >>> h.bin_index(2.0)
            ValueError: Cannot find index of bin containing x = 2.0, which is outside of histogram x-boundaries [0.0, 2.0)
            >>> h.bin_index(-1.0)
            ValueError: Cannot find index of bin containing x = -1.0, which is outside of histogram x-boundaries [0.0, 2.0)

        """
        return _get_bin_index(self.binedges, x, label='x')



    def curve(self, variation=''):
        '''
        Curve representation of histogram
        @variation: if given, return the curve for the variation of this name. Otherwise, return the nominal curve
        '''
        x = np.repeat(self.binedges, 2)[1:-1]
        y = np.repeat(self.heights, 2)
        return (x, y)



    def points(self, variation='', shift=0., abs_shift=False):
        '''
        Point representation of histogram
        If @shift is given, the x-coordinates of the midpoints are given shifted by this absolute x-value (if @abs_shift=True) or relative fraction of the corresponding bin's width (if @abs_shift=False)
        '''
        midx = self.binedges[:-1] + 0.5 * self.binsizes
        if abs_shift:
            midx = midx + shift
        else:
            midx = midx + shift * self.binsizes
        return (midx, self.heights)



    def errorband(self, *args, **kwargs):
        '''
        Basically same as errorbars method, only in curve representation
        @*args and @**kwargs get passed on to self.net_variations()
        '''
        upper, lower = self.net_variations(*args, **kwargs)
        x = np.repeat(self.binedges, 2)[1:-1]

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning) # do not warn about NaNs in the division in the following line
            yupper = np.repeat(upper/self.binsizes, 2)
            ylower = np.repeat(lower/self.binsizes, 2)
            return x, yupper, ylower



    def _recalculate_variation_areas_quadsum(self, var_areas, newedges):
        sign = np.sign(np.sum(var_areas) - np.sum(self.areas)) # infer the direction of the shifts
        shifts = var_areas - self.areas
        return np.sqrt(np.add.reduceat(shifts**2, np.searchsorted(self.binedges, newedges)[:-1])) * sign + \
               np.add.reduceat(self.areas, np.searchsorted(self.binedges, newedges)[:-1])



    def rebin(self, newedges):
        '''
        Rebin to @newedges
        Each element of @newedges should correspond to an existing binedge, i.e. only existing bins are merged

        CAUTION: currently ASSUMES that each uncorrelated variation only has shifts in one direction of the nominal
        (i.e. it is either higher or lower everywhere)!
        '''
        if isinstance(newedges, list):
            newedges = np.array(newedges)
        # First altogether drop bins that are outside of the outermost new edges:
        min_index = self.bin_index(np.min(newedges))
        max_index = None if np.max(newedges) == np.max(self.binedges) else self.bin_index(np.max(newedges))
        if min_index > 0 or max_index is not None:
            self.uncorr_variations = {name : areas[min_index:max_index] for name, areas in self.uncorr_variations.items()}
            self.corr_variations = {name : areas[min_index:max_index] for name, areas in self.corr_variations.items()}
            self.areas = self.areas[min_index:max_index]
            self.binedges = self.binedges[min_index:None] if max_index is None else self.binedges[min_index:max_index+1]
        # CAUTION: the order of rebinning variations, binedges, and areas matters here!
        self.uncorr_variations = {name : self._recalculate_variation_areas_quadsum(areas, newedges) for name, areas in self.uncorr_variations.items()}
        self.corr_variations = {name : np.add.reduceat(areas, np.searchsorted(self.binedges, newedges)[:-1]) for name, areas in self.corr_variations.items()}
        self.areas = np.add.reduceat(self.areas, np.searchsorted(self.binedges, newedges)[:-1])
        self.binedges = np.take(self.binedges, np.searchsorted(self.binedges, newedges))



    def merge_bins(self, xmin, xmax):
        '''
        Merge the bins falling into the given x-range into one bin
        '''
        if xmin >= xmax:
            raise RuntimeError('Must have xmin < xmax for merging histogram bins')
        newedges = np.concatenate((self.binedges[self.binedges <= xmin], self.binedges[self.binedges >= xmax]))
        if xmax > np.max(self.binedges): np.append(newedges, np.max(self.binedges)) # so that the highest bin edge stays intact even when xmax is greater than it
        self.rebin(newedges)



    def squash_highest_bin(self, squash_above, new_xmax):
        '''
        Merge all bins from @squash_above upwards and set the highest bin edge to @new_xmax.

        Does nothing if squash_above is >= the highest bin edge.
        '''
        if squash_above >= new_xmax:
            raise RuntimeError('Setting new highest bin edge above the bin squashing threshold is forbidden')
        if squash_above >= np.max(self.binedges):
            return
        self.merge_bins(squash_above, np.max(self.binedges))
        # Only now update binedges:
        self.binedges[-1] = new_xmax



    def height(self, bin_index):
        """Returns the height of the given bin index with uncertainties.

        :returns: height of the indexed bin including its variations
        :rtype: :py:class:`heppy.value`

        Usage example:

        .. code-block:: python

            >>> import heppy as hp
            >>> h = hp.histogram1d([0., 1., 3.], [10., 11.], corr_variations={'systematic__up' : [13., 11.5]})
            >>> v = h.height(1)
            >>> v.nominal
            11.0
            >>> v.corr_variations['systematic__up']
            11.5

        """
        uncorr_variations = {key : (values/self.binwidths)[bin_index] for key, values in self.uncorr_variations.items()}
        corr_variations = {key : (values/self.binwidths)[bin_index] for key, values in self.corr_variations.items()}
        return Value(self.heights[bin_index], uncorr_variations=uncorr_variations, corr_variations=corr_variations)



    def iterheights(self):
        """Generates iterator over heights.

        :returns: bin heights including their variations
        :rtype: :py:class:`heppy.value`

        Usage example:

        .. code-block:: python

            >>> import heppy as hp
            >>> h = hp.histogram1d([0., 1., 3.], [10., 11.], corr_variations={'systematic__up' : [13., 11.5]})
            >>> for height in h.iterheights(): print(height.nominal, height.corr_variations['systematic__up'])
            10.0 13.0
            11.0 11.5

        """
        for bin_index in range(self.nbins):
            yield self.height(bin_index)



    def iterbins(self):
        """Generates iterator over bins, yielding bin edges and heights.

        :returns: bin egdes and nominal bin height
        :rtype: ``tuple`` of the following: ``tuple`` of two ``float``, and one ``float``

        Usage example:

        .. code-block:: python

            >>> import heppy as hp
            >>> h = hp.histogram1d([0., 1., 3.], [10., 11.], corr_variations={'systematic__up' : [13., 11.5]})
            >>> for binedges, height in h.iterbins(): print(binedges, height.nominal)
            (0.0, 1.0) 10.0
            (1.0, 3.0) 11.0
            >>> for binedges, height in h.iterbins(): print(binedges, height.nominal, height.corr_variations['systematic__up'])
            (0.0, 1.0) 10.0 13.0
            (1.0, 3.0) 11.0 11.5

        """
        for bin_lower_edge, bin_upper_edge, height in zip(self.binedges[:-1], self.binedges[1:], self.iterheights()):
            yield (bin_lower_edge, bin_upper_edge), height



    def cumulative(self, side='left', nan_to_num=True):
        """Returns a new histogram containing the cumulative sums of the bin areas.

        Analogous to Numpy's ``cumsum`` function.

        Note: the plot attributes are copied over from ``self`` to the returned
        histogram.


        :param side: which side to integrate from, may be either ``'left'`` or ``'right'``
        :type side: ``str``
        :param nan_to_num: treat NaN as 0 when taking the cumulative sum?
        :type nan_to_num: ``bool``

        :returns: histogram of the cumulative sum of the bin areas
        :rtype: :py:class:`heppy.histogram1d`
        """
        areas = deepcopy(self.areas)
        if nan_to_num:
            areas = np.nan_to_num(areas)
        if side == 'left':
            cumheights = np.cumsum(areas)
        elif side == 'right':
            cumheights = np.cumsum(areas[::-1])[::-1]
        else:
            raise RuntimeError('Argument "side" must be either "left" or "right".')
        return histogram1d(self.binedges, cumheights, areas=False, plot_attributes=self.plot_attributes)



    def to_yoda(self, identifier, metadata={}):
        """Returns the histogram in YODA output format as a string.

        See the websites of `YODA <https://yoda.hepforge.org>`_ and its main user `Rivet <https://rivet.hepforge.org>`_ for more information.

        :param identifier: in-file identifier for the histogram, e.g. ``'/REF/ATLAS_2017_I1614149/d16-x01-y02'``
        :type identifier: ``str``
        :param metadata: optional dictionary of metadata. E.g. for Rivet use, one could have ``metadata = {'IsRef' : 1, 'Path' : '/REF/ATLAS_2017_I1614149/d16-x01-y02', 'Title' : 'doi:10.17182/hepdata.80041.v2/t16'}``
        :type metadata: ``dict``

        :returns: histogram formatted as YODA input string
        :rtype: ``str``

        .. todo::

            Add Variations and ErrorBreakdown fields

            Unit test this method

        """
        template = dedent('''\
        BEGIN YODA_SCATTER2D_V2 {identifier}
        {metadata}
        Type: Scatter2D
        ---
        {data}
        END YODA_SCATTER2D_V2
        ''')
        xval, yval = self.points()
        xerr_minus = xval - self.binedges[:-1]
        xerr_plus = self.binedges[1:] - xval
        yerr_plus, yerr_minus = self.errorbars()
        yerr_plus = np.abs(yerr_plus)
        yerr_minus = np.abs(yerr_minus)
        data_dict = {
            '# xval' : xval,
            'xerr-' : xerr_minus,
            'xerr+' : xerr_plus,
            'yval' : yval,
            'yerr-' : yerr_minus,
            'yerr+' : yerr_plus,
        }
        data = pd.DataFrame.from_dict(data_dict)
        return template.format(
            identifier=identifier,
            metadata='\n'.join(['{key}: {val}'.format(key=key, val=val) for key, val in metadata.items()]),
            data=data.to_string(index=False))



    to_rivet = to_yoda



    def to_root(self, nominal_label='nominal', key_form='{name}_{variation}', errors=None):
        """Returns a dictionary of variation names mapped to ROOT TH1D's.

        :param nominal_label: dictionary key to give to the nominal histogram
        :type nominal_label: ``str``
        :param key_form: template for keys in the returned dictionary. The
            names of the histograms will also be set to these values. It accepts
            the formatting fields `name` (for `self.name`) and variation (for
            the name of the variation)
        :type key_form: ``str``
        :param errors: optional array of bin errors. Must have the same dimensionality
        as the histogram areas. Note that the same errors are used for all variation
        histograms.
        :type errors: ``np.array`` or ``None``

        :returns: dictionary of ROOT histograms (values) mapped by variation
            name (keys)
        :rtype: ``dict`` of ``str`` and ``ROOT.TH1D``
        """
        import ROOT
        import root_numpy as rnp
        from array import array
        def to_th1(name, binedges, areas):
            th1 = ROOT.TH1D(name, name, len(binedges)-1, array('d', [b for b in binedges]))
            rnp.array2hist(areas, th1, errors=errors)
            return th1
        th1s = {}
        # Add nominal
        key = key_form.format(name=self.name, variation=nominal_label)
        th1s[key] = to_th1(key, self.binedges, self.areas)
        for variation, areas in {**self.uncorr_variations, **self.corr_variations}.items():
            key = key_form.format(name=self.name, variation=variation)
            th1s[key] = to_th1(key, self.binedges, areas)
        return th1s



    def to_root_file(self, filename, recreate=False, **kwargs):
        """Writes this histogram to a ROOT file as a set of TH1D's.

        :param filename: name or path to the ROOT file. May exist or not.
        :type filename: ``str``
        :param recreate: only has an effect if the ROOT file exists already. If
            `True`, it will be overwritten. Otherwise, the new histograms will
            be added to the existing file.
        :type recreate: ``bool``
        :param **kwargs: keyword arguments that get passed on to
            :py:func:`histogram1d.to_root`
        """
        import ROOT
        mode = 'RECREATE' if recreate else 'UPDATE'
        rootfile = ROOT.TFile(filename, mode)
        if not rootfile.IsOpen():
            raise OSError(f'Cannot open ROOT file "{filepath}"')
        th1s = self.to_root(**kwargs)
        for key, th1 in th1s.items():
            th1.Write(key)





def zeros_like(a, name=None):
    '''
    Returns a histogram of zeros with the same bin edges and variations as ``a``.

    The attributes and plot attributes are not kept.

    :param a: the bin edges and variation names of ``a`` define these same
    attributes of the returned histogram.
    :type a: :py:class:`heppy.histogram1d` or :py:class:`heppy.histogram2d`
    :param name: if given, this becomes the name attribute of the returned
    histogram. If ``Non``, the returned histogram has the name ``"zeros like " + a.name``
    :type name: ``str`` or ``None``

    :returns: :py:class:`heppy.histogram1d` or :py:class:`heppy.histogram2d`
    '''
    b = deepcopy(a)
    zeros = np.zeros_like(a.areas)
    b.areas = np.zeros_like(a.areas)
    for variation in b.uncorr_variations.keys():
        b.uncorr_variations[variation] = np.zeros_like(a.areas)
    for variation in b.corr_variations.keys():
        b.corr_variations[variation] = np.zeros_like(a.areas)
    b.name = f'zeros like {a.name}' if name is None else name
    b.attributes = {}
    b.plot_attributes = {}
    return b





def from_file(infilename, key):
    '''
    Read histogram written out by heppy (using :py:class:`heppy.basehistogram.to_file`).

    :param infilename: name of the file that the histogram should be read from
    :type infilename: :code:`str`
    :param key: name/key of the histogram inside the input file
    :type key: :code:`str`

    :returns: :py:class:`heppy.histogram1d` or :py:class:`heppy.histogram2d`
    '''
    with open(infilename, 'r') as infile:
        sep = ' : '
        for line in infile:
            if line.split(sep)[0] == key:
                from numpy import array, nan, inf
                return eval(line.split(sep)[1])
        raise RuntimeError('Could not find histogram key "{key}" in input file "{infilename}"'.format(key=key, infilename=infilename))





def histdiv(a, b, corr=None, ignore_denominator_uncertainty=False):
    '''
    Sophisticated division of two histograms

    :param a: numerator histogram
    :type a: :py:class:`heppy.basehistogram`
    :param b: denominator histogram
    :type b: :py:class:`heppy.basehistogram`
    :param corr: information on how a and b are correlated --- NOT YET IMPLEMENTED, do not use
    :param ignore_denominator_uncertainty: switch to ignore the variations of the denominator histogram. If True, divide all variations of the numerator histogram by the nominal denominator histogram.
    :type ignore_denominator_uncertainty: :code:`bool`

    NOTE: the returned ratio histogram's bin heights are not given "per bin size", but take the role that the areas have for histograms that do not represent a ratio.

    :returns: ratio histogram a/b with variations treated as specified
    :raises NotImplementedError: if :code:`corr` is not :code:`None` (remains to be implemented)
    '''
    if ignore_denominator_uncertainty:
        b_no_uncertainty = deepcopy(b)
        b_no_uncertainty.uncorr_variations = {}
        b_no_uncertainty.corr_variations = {}
        r = a / b_no_uncertainty
    else:
        r = a / b
    # Undo division by bin sizes (areas=False):
    r = type(a)(r.binedges, r.areas, areas=False, name=r.name, uncorr_variations=r.uncorr_variations, corr_variations=r.corr_variations, attributes=r.attributes, plot_attributes=r.plot_attributes)
    if isinstance(corr, str) and corr.startswith('subset-toys'):
        ntoys = int(corr.split('-')[-1])
        if (ntoys < 100):
            print('Warning: it is not recommended to use ntoys < 100! Uncertainty propagation will be inaccurate, including due to internal mechanism for dealing with bins in which numerator == denominator!')
        both = a.areas
        denonly = b.areas - a.areas
        if (denonly < 0).any():
            raise RuntimeError('Numerator is not a subset of denominator! Cannot use this uncertainty propagation method.')
        both_toys = np.random.poisson(both, (ntoys, *both.shape))
        denonly_toys = np.random.poisson(denonly, (ntoys, *both.shape))
        ratio_toys = both_toys / (both_toys + denonly_toys)
        #
        # Compute final uncertainty as RMS distance from nominal (up and down separately)
        #
        shift_toys = ratio_toys - r.heights
        upshift_toys = np.clip(shift_toys, 0.0, None)
        downshift_toys = np.clip(shift_toys, None, 0.0)
        # Need the effective number of toys separately for up and down
        # To get it, we just count how many down and how many up fluctuations we had in each bin
        n_effective_toys_up = np.sum(np.ceil(upshift_toys), axis=0)
        n_effective_toys_down = np.sum(np.ceil(np.abs(downshift_toys)), axis=0)
        # Note that in each bin, n_effective_toys_up and n_effective_toys_down sum to either ntoys or zero
        # The latter happens if the numerator and denominator hists have exactly the same entries, and hence
        # will fluctuate coherently and not incur any uncertainty
        # To avoid dividing by zero in such cases, we set them to 1. It doesn't matter what we set them to,
        # since the uncertainties will anyway be zero in these bins.
        n_effective_toys_up = np.clip(n_effective_toys_up, 1.0, None)
        n_effective_toys_down = np.clip(n_effective_toys_down, 1.0, None)
        r.uncorr_variations['Statistical__1up'] = r.areas + np.sqrt(np.sum(upshift_toys**2, axis=0) / n_effective_toys_up) * r.binsizes
        r.uncorr_variations['Statistical__1down'] = r.areas - np.sqrt(np.sum(downshift_toys**2, axis=0) / n_effective_toys_down) * r.binsizes
    elif corr is not None:
        raise NotImplementedError('Division of histograms that are not statistically independent still needs to be implemented.')
    return r





# Convenience alias
histogram = histogram1d





class histogram2d(basehistogram):
    '''
    Heppy two-dimensional histogram.
    This currently has much more limited functionality than the 1D histogram class, although probably
    most (if not all) of the former's mathematical operations should also work for the 2D histogram
    (at least with minor modifications).

    Note: only independent binnings of the two axes are supported (i.e. y-bins don't depend on x-bins and
    vice versa).
    '''
    def __init__(self, *args, **kwargs):
        super(histogram2d, self).__init__(*args, **kwargs)



    @property
    def nbins(self):
        '''
        :returns: tuple of number of bins along x- and y-axis
        '''
        return len(self.binedges[0]) - 1, len(self.binedges[1]) - 1



    def bin_index_x(self, x):
        """Returns the index of the x-axis bin that contains the given x-value.

        Lower bin edges are included in a bin, upper bin edges are excluded (same as in the `ROOT <https://root.cern>`_ convention).

        :param x: x-value
        :type x: ``float``

        :returns: index of x-axis bin that contains the x-value
        :rtype: ``int``

        :raises ValueError: if x-value lies outside of the outer bin edges of the histogram
        """
        return _get_bin_index(self.binedges[0], x, label='x')



    def bin_index_y(self, y):
        """Returns the index of the y-axis bin that contains the given y-value.

        Lower bin edges are included in a bin, upper bin edges are excluded (same as in the `ROOT <https://root.cern>`_ convention).

        :param y: y-value
        :type y: ``float``

        :returns: index of y-axis bin that contains the y-value
        :rtype: ``int``

        :raises ValueError: if y-value lies outside of the outer bin edges of the histogram
        """
        return _get_bin_index(self.binedges[1], y, label='y')



    def points(self):
        '''
        Point representation of 2D histogram.

        This involves flattening/ravelling the histogram bin midpoints and heights to one-dimensional arrays.
        The flattening is done in row-major, C-style order, with the y-axis index changing fastest and the
        x-axis index changing slowest.

        :returns: :code:`tuple` of x-axis bin midpoints, y-axis bin midpoints, and heights
        '''
        binedges_x, binedges_y = self.binedges
        # Calculate bin midpoints in the x and the y direction
        mid_x = binedges_x[:-1] + 0.5 * _calculate_bin_sizes(binedges_x)
        mid_y = binedges_y[:-1] + 0.5 * _calculate_bin_sizes(binedges_y)
        # Now we need to repeat the mid_x and mid_y elements such that they match the
        # raveled heights
        # The y bin changes faster than the x bin
        nbins_x, nbins_y = self.nbins
        expanded_mid_x = np.repeat(mid_x, nbins_y)
        expanded_mid_y = np.tile(mid_y, nbins_x)
        expanded_heights = np.ravel(self.heights)
        return expanded_mid_x, expanded_mid_y, expanded_heights



    def _recalculate_variation_areas_quadsum(self, var_areas, newedges):
        sign = np.sign(np.sum(var_areas) - np.sum(self.areas)) # infer the direction of the shifts
        shifts = var_areas - self.areas
        nominal = self.areas.copy() # Nominal areas to be rebinned along with the variation shifts
        for index in [0, 1]:
            # print(self.binedges[index])
            # print(newedges[index])
            shifts = sign * np.sqrt(np.add.reduceat(shifts**2, np.searchsorted(self.binedges[index], newedges[index])[:-1], axis=index))
            nominal = np.add.reduceat(nominal, np.searchsorted(self.binedges[index], newedges[index])[:-1], axis=index)
        return nominal + shifts



    def rebin(self, newedges):
        '''
        Rebin 2D histogram. Correlated and uncorrelated variations will be recalculated to match the new bin edges.

        CAUTION: currently ASSUMES that each uncorrelated variation only has shifts in one direction of the nominal
        (i.e. it is either higher or lower everywhere)!

        :param newedges: new bin edges. Each new bin edge should correspond to an existing bin edge, i.e. only existing bins are merged
        :type newedges: :code:`tuple` of two :code:`numpy.array`

        :raises: :code:`ValueError` if newedges is not of the correct type
        '''
        if not isinstance(newedges, tuple) or not len(newedges) == 2 or not all([isinstance(e, np.ndarray) for e in newedges]):
            raise ValueError('Argument "newedges" must be a 2-tuple of Numpy arrays')
        # Rebin along one axis after the other --- the order does not matter!
        # (Ensure that the order indeed does not matter when dealing with uncorrelated uncertainties,
        # there may be caveats?)
        self.binedges = list(self.binedges) # make binedges (tuple!) mutable by converting it to a list temporarily...
        # First altogether drop bins that are outside of the outermost new edges:
        for index in [0, 1]:
            bin_index_function = [self.bin_index_x, self.bin_index_y][index]
            min_index = bin_index_function(np.min(newedges[index]))
            max_index = None if np.isclose(np.max(newedges[index]), np.max(self.binedges[index])) else bin_index_function(np.max(newedges[index]))
            if min_index > 0 or max_index is not None:
                if index == 0:
                    self.uncorr_variations = {name : areas[min_index:max_index,:] for name, areas in self.uncorr_variations.items()}
                    self.corr_variations = {name : areas[min_index:max_index,:] for name, areas in self.corr_variations.items()}
                    self.areas = self.areas[min_index:max_index,:]
                else:
                    self.uncorr_variations = {name : areas[:,min_index:max_index] for name, areas in self.uncorr_variations.items()}
                    self.corr_variations = {name : areas[:,min_index:max_index] for name, areas in self.corr_variations.items()}
                    self.areas = self.areas[:,min_index:max_index]
                self.binedges[index] = self.binedges[index][min_index:None] if max_index is None else self.binedges[index][min_index:max_index+1]
        self.uncorr_variations = {name : self._recalculate_variation_areas_quadsum(areas, newedges) for name, areas in self.uncorr_variations.items()}
        for index in [0, 1]:
            # CAUTION: the order of rebinning variations, binedges, and areas matters here!
            self.corr_variations = {name : np.add.reduceat(areas, np.searchsorted(self.binedges[index], newedges[index])[:-1], axis=index) for name, areas in self.corr_variations.items()}
            self.areas = np.add.reduceat(self.areas, np.searchsorted(self.binedges[index], newedges[index])[:-1], axis=index)
            self.binedges[index] = np.take(self.binedges[index], np.searchsorted(self.binedges[index], newedges[index]))
        self.binedges = tuple(self.binedges) # convert binedges back to tuple



    def as_1d(self, name=''):
        '''
        Return a copied one-dimensional reinterpretation of this histogram.
        This only works if the histogram only has one bin in one of its dimensions. This dimension will
        then be ignored.

        :param name: name for the reinterpreted histogram
        :type name: :code:`str`
        '''
        kept_axis = None
        if len(self.binedges[0]) == 2:
            kept_axis = 1
        elif len(self.binedges[1]) == 2:
            kept_axis = 0
        if kept_axis is None:
            raise ValueError('Cannot reinterpret 2D histogram as 1D histogram, since neither of its axes has only one bin')
        binedges = self.binedges[kept_axis]
        areas = self.areas.flatten(order='C') # or 'F'
        cv = {key : areas.flatten(order='C') for key, areas in self.corr_variations.items()}
        uv = {key : areas.flatten(order='C') for key, areas in self.uncorr_variations.items()}
        return histogram1d(binedges, areas, areas=True, name=name, corr_variations=cv, uncorr_variations=uv, attributes=self.attributes, plot_attributes=self.plot_attributes)



    def project(self, axis, name=''):
        '''
        Project histogram to one axis by integrating over the other. Correlated and uncorrelated
        uncertainties are computed for the resulting one-dimensional histogram.

        :param axis: which axis to project onto, i.e. the *axis that is kept*
        :type axis: :code:`'x'` or :code:`'y'`

        :param name: name for the projection histogram
        :type name: :code:`str`


        :returns: :py:class:`heppy.histogram1d` representing the projection

        :raises: :code:`ValueError` if invalid axis identifier is given
        '''
        if not axis in ['x', 'y']:
            raise ValueError('Invalid axis "{axis}", valid choices are: "x", "y"'.format(axis=axis))
        binedge_index = {'x' : 0, 'y' : 1}[axis]
        # Rebin the histogram to (2D) new edges such that there is only one bin in the projected-out
        # dimension:
        newedges_x = self.binedges[0] if axis == 'x' else np.array([self.binedges[0][0], self.binedges[0][-1]])
        newedges_y = self.binedges[1] if axis == 'y' else np.array([self.binedges[1][0], self.binedges[1][-1]])
        newedges = (newedges_x, newedges_y)
        projected = deepcopy(self)
        projected.rebin(newedges)
        if name == '':
            name = self.name + ' projected to {axis}-axis'.format(axis=axis)
        return projected.as_1d(name=name)



    def slice(self, axis, bin_index, name=''):
        """Returns 1D histogram of the distribution along one axis in a given bin of the other axis.

        :param axis: axis along which the slicing is done, i.e. the *axis that is kept*
        :type axis: :code:`'x'` or :code:`'y'`

        :param bin_index: index of the bin on the *axis that is not kept*
        :type bin_index: ``int``

        :param name: name for the slice histogram
        :type name: ``str``


        :returns: 1D histogram of the slice
        :rtype: :py:class:`heppy.histogram1d`
        """
        if not axis in ['x', 'y']:
            raise ValueError('Invalid axis "{axis}", valid choices are: "x", "y"'.format(axis=axis))
        other_axis = {'x' : 'y', 'y' : 'x'}[axis]
        binedge_index = {'x' : 0, 'y' : 1}[other_axis]
        bin_lower_edge = self.binedges[binedge_index][bin_index]
        bin_upper_edge = self.binedges[binedge_index][bin_index+1]
        # The actual slicing happens below.
        # The strategy is to rebin a copy of the 2D histogram such that the bins in the
        # ``axis``-direction are kept while only one bin in the ``other_axis``-direction
        # is kept. The resulting 2D histogram is then cast to a 1D histogram.
        sliced = deepcopy(self)
        newedges = {
            'x' : (sliced.binedges[0], np.array([bin_lower_edge, bin_upper_edge])),
            'y' : (np.array([bin_lower_edge, bin_upper_edge]), sliced.binedges[1]),
            }[axis]
        sliced.rebin(newedges)
        if name == '':
            name = self.name + ' slice along {axis}-axis in {other_axis}-bin [{binmin}, {binmax})'.format(axis=axis, other_axis=other_axis, binmin=bin_lower_edge, binmax=bin_upper_edge)
        return sliced.as_1d(name=name)



    def height(self, bin_index_x, bin_index_y):
        """Returns the height of the given bin indices with uncertainties.

        :param bin_index_x: bin index along x-axis
        :param bin_index_x: ``int``
        :param bin_index_y: bin index along y-axis
        :param bin_index_y: ``int``

        :returns: height of the indexed bin including its variations
        :rtype: :py:class:`heppy.value`
        """
        uncorr_variations = {key : (values/self.binsizes)[bin_index_x,bin_index_y] for key, values in self.uncorr_variations.items()}
        corr_variations = {key : (values/self.binsizes)[bin_index_x,bin_index_y] for key, values in self.corr_variations.items()}
        return Value(self.heights[bin_index_x,bin_index_y], uncorr_variations=uncorr_variations, corr_variations=corr_variations)



    def iterheights(self, faster='y'):
        """Generates iterator over heights.

        :param faster: controls the iteration order by specifying along which axis the bin index changes faster
        :type faster: ``str``; ``'x'`` or ``'y'``

        :returns: bin heights including their variations
        :rtype: :py:class:`heppy.value`
        """
        if not faster in ('x', 'y'):
            raise ValueError('Valid values for keyword argument "faster" are: "x", "y"')
        nbins_x, nbins_y = self.nbins
        if faster == 'y':
            for bin_index_x in range(nbins_x):
                for bin_index_y in range(nbins_y):
                    yield self.height(bin_index_x, bin_index_y)
        elif faster == 'x':
            for bin_index_y in range(nbins_y):
                for bin_index_x in range(nbins_x):
                    yield self.height(bin_index_x, bin_index_y)



    def iterbins(self):
        """Generates iterator over bins, yielding bin edges and heights.

        :returns: x-axis bin egdes, y-axis bin edges, and bin height with variations
        :rtype: ``tuple`` of the following: ``tuple`` of two ``float``, ``tuple`` of two ``float``, and one :py:class:`heppy.value`

        Usage example:

        .. code-block:: python

            >>> import heppy as hp
            >>> import numpy as np
            >>> heights = np.array([             # bin heights
                    [1., 5.],
                    [2., 6.],
                    [3., 7.],
                    ])
            >>> x = np.array([-7., 0., 5., 50.]) # bin edges in x
            >>> y = np.array([-1., 0., 1.])      # bin edges in y
            >>> h = hp.histogram2d((x, y), heights)
            >>> for binedges_x, binedges_y, height in h.iterbins(): print(binedges_x, binedges_y, height.nominal)
            (-7.0, 0.0) (-1.0, 0.0) 1.0
            (-7.0, 0.0) (0.0, 1.0) 5.0
            (0.0, 5.0) (-1.0, 0.0) 2.0
            (0.0, 5.0) (0.0, 1.0) 6.0
            (5.0, 50.0) (-1.0, 0.0) 3.0
            (5.0, 50.0) (0.0, 1.0) 7.0

        """
        nbins_x, nbins_y = self.nbins
        binedges_x, binedges_y = self.binedges
        bin_lower_edges_x = np.repeat(binedges_x[:-1], nbins_y)
        bin_upper_edges_x = np.repeat(binedges_x[1:], nbins_y)
        bin_lower_edges_y = np.tile(binedges_y[:-1], nbins_x)
        bin_upper_edges_y = np.tile(binedges_y[1:], nbins_x)
        for bin_lower_edge_x, bin_upper_edge_x, bin_lower_edge_y, bin_upper_edge_y, height in zip(bin_lower_edges_x, bin_upper_edges_x, bin_lower_edges_y, bin_upper_edges_y, self.iterheights(faster='y')):
            yield (bin_lower_edge_x, bin_upper_edge_x), (bin_lower_edge_y, bin_upper_edge_y), height



    def to_root(self, nominal_label='nominal', key_form='{name}_{variation}', errors=None):
        """Returns a dictionary of variation names mapped to ROOT TH2D's.

        :param nominal_label: dictionary key to give to the nominal histogram
        :type nominal_label: ``str``
        :param key_form: template for keys in the returned dictionary. The
            names of the histograms will also be set to these values. It accepts
            the formatting fields `name` (for `self.name`) and variation (for
            the name of the variation)
        :type key_form: ``str``
        :param errors: optional array of bin errors. Must have the same dimensionality
        as the histogram areas. Note that the same errors are used for all variation
        histograms.
        :type errors: ``np.array`` or ``None``


        :returns: dictionary of ROOT histograms (values) mapped by variation
            name (keys)
        :rtype: ``dict`` of ``str`` and ``ROOT.TH2D``
        """
        import ROOT
        import root_numpy as rnp
        from array import array
        def to_th2(name, binedges, areas):
            th2 = ROOT.TH2D(name, name, len(binedges[0])-1, array('d', [b for b in binedges[0]]), len(binedges[1])-1, array('d', [b for b in binedges[1]]))
            rnp.array2hist(areas, th2, errors=errors)
            return th2
        th2s = {}
        # Add nominal
        key = key_form.format(name=self.name, variation=nominal_label)
        th2s[key] = to_th2(key, self.binedges, self.areas)
        for variation, areas in {**self.uncorr_variations, **self.corr_variations}.items():
            key = key_form.format(name=self.name, variation=variation)
            th2s[key] = to_th2(key, self.binedges, areas)
        return th2s



    def to_root_file(self, filename, recreate=False, **kwargs):
        """Writes this histogram to a ROOT file as a set of TH2D's.

        :param filename: name or path to the ROOT file. May exist or not.
        :type filename: ``str``
        :param recreate: only has an effect if the ROOT file exists already. If
            `True`, it will be overwritten. Otherwise, the new histograms will
            be added to the existing file.
        :type recreate: ``bool``
        :param **kwargs: keyword arguments that get passed on to
            :py:func:`histogram2d.to_root`
        """
        import ROOT
        mode = 'RECREATE' if recreate else 'UPDATE'
        rootfile = ROOT.TFile(filename, mode)
        if not rootfile.IsOpen():
            raise OSError(f'Cannot open ROOT file "{filepath}"')
        th2s = self.to_root(**kwargs)
        for key, th2 in th2s.items():
            th2.Write(key)



class histostack(object):
    '''
    Stack of one-dimensional histograms

    :param histograms: histograms in the stack
    :type histograms: :code:`list` of :py:class:`heppy.histogram1d`
    :param attributes: dictionary of completely arbitrary attributes that the user can provide/change/access. E.g. information on how to plot
    :type attributes: :code:`dict`
    '''
    def __init__(self, histograms, attributes={}):
        super(histostack, self).__init__()
        self.histograms = histograms
        self.attributes = attributes

    @property
    def total(self):
        '''
        :returns: :py:class:`heppy.histogram1d` that is the combination of all the stacked ones, with the combined uncertainty. If the stack has no histograms, returns :code:`None`
        '''
        if not self.histograms: return None
        try:
            return sum(self.histograms[1:], self.histograms[0])
        except IndexError:
            return self.histograms[0]

    def iterbands(self):
        '''
        Bands are 3-tuples of (curve representation) x-values as well as two subsequent curves that are useful as arguments to :code:`plt.fill_between()`.
        E.g.:

        .. code-block:: python

            for histogram, band in zip(stack.histograms, stack.iterbands()):
                ax.fill_between(*band, **histogram.attributes)

        The bands are ordered such that the first histogram in the stack is at the top and the last at the bottom
        '''
        if not self.histograms:
            return
        (x, y) = self.histograms[0].curve()
        bottom = np.zeros_like(y)
        bands = []
        for histo in reversed(self.histograms):
            top = bottom + histo.curve()[1]
            bands.append((x, bottom, top))
            bottom = top
        for band in reversed(bands): # Storing the bands first and looping over them again in reversed order means that the topmost histogram has the first colour
            yield band
