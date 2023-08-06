import pytest
import pdb
import re

# Auxiliary modules
import numpy as np
from copy import deepcopy
import sys

# Module to be tested
sys.path.append('..')
import heppy

# Setup: create a histogram
areas = np.array([4.3, 9.7, 12.1])
binedges = np.array([-7., 0., 5., 50.])
uncorr_variations = {
    'stat_up' : areas + np.sqrt(areas), # approx [6.37, 12.81, 15.58]
    'stat_down' : areas - np.sqrt(areas) # approx [2.23, 6.59, 8.62]
}
corr_variations = {
    'foo_up' : areas + np.ones_like(areas),
    'foo_down' : areas - np.ones_like(areas),
    'single' : areas + np.array([-4., 8.5, 3.0])
}
_h = heppy.histogram(binedges, areas, areas=True, uncorr_variations=uncorr_variations, corr_variations=corr_variations)
_h.name = 'fooble'



# Tests
# TODO: check that illegal options in rebinning methods trigger exception!

def test_heights():
    np.testing.assert_array_almost_equal(_h.heights, np.array([0.6142857142857142, 1.94, 0.2688888888888889]))

def test_find_bin():
    # Check cases where x lies within the histogram x-boundaries:
    assert _h.bin_index(-7.0) == 0
    assert _h.bin_index(-5.0) == 0
    assert _h.bin_index(0.) == 1
    assert _h.bin_index(0.5) == 1
    assert _h.bin_index(5.3) == 2
    # Check cases where x lies outside of the histogram x-boundaries:
    with pytest.raises(ValueError) as exc_info:
        assert _h.bin_index(-7.1)
    assert exc_info.value.args[0] == 'Cannot find index of bin containing x = -7.1, which is outside of histogram x-boundaries [-7.0, 50.0)'
    with pytest.raises(ValueError) as exc_info:
        assert _h.bin_index(60.)
    assert exc_info.value.args[0] == 'Cannot find index of bin containing x = 60.0, which is outside of histogram x-boundaries [-7.0, 50.0)'
    with pytest.raises(ValueError) as exc_info:
        assert _h.bin_index(50.) # IMPORTANT: upper bin edge is NOT part of bin!
    assert exc_info.value.args[0] == 'Cannot find index of bin containing x = 50.0, which is outside of histogram x-boundaries [-7.0, 50.0)'

def test_integral():
    np.testing.assert_approx_equal(_h.integral(), 26.1)

def test_rebin():
    h = deepcopy(_h)
    h.rebin([-7., 5., 50.])
    np.testing.assert_array_almost_equal(h.binedges, np.array([-7, 5., 50.]))
    np.testing.assert_array_almost_equal(h.areas, np.array([14., 12.1]))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_up'], h.areas + np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_down'], h.areas - np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(h.corr_variations['foo_up'], np.array([16., 13.1]))
    np.testing.assert_array_almost_equal(h.corr_variations['foo_down'], np.array([12., 11.1]))
    np.testing.assert_array_almost_equal(h.corr_variations['single'], np.array([18.5, 15.1]))
    np.testing.assert_approx_equal(h.integral(), 26.1)

def test_lossy_rebin():
    """
    Rebinning less than the complete bin range of the histogram.
    Information falling outside of the new outer bin edges is dropped.
    """
    # Cutting off from the low end
    h = deepcopy(_h)
    h.rebin([5., 50.])
    np.testing.assert_array_almost_equal(h.binedges, np.array([5., 50.]))
    np.testing.assert_array_almost_equal(h.areas, np.array([12.1]))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_up'], h.areas + np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_down'], h.areas - np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(h.corr_variations['foo_up'], np.array([13.1]))
    np.testing.assert_array_almost_equal(h.corr_variations['foo_down'], np.array([11.1]))
    np.testing.assert_array_almost_equal(h.corr_variations['single'], np.array([15.1]))
    np.testing.assert_approx_equal(h.integral(), 12.1)
    # Cutting off from the high end
    h = deepcopy(_h)
    h.rebin([-7., 5.])
    np.testing.assert_array_almost_equal(h.binedges, np.array([-7., 5.]))
    np.testing.assert_array_almost_equal(h.areas, np.array([14.]))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_up'], h.areas + np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_down'], h.areas - np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(h.corr_variations['foo_up'], np.array([16.]))
    np.testing.assert_array_almost_equal(h.corr_variations['foo_down'], np.array([12.]))
    np.testing.assert_array_almost_equal(h.corr_variations['single'], np.array([18.5]))
    np.testing.assert_approx_equal(h.integral(), 14.)


