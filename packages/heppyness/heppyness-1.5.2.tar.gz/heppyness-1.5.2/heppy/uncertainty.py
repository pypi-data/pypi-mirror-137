import numpy as np
from copy import deepcopy
import fnmatch
import matplotlib.pyplot as plt
from itertools import groupby
import os
from textwrap import dedent
from .histogram import histogram1d as _histogram1d
from .histogram import histogram2d as _histogram2d
from .heatmap import _make_text, _map_to_equispaced
from matplotlib.colors import Normalize



def _make_1d_controlplot(histogram, nominal, reference, array, keys, var_hi, var_lo, path):
    """Helper function that saves a controlplot for a 1-dimensional histogram."""
    fig, ax = plt.subplots(1)
    x = histogram.points()[0]
    linestyles = ['-', '--', '-.', ':']
    if len(x) == 1:
        x = [0., 1.]
        for row_index in range(array.shape[0]):
            # There are 10 different colours in the default sequence, so change line style every 10 uncertainties to keep them distinguishable
            linestyle = linestyles[(row_index % 40) // 10] # index switches 0, 1, 2, 3, 0, 1, 2, 3, 0 etc. every 10 steps
            ax.plot(x, [array[row_index][0]/nominal[0], array[row_index][0]/nominal[0]], linestyle=linestyle, alpha=0.5, label=keys[row_index])
        ax.plot(x, [reference[0]/nominal[0], reference[0]/nominal[0]], 'r-.', label='Reference')
        ax.plot(x, [nominal[0]/nominal[0], nominal[0]/nominal[0]], 'k:', label='Nominal')
        ax.fill_between(x, [var_hi[0]/nominal[0], var_hi[0]/nominal[0]], [var_lo[0]/nominal[0], var_lo[0]/nominal[0]], facecolor='0.75', edgecolor='0.75', alpha=0.3, linewidth=0, label='Combined (incl. postprocessing)')
        ax.xaxis.set_ticklabels([])
        ax.set_xlabel('Integrated', ha='right', x=1., size='x-large')
    else:
        for row_index in range(array.shape[0]):
            # There are 10 different colours in the default sequence, so change line style every 10 uncertainties to keep them distinguishable
            linestyle = linestyles[(row_index % 40) // 10] # index switches 0, 1, 2, 3, 0, 1, 2, 3, 0 etc. every 10 steps
            ax.plot(x, array[row_index]/nominal, linestyle=linestyle, alpha=0.5, label=keys[row_index])
        ax.plot(x, reference/nominal, 'r-.', label='Reference')
        ax.plot(x, nominal/nominal, 'k:', label='Nominal')
        ax.fill_between(x, var_hi/nominal, var_lo/nominal, facecolor='0.75', edgecolor='0.75', alpha=0.3, linewidth=0, label='Combined (incl. postprocessing)')
        xlabel = histogram.plot_attributes.get('xlabel', 'set histogram.plot_attributes[\'xlabel\'] = <label>!')
        ax.set_xlabel(xlabel, ha='right', x=1., size='x-large')

    fig.subplots_adjust(right=0.5)
    ax.legend(bbox_to_anchor=(1.01, 1.15), fontsize='xx-small')
    ax.set_ylabel('Ratio to nominal', ha='right', y=1., size='x-large')
    # print(self.controlplot + ' {0}'.format(array.shape[0]))
    fig.savefig(path)
    plt.close(fig)



def _make_2d_controlplot(histogram, nominal, reference, array, keys, var_hi, var_lo, path):
    """Helper function that saves a controlplot for a 2-dimensional histogram.

    Caution: since there's one panel (= subplot) per variation in this plot, it will
    become very large if there are lots of variations.
    """
    nrows = int(np.ceil(len(keys)/2))
    fig, axes = plt.subplots(nrows, 2, figsize=(10, 4*nrows), squeeze=False, constrained_layout=True)
    # fig, axes = plt.subplots(len(keys), figsize=(8, 5*len(keys)))
    for index, (key, varied_areas) in enumerate(zip(keys, array)):

        these_axes = axes[np.unravel_index(index, axes.shape)]

        #print(key, varied_areas)
        uncertainty_hist = deepcopy(histogram)
        uncertainty_hist.corr_variations = {}
        uncertainty_hist.uncorr_variations = {}
        uncertainty_hist.areas = (varied_areas - nominal) / nominal * 100.0 # for percentage!
        #print(uncertainty_hist.areas)

        midx, midy, heights = uncertainty_hist.points()

        # Visualised bin edges and midpoints
        vis_binedges = uncertainty_hist.binedges
        vis_midx = midx
        vis_midy = midy
        # We use monowidth visualisation, where the actual bin edges and midpoints are mapped to equidistant
        # visualised ones:
        # Bin edges at integers from zero:
        vis_binedges = (np.array([i for i, _ in enumerate(uncertainty_hist.binedges[0])]), np.array([i for i, _ in enumerate(uncertainty_hist.binedges[1])]))
        # Bin midpoints at integers from zero PLUS 0.5 (to make them midpoints w.r.t. the edges):
        vis_midx = _map_to_equispaced(midx)
        vis_midy = _map_to_equispaced(midy)

        # midx and midy are used here as "dummy" fill values at the bin centres.
        # The histogram is filled "with" these values with the actual bin height (or optionally area) as "weight"
        nominals = np.ravel(uncertainty_hist.areas)

        these_axes.hist2d(vis_midx, vis_midy, weights=nominals, bins=vis_binedges, cmap='bwr', norm=Normalize(vmin=-2.0, vmax=2.0))

        # Write bin contents as text onto the plot
        def text_formatter(nominal=None, **ignore):
            text = f'{nominal:+.2f}'
            if 'nan' in text.lower():
                return ''
            return text
        for x, y, uncertainty_value in zip(vis_midx, vis_midy, nominals):
            text = _make_text(text_formatter, {'nominal' : uncertainty_value})
            these_axes.text(x, y, text, verticalalignment='center', horizontalalignment='center', color='black', fontsize=8)

        # Set proper tick labels for monowidth plots:
        these_axes.set_xticks(vis_binedges[0])
        these_axes.set_yticks(vis_binedges[1])
        # Nicely format the actual binedges: drop any trailing decimal points and zeros
        # if all have integer values by converting the values to ints:
        actual_binedges_x = uncertainty_hist.binedges[0].astype(int) if np.all(np.equal(np.mod(uncertainty_hist.binedges[0], 1), 0)) else np.around(uncertainty_hist.binedges[0], 5)
        actual_binedges_y = uncertainty_hist.binedges[1].astype(int) if np.all(np.equal(np.mod(uncertainty_hist.binedges[1], 1), 0)) else np.around(uncertainty_hist.binedges[1], 5)
        these_axes.set_xticklabels(actual_binedges_x)
        these_axes.set_yticklabels(actual_binedges_y)

        # Make the plot prettier
        these_axes.set_title(key, x=0., ha='left', size='large')
        if 'xlabel' in uncertainty_hist.plot_attributes:
            these_axes.set_xlabel(uncertainty_hist.plot_attributes['xlabel'], ha='right', x=1., size='large')
        if 'ylabel' in uncertainty_hist.plot_attributes:
            these_axes.set_ylabel(uncertainty_hist.plot_attributes['ylabel'], ha='right', y=1., size='large')
        these_axes.tick_params(which='both', bottom=True, top=True, left=True, right=True, direction='in')

    fig.suptitle('Relative uncertainties (%)', ha='center', size='x-large')
    # fig.subplots_adjust(left=0.08, bottom=0.08, right=0.08, top=0.08, wspace=0.08, hspace=0.08)
    fig.savefig(path)



# Terminology used in the combination methods:
# @array: Numpy array of varied histogram areas, where the columns correspond to bins and the rows to variations
# @nominal: Numpy array of the nominal histogram areas, with respect to which the uncertainty is determined

def combine_add_quad(array, nominal):
    diffs = array - nominal
    diffs_hi = diffs.clip(min=0.)
    diffs_lo = diffs.clip(max=0.)
    hi = nominal + np.sqrt(np.sum(diffs_hi**2, axis=0))
    lo = nominal - np.sqrt(np.sum(diffs_lo**2, axis=0))
    return (hi, lo)

def combine_add_lin(array, nominal):
    diffs = array - nominal
    diffs_hi = diffs.clip(min=0.)
    diffs_lo = diffs.clip(max=0.)
    hi = nominal + np.sum(diffs_hi, axis=0)
    lo = nominal + np.sum(diffs_lo, axis=0) # note: plus sign, the sum is non-positive
    return (hi, lo)

def combine_symm_rms(array, nominal):
    n_rows = array.shape[0] # how many variations (= rows) there are in the array
    shift = np.sqrt(np.sum((array - nominal)**2, axis=0) / float(n_rows))
    hi = nominal + shift
    lo = nominal - shift
    return (hi, lo)

def combine_asym_rms(array, nominal):
    n_hi = np.sum(np.greater_equal(array, nominal).astype(float), axis=0) # array containing the counts of high shifts in each bin
    shift_hi = np.sqrt(np.sum( ( (array - nominal).clip(min=0.) )**2, axis=0 ) / n_hi)
    hi = nominal + shift_hi
    n_lo = np.sum(np.less_equal(array, nominal).astype(float), axis=0) # array containing the counts of low shifts in each bin
    shift_lo = np.sqrt(np.sum( ( (array - nominal).clip(max=0.) )**2, axis=0 ) / n_lo)
    lo = nominal - shift_lo
    return (hi, lo)

def combine_envelope(array, nominal):
    # This reshaping seems to be done implicitly for 1D arrays, but must be done
    # explicitly for 2D arrays:
    nominal = deepcopy(nominal).reshape(1, *nominal.shape)
    array_incl_nominal = np.vstack((array, nominal)) # append nominal to array
    hi = np.max(array_incl_nominal, axis=0)
    lo = np.min(array_incl_nominal, axis=0)
    return (hi, lo)

def combine_asym_hessian(array, nominal):
    raise NotImplementedError
    return (hi, lo)

def combine_symm_hessian(array, nominal):
    shift = np.sqrt(np.sum((array - nominal)**2, axis=0))
    hi = nominal + shift
    lo = nominal - shift
    return (hi, lo)

def combine_asym_hessian_pairwise(array, nominal):
    diffs = array - nominal
    diffs_odd = diffs[0::2]
    diffs_even = diffs[1::2]
    if not diffs_odd.shape == diffs_even.shape:
        raise RuntimeError()
    hi = nominal + np.sqrt(np.sum( (np.maximum(diffs_odd, diffs_even).clip(min=0.) )**2, axis=0) )
    lo = nominal - np.sqrt(np.sum( (np.maximum(-diffs_odd, -diffs_even).clip(min=0.) )**2, axis=0) )
    return (hi, lo)

def combine_symm_hessian_pairwise(array, nominal):
    raise NotImplementedError
    return (hi, lo)



def _make_variation_array(variation_dictionary, keys):
    return np.array([variation_dictionary[key] for key in keys])



class model(object):
    '''
    Model for combining multiple variations into one uncertainty.

    Contains information of which variations to combine how and
    what to call the result.
    '''
    def __init__(self, name, keys, strategy, reference=None, postprocess=None, suffixes=('__hi', '__lo'), controlplot=None, matches_required=None):
        '''
        Let 'old' be the histogram whose variations will be combined and 'new' the resulting histogram.

        @name: of the uncertainty, will become the key in new.corr_variations
        @keys: list of names of the variations, should be in old.corr_variations.keys(), OR string containing Unix-style wildcards (*, ?, [...], [!...])
               that match any non-zero number of old.corr_variations.keys()
        @strategy:  how to primarily combine the variations into one uncertainty. Valid options are:
                    "no_comb" --- no combination, just write out the same variations as were found for the input
                    "drop" --- remove the variations from the histogram
                    "add_quad" --- add the differences between the variations and the nominal in quadrature
                    "add_lin" --- add the differences between the variations and the nominal linearly
                    "symm_rms" --- take the root mean square deviation of the variations from the nominal as the symmetric uncertainty. _If_ the nominal
                                   corresponds to the sample mean of the variations, the result corresponds to the standard deviation
                                   * example use case: combining NNPDF PDF variations into uncertainty
                    "asym_rms" --- take the root mean square difference from the nominal on each side of the nominal
                                   (smaller/larger) as the uncertainty
                                   * example use case: combining a set of toy variations into an asymmetric uncertainty
                    "asym_hessian" --- asymmetric Hessian uncertainty
                                       * example use case: ???
                    "symm_hessian" --- symmetric Hessian uncertainty
                                       * example use case: combining PDF4LHC15_30 PDF variations into uncertainty
                    "asym_hessian_pairwise" --- asymmetric Hessian uncertainty for cases in which pairwise variations are given. There MUST be an even
                                                number of variations (this is checked by the code) and they must be sorted so that variations 1 and 2,
                                                variations 3 and 4, etc., form pairs (this cannot be checked by the code, so it's entirely the user's
                                                responsibility).
                                                * example use case: combining CT14 PDF variations into uncertainty
                    "symm_hessian_pairwise" --- symmetric Hessian uncertainty for cases in which pairwise variations are given. There MUST be an even
                                                number of variations (this is checked by the code) and they must be sorted so that variations 1 and 2,
                                                variations 3 and 4, etc., form pairs (this cannot be checked by the code, so it's entirely the user's
                                                responsibility).
                                                * example use case: ???
                    "envelope" --- take the envelope of all variations AND the nominal as the uncertainty
                                   * example use case: combining QCD renormalisation and factorisation scale variations into uncertainty
        @reference: Some uncertainties require a reference histogram to calculate, e.g. the PDF uncertainty band of a PDF set should be calculated around the
                    nominal histogram of that PDF set, which is not the same as the nominal histogram if the PDF set in question is not the nominal PDF set.
                    @reference can be used to choose the correct reference histogram by setting it to the (string) key of the variation histogram that should
                    be used as reference.
                    If @reference=None, the nominal histogram will be used as reference.
        @postprocess:    options are:
                         None --- no further processing after the primary @strategy has been applied
                         "max" --- symmetrise around nominal by mirroring the larger absolute difference between variation and nominal in each bin
                         <float> --- if a float is given, the deviation of the variation from the nominal in each bin is multiplied by this number
                                     * example use case: convert 90% confidence interval uncertainties given for CT14 PDF set to 68% confidence interval
                                       uncertainties by setting postprocess=1./1.645
        @suffixes:  which suffixes to append for the resulting high and low variation (in that order)
        @controlplot:   if a path is given, a plot summarising the uncertainty combination may be created and saved under this name (if the controlplots argument
                        of model.apply() is not None). A text file describing what uncertainties were found and how they were combined is also created.
                        Useful for technical debugging as well as understanding physical effects.
        @matches_required:  can be set to an integer to require exactly that number of variations being found for the model. Otherwise, a RuntimeError is raised.

        NOTE: in the future, could add smoothings etc.
        '''
        super(model, self).__init__()
        self.name = name
        self.keys = keys
        self.strategy = strategy
        self.reference_key = reference
        self.postprocess = postprocess
        self.suffixes = suffixes
        self.controlplot = controlplot
        self.matches_required = matches_required
        self.combination_functions = {
            'no_comb' : None,
            'rename' : None,
            'drop' : None,
            'add_quad' : combine_add_quad,
            'add_lin' : combine_add_lin,
            'symm_rms' : combine_symm_rms,
            'asym_rms' : combine_asym_rms,
            'asym_hessian' : combine_asym_hessian,
            'symm_hessian' : combine_symm_hessian,
            'asym_hessian_pairwise' : combine_asym_hessian_pairwise,
            'symm_hessian_pairwise' : combine_symm_hessian_pairwise,
            'envelope' : combine_envelope,
        }
        if not strategy in self.combination_functions.keys():
            raise RuntimeError('Invalid uncertainty combination strategy "{0}" in model, please pick one of "{1}"'.format(strategy, ", ".join(self.combination_functions.keys())))



    def _find_keys(self, histogram, controlplot_location=None):
        all_keys = histogram.corr_variations.keys()
        if controlplot_location and self.controlplot:
            logfile_contents = dedent('''
            All available keys in histogram:

            {all_keys}

            Model will try to select keys matching:

            {keys}
            ''')
            logpath = os.path.join(controlplot_location, os.path.splitext(self.controlplot)[0]+'.txt')
            if not os.path.exists(controlplot_location):
                os.makedirs(controlplot_location)
            with open(logpath, 'w') as logfile:
                logfile.write(logfile_contents.format(all_keys=all_keys, keys=self.keys))
                # print(logfile_contents.format(all_keys=all_keys, keys=self.keys))
        # If self.keys is a list:
        if isinstance(self.keys, list):
            missing = [key for key in self.keys if not key in all_keys]
            if missing:
                raise RuntimeError('Uncertainty combination model "{0}" cannot be applied: the following input variations are missing in the input histogram: "{1}"'.format(self.name, '", "'.join(missing)))
            return self.keys
        # Else assume self.keys is a string, possibly containing Unix-style wildcards:
        keys = fnmatch.filter(list(all_keys), self.keys)
        if self.matches_required and len(keys) != self.matches_required:
            raise RuntimeError('Uncertainty combination model "{0}" cannot be applied: require {1} keys in histogram.corr_variations matching expression "{2}", but found {3}.'.format(self.name, self.matches_required, self.keys, len(keys)))
        return sorted(keys)



    def apply(self, histogram, controlplot_location=None):
        '''
        WARNING: SIDE EFFECTS - this method will change the @histogram.corr_variations dictionary.
        @controlplots: if a directory (end with '/') or prefix is given, control plots will be stored there for models
                       that have them enabled (model.controlplot != None)
        '''
        # print(histogram.corr_variations.keys())
        if self.controlplot is None:
            controlplot_location = None
        keys = self._find_keys(histogram, controlplot_location=controlplot_location)
        if not keys:
            raise RuntimeError('Found no variations for uncertainty combination model "{0}"'.format(self.name))
        if self.strategy == 'no_comb':
            return
        if self.strategy == 'drop':
            for key in keys:
                histogram.corr_variations.pop(key)
            return
        nominal = histogram.areas # alias for readability
        reference = nominal if not self.reference_key else histogram.corr_variations[self.reference_key]
        # Make array in which rows correspond to the variations:
        array = _make_variation_array(histogram.corr_variations, keys)
        # Combine original variations into new variations:
        combination_function = self.combination_functions[self.strategy]
        var_hi, var_lo = combination_function(array, reference) # NOTE: the histogram @reference is used as the @nominal in the combination function!!!
        # Apply postprocessing if desired:
        if self.postprocess:
            if isinstance(self.postprocess, float):
                var_hi *= reference + self.postprocess * (var_hi - reference)
                var_lo *= reference + self.postprocess * (var_lo - reference)
            elif self.postprocess == 'max':
                # Note: 'max' postprocessing is with respect to nominal, not reference
                shift = np.maximum(np.abs(var_hi - nominal), np.abs(var_lo - nominal))
                var_hi = nominal + shift
                var_lo = nominal - shift
        # Add new variations to the histogram:
        histogram.corr_variations[self.name + self.suffixes[0]] = var_hi
        histogram.corr_variations[self.name + self.suffixes[1]] = var_lo
        # Make controlplot if requested
        if controlplot_location:
            controlplot_args = [histogram, nominal, reference, array, keys, var_hi, var_lo, os.path.join(controlplot_location, self.controlplot)]
            if isinstance(histogram, _histogram1d):
                _make_1d_controlplot(*controlplot_args)
            elif isinstance(histogram, _histogram2d):
                _make_2d_controlplot(*controlplot_args)
        # Drop the original variations from the input histogram:
        for key in keys:
            histogram.corr_variations.pop(key)



def _keep_largest_shift(shift_array):
    '''
    Keep the largest shift in
    '''
    pass



def _delete_substrings(string, substrings):
    '''
    TODO: convert to a function called "_delete_suffixes" that only deletes
          substrings _at the end_.
    '''
    for ss in substrings:
        string = string.replace(ss, '')
    return string



# def _matches_any(string, body, suffixes):
#     '''
#     Return true if `string` is equal to `body` plus any of the `suffixes`.
#     If no `suffixes` are given, return False.
#     '''
#     if not suffixes:
#         return False
#     for suffix in suffixes:
#         if string == body + suffix:
#             return True
#     return False



def _iterator_over_variation_keys_grouped_by_label(keys, suffixes):
    '''
    Generator yielding the label (= variation key without suffix such as'_1up', '_1down', e.g. 'jes_1up' -> 'jes')
    and a list of the variation keys matching that label.
    '''
    keys = sorted(keys)
    for label, matching_keys in groupby(keys, lambda x : _delete_substrings(x, suffixes) ):
        yield label, list(matching_keys)



def _remove_nonmaximal_shifts(var, envelope, nominal):
    '''
    Return a modified version of `var` in which the deviations from the `nominal` have been set to
    zero if they are smaller than the corresponding values in `envelope` (which is a tuple of high, low!).

    CAUTION: HAS A BUG --- if two variations have the an identical shift (sign and magnitude), both are kept!!!
    '''
    raise NotImplementedError
    zero = np.zeros_like(var)
    shifts = var - nominal
    neg_shifts = np.where(shifts < 0, shifts, zero)
    pos_shifts = np.where(shifts > 0, shifts, zero)
    neg_envelope_shifts = np.where((envelope[1] - nominal) < 0, envelope[1] - nominal, zero)
    pos_envelope_shifts = np.where((envelope[0] - nominal) > 0, envelope[0] - nominal, zero)
    # Now calculate the shifts to be used in the result:
    # TODO: float comparison not numerically safe!!! Replace with something with safer!!!
    cleaned_neg = np.where(neg_shifts == neg_envelope_shifts, neg_shifts, zero)
    cleaned_pos = np.where(pos_shifts == pos_envelope_shifts, neg_shifts, zero)
    return nominal + cleaned_neg + cleaned_pos



def remove_same_sign_shifts(histogram, suffixes=['_1up', '_1down', '_up', '_down']):
    '''
    Drop smaller same-sign correlated variation shifts from the nominal for any group of variations
    whose names differ only by (any number of occurrences of) any of the strings in :code:`matches`
    '''
    raise NotImplementedError
    out = deepcopy(histogram)
    corr_variation_names = list(out.corr_variations.keys())
    envelope_by_label = {} # values will be tuples of (high, low)
    for label, matching_keys in _iterator_over_variation_keys_grouped_by_label(corr_variation_names, suffixes):
        envelope_by_label[label] = combine_envelope(_make_variation_array(out.corr_variations, matching_keys), out.areas)

    for key, var in out.corr_variations.items():
        label = _delete_substrings(key, suffixes)
        out.corr_variations[key] = _remove_nonmaximal_shifts(var, envelope_by_label[label], out.areas)

    return out



def combine_copy(histogram, models, ignore_missing=False, controlplot_location=None, drop_same_sign_shifts=False, suffixes=['_1up', '_1down', '_up', '_down']):
    '''
    @histogram: the input histogram. The return value will be a copy of this histogram, with the desired variation combinations applied.
    @models: iterable of the models to be applied
    @ignore_missing: if True, do not throw an exception if the input variations specified in a model are missing, but simply ignore the model
    @controlplot_location: if a directory (end with '/') or prefix is given, control plots will be stored there for models
                           that have them enabled (model.controlplot != None)
    :param drop_same_sign_shifts: if True, _correlated_ variation names that differ only by any suffix given in argument :code:`suffixes` are grouped together. If more than one of these grouped variations has a shift with respect to the nominal in a given bin, only the largest shift in that bin is kept. The other shifts are set to zero (i.e. the variation is set to equal the nominal in the bin). A common case where this is useful is to avoid double-counting the same source of systematic uncertainty in bins where the "up" and "down" variation point in the same direction with respect to the nominal in some bin(s). Uncorrelated variations are not affected by this option.
    :type drop_same_sign_shifts: :code:`bool`
    :param suffixes: see argument :code:`drop_same_sign_shifts` for explanation
    :type suffixes: :code:`list` of :code:`str`

    IMPORTANT NOTE: it is possible to apply combination models whose input variations are only produced in the same call of combine_copy. In other words,
                    the variations don't yet need to exist in the @histogram.corr_variations when passing @histogram to combine_copy.
    '''
    if drop_same_sign_shifts:
        out = remove_same_sign_shifts(histogram, suffixes=suffixes)
    else:
        out = deepcopy(histogram)
    # print(list(out.corr_variations.keys()))

    for model in models:
        try:
            model.apply(out, controlplot_location=controlplot_location)
            # print(model.name)
            # print(list(out.corr_variations.keys()))
        except RuntimeError:
            if not ignore_missing:
                raise
    return out