def test_merge_bins():
    h = deepcopy(_h)
    h.merge_bins(0., 50.)
    np.testing.assert_array_almost_equal(h.binedges, np.array([-7, 0., 50.]))
    np.testing.assert_array_almost_equal(h.areas, np.array([4.3, 21.8]))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_up'], h.areas + np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_down'], h.areas - np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(h.corr_variations['foo_up'], np.array([5.3, 23.8]))
    np.testing.assert_array_almost_equal(h.corr_variations['foo_down'], np.array([3.3, 19.8]))
    np.testing.assert_array_almost_equal(h.corr_variations['single'], np.array([0.3, 33.3]))
    np.testing.assert_approx_equal(h.integral(), 26.1)

def test_squash_highest_bin():
    h = deepcopy(_h)
    h.squash_highest_bin(0., 25.)
    np.testing.assert_array_almost_equal(h.binedges, np.array([-7, 0., 25.]))
    np.testing.assert_array_almost_equal(h.areas, np.array([4.3, 21.8]))
    np.testing.assert_array_almost_equal(h.heights, np.array([0.6142857142857142, 0.872]))
    np.testing.assert_approx_equal(h.integral(), 26.1)

def test_net_variations_uncorr_only():
    h = deepcopy(_h)
    h.corr_variations = {}
    upper, lower = h.net_variations()
    np.testing.assert_array_almost_equal(lower, h.areas - np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(upper, h.areas + np.sqrt(h.areas))
    upper_shift, lower_shift = h.net_variations(subtract_nominal=True)
    np.testing.assert_array_almost_equal(lower_shift, -np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(upper_shift, np.sqrt(h.areas))
    upper_rel, lower_rel = h.net_variations(relative=True)
    np.testing.assert_array_almost_equal(lower_rel, (h.areas - np.sqrt(h.areas)) / h.areas)
    np.testing.assert_array_almost_equal(upper_rel, (h.areas + np.sqrt(h.areas)) / h.areas)
    upper_rel_shift, lower_rel_shift = h.net_variations(subtract_nominal=True, relative=True)
    np.testing.assert_array_almost_equal(lower_rel_shift, -1./np.sqrt(h.areas))
    np.testing.assert_array_almost_equal(upper_rel_shift, 1./np.sqrt(h.areas))

def test_net_variations_corr_only():
    h = deepcopy(_h)
    h.uncorr_variations = {}
    # TODO!
    # (lower, upper) = h.net_variations()
    # np.testing.assert_array_almost_equal(lower, h.areas - np.sqrt(h.areas))
    # np.testing.assert_array_almost_equal(upper, h.areas + np.sqrt(h.areas))
    # (lower_shift, upper_shift) = h.net_variations(subtract_nominal=True)
    # np.testing.assert_array_almost_equal(lower_shift, -np.sqrt(h.areas))
    # np.testing.assert_array_almost_equal(upper_shift, np.sqrt(h.areas))
    # (lower_rel, upper_rel) = h.net_variations(relative=True)
    # np.testing.assert_array_almost_equal(lower_rel, (h.areas - np.sqrt(h.areas)) / h.areas)
    # np.testing.assert_array_almost_equal(upper_rel, (h.areas + np.sqrt(h.areas)) / h.areas)
    # (lower_rel_shift, upper_rel_shift) = h.net_variations(subtract_nominal=True, relative=True)
    # np.testing.assert_array_almost_equal(lower_rel_shift, -1./np.sqrt(h.areas))
    # np.testing.assert_array_almost_equal(upper_rel_shift, 1./np.sqrt(h.areas))

def test_net_variations_selective():
    h = deepcopy(_h)
    h.corr_variations = {}
    upper, lower = h.net_variations()
    _upper, _lower = _h.net_variations(['stat_up', 'stat_down'])
    np.testing.assert_array_almost_equal(lower, _lower)
    np.testing.assert_array_almost_equal(upper, _upper)

def test_net_variations():
    pass
    # TODO!
    # (lower, upper) = h.net_variations()
    # np.testing.assert_array_almost_equal(lower, h.areas - np.sqrt(h.areas))
    # np.testing.assert_array_almost_equal(upper, h.areas + np.sqrt(h.areas))
    # (lower_shift, upper_shift) = h.net_variations(subtract_nominal=True)
    # np.testing.assert_array_almost_equal(lower_shift, -np.sqrt(h.areas))
    # np.testing.assert_array_almost_equal(upper_shift, np.sqrt(h.areas))
    # (lower_rel, upper_rel) = h.net_variations(relative=True)
    # np.testing.assert_array_almost_equal(lower_rel, (h.areas - np.sqrt(h.areas)) / h.areas)
    # np.testing.assert_array_almost_equal(upper_rel, (h.areas + np.sqrt(h.areas)) / h.areas)
    # (lower_rel_shift, upper_rel_shift) = h.net_variations(subtract_nominal=True, relative=True)
    # np.testing.assert_array_almost_equal(lower_rel_shift, -1./np.sqrt(h.areas))
    # np.testing.assert_array_almost_equal(upper_rel_shift, 1./np.sqrt(h.areas))

def test_errorbars_uncorr_only():
    # TODO: change to contain ALL variations, also correlated ones
    h = deepcopy(_h)
    h.corr_variations = {}
    upper, lower = h.errorbars()
    np.testing.assert_array_almost_equal(lower, np.sqrt(h.areas)/h.binwidths)
    np.testing.assert_array_almost_equal(upper, np.sqrt(h.areas)/h.binwidths)

def test_add():
    h = _h + _h
    np.testing.assert_array_almost_equal(h.binedges, np.array([-7, 0., 5., 50.]))
    np.testing.assert_array_almost_equal(h.areas, 2*areas)
    np.testing.assert_array_almost_equal(h.heights, 2.* np.array([0.6142857142857142, 1.94, 0.2688888888888889]))
    h.corr_variations = {} # TODO: delete me!
    upper_errorbar, lower_errorbar = h.errorbars()
    np.testing.assert_array_almost_equal(lower_errorbar, np.sqrt(h.areas)/h.binwidths)
    np.testing.assert_array_almost_equal(upper_errorbar, np.sqrt(h.areas)/h.binwidths)

def test_add_with_zero_bin_area():
    g = deepcopy(_h)
    g.areas = np.array([2., 1., 0.])
    g.uncorr_variations = {
        'stat_up' : np.array([2., 1., 0.]) + np.sqrt(np.array([2., 1., 0.])),
        'stat_down' : np.array([2., 1., 0.]) - np.sqrt(np.array([2., 1., 0.])),
    }
    h = g + _h
    h.corr_variations = {} # TODO: delete me!
    upper_errorbar, lower_errorbar = h.errorbars()
    np.testing.assert_array_almost_equal(lower_errorbar, np.sqrt(h.areas)/h.binwidths)
    np.testing.assert_array_almost_equal(upper_errorbar, np.sqrt(h.areas)/h.binwidths)

def test_multiply():
    h = _h * 3.5
    h.corr_variations = {} # TODO: delete me!
    np.testing.assert_array_almost_equal(h.binedges, np.array([-7, 0., 5., 50.]))
    np.testing.assert_array_almost_equal(h.areas, 3.5*areas)
    np.testing.assert_array_almost_equal(h.heights, 3.5* np.array([0.6142857142857142, 1.94, 0.2688888888888889]))
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_up'], 3.5*_h.uncorr_variations['stat_up'])
    np.testing.assert_array_almost_equal(h.uncorr_variations['stat_down'], 3.5*_h.uncorr_variations['stat_down'])
    upper, lower = h.net_variations('stat_up')
    _upper, _lower = _h.net_variations('stat_up')
    np.testing.assert_array_almost_equal(lower, 3.5*_lower)
    np.testing.assert_array_almost_equal(upper, 3.5*_upper)
    upper_errorbar, lower_errorbar = h.errorbars()
    _upper_errorbar, _lower_errorbar = _h.errorbars(['stat_up', 'stat_down'])
    np.testing.assert_array_almost_equal(lower_errorbar, 3.5*_lower_errorbar)
    np.testing.assert_array_almost_equal(upper_errorbar, 3.5*_upper_errorbar)

def test_divide_scalar():
    h = deepcopy(_h)
    h.corr_variations = {} # TODO: delete me!
    r = h / 3.0
    np.testing.assert_array_almost_equal(r.binedges, np.array([-7, 0., 5., 50.]))
    np.testing.assert_array_almost_equal(r.areas, areas/3.0)

def test_histdiv_scalar():
    '''
    This is not typically an interesting use case, but the unit test may be useful for pinpointing issues
    '''
    h = deepcopy(_h)
    h.corr_variations = {} # TODO: delete me!
    r = heppy.histdiv(h, 3.0)
    np.testing.assert_array_almost_equal(r.binedges, np.array([-7, 0., 5., 50.]))
    np.testing.assert_array_almost_equal(r.heights, areas/3.0) # NOTE: heights, not areas, due to non-division by binwidths

def test_divide():
    h = deepcopy(_h)
    h.corr_variations = {} # TODO: delete me!
    g = deepcopy(_h)
    g.corr_variations = {} # TODO: delete me!
    g.areas = np.array([2., 1., 0.])
    g.uncorr_variations = {
        'stat_up' : np.array([2., 1., 0.]) + np.sqrt(np.array([2., 1., 0.])),
        'stat_down' : np.array([2., 1., 0.]) - np.sqrt(np.array([2., 1., 0.])),
    }
    r = g / h
    np.testing.assert_array_almost_equal(r.binedges, np.array([-7, 0., 5., 50.]))
    np.testing.assert_array_almost_equal(r.areas, np.array([0.46511628, 0.10309278, 0.]))
    # np.testing.assert_array_almost_equal(h.heights, 3.5* np.array([0.6142857142857142, 1.94, 0.2688888888888889]))
    # np.testing.assert_array_almost_equal(h.uncorr_variations['stat_up'], 3.5*_h.uncorr_variations['stat_up'])
    # np.testing.assert_array_almost_equal(h.uncorr_variations['stat_down'], 3.5*_h.uncorr_variations['stat_down'])
    # upper, lower = h.net_variations('stat_up')
    # _upper, _lower = _h.net_variations('stat_up')
    # np.testing.assert_array_almost_equal(lower, 3.5*_lower)
    # np.testing.assert_array_almost_equal(upper, 3.5*_upper)
    # upper_errorbar, lower_errorbar = h.errorbars()
    # _upper_errorbar, _lower_errorbar = _h.errorbars(['stat_up', 'stat_down'])
    # np.testing.assert_array_almost_equal(lower_errorbar, 3.5*_lower_errorbar)
    # np.testing.assert_array_almost_equal(upper_errorbar, 3.5*_upper_errorbar)

def test_cumulative():
    h = deepcopy(_h)
    # Intergrating/summing from the left:
    lcum = h.cumulative()
    np.testing.assert_array_almost_equal(lcum.binedges, h.binedges)
    np.testing.assert_array_almost_equal(lcum.heights, np.array([4.3, 4.3+9.7, 4.3+9.7+12.1]))
    # Intergrating/summing from the right:
    rcum = h.cumulative(side='right')
    np.testing.assert_array_almost_equal(rcum.binedges, h.binedges)
    np.testing.assert_array_almost_equal(rcum.heights, np.array([4.3+9.7+12.1, 9.7+12.1, 12.1]))

def test_histdiv():
    '''
    This is not typically an interesting use case, but the unit test may be useful for pinpointing issues
    '''
    h = deepcopy(_h)
    h.corr_variations = {} # TODO: delete me!
    g = deepcopy(_h)
    g.corr_variations = {} # TODO: delete me!
    g.areas = np.array([2., 1., 0.])
    g.uncorr_variations = {
        'stat_up' : np.array([2., 1., 0.]) + np.sqrt(np.array([2., 1., 0.])),
        'stat_down' : np.array([2., 1., 0.]) - np.sqrt(np.array([2., 1., 0.])),
    }
    r = heppy.histdiv(g, h)
    np.testing.assert_array_almost_equal(r.binedges, np.array([-7, 0., 5., 50.]))
    np.testing.assert_array_almost_equal(r.heights, np.array([0.46511628, 0.10309278, 0.])) # NOTE: heights, not areas, due to non-division by binwidths

def test_to_root():
    """Tests converting the histogram to a dictionary of ROOT.TH1D's mapped by variation key."""
    th1s = _h.to_root()
    assert isinstance(th1s, dict)
    assert len(th1s) == 6
    assert sorted(list(th1s.keys())) == ['fooble_foo_down', 'fooble_foo_up', 'fooble_nominal', 'fooble_single', 'fooble_stat_down', 'fooble_stat_up']
    np.testing.assert_approx_equal(th1s['fooble_nominal'].GetBinContent(2), 9.7)
    np.testing.assert_approx_equal(th1s['fooble_foo_down'].GetBinContent(3), 11.1)

def test_to_root_file():
    """Tests writing the histograms to a bunch of ROOT.TH1D's inside a ROOT file."""
    _h.to_root_file('output.root', recreate=True)
    _g = deepcopy(_h)
    _g.name = 'barbaz'
    # Add to same file
    _g.to_root_file('output.root', nominal_label='default', key_form='{name}__{variation}')
    # TODO add some tests
