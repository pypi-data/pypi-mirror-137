#!/usr/bin/env python3

import numpy as np
import root_numpy as rnp
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import heppy as hp
import fnmatch



def get_TH(rootfile, histopath):
    '''
    @rootfile may be a ROOT.TFile opened in read mode or the path to an existing ROOT file
    @histopath is the path of the histogram inside the file
    '''
    if isinstance(rootfile, str):
        filepath = rootfile
        rootfile = ROOT.TFile(rootfile, 'r') # open ROOT file
        if not rootfile.IsOpen():
            raise OSError('Cannot open ROOT file "{filepath}"'.format(filepath=filepath))
    histogram_owned_by_file = rootfile.Get(histopath)
    ROOT.gROOT.cd()
    try:
        return histogram_owned_by_file.Clone()
    except ReferenceError:
        raise ReferenceError('Cannot read histogram "{histopath}" in file {filepath}'.format(histopath=histopath, filepath=rootfile.GetName()))



def readroot_binareas(rootfile, histopath, rebin=False):
    '''
    Read bin areas only and return them as a numpy array
    '''
    th = get_TH(rootfile, histopath)
    if rebin:
        th = th.Rebin(rebin)
    return rnp.hist2array(th)



def readroot_binedges1d(th1):
    '''
    Read the binedges of a TH1 histogram and return them as a one-dimensional Numpy array
    '''
    return np.array([th1.GetBinLowEdge(i) for i in range(1, th1.GetNbinsX() + 2)])



def readroot_binedges2d(th2):
    '''
    Read the binedges of a TH2 histogram and return them as a 2-tuple of one-dimensional Numpy arrays,
    where the first element represents the binedges along the x-axis and the second the binedges along
    the y-axis
    '''
    x_axis = th2.GetXaxis()
    x_edges = np.array([x_axis.GetBinLowEdge(i) for i in range(1, x_axis.GetNbins() + 2)])
    y_axis = th2.GetYaxis()
    y_edges = np.array([y_axis.GetBinLowEdge(i) for i in range(1, y_axis.GetNbins() + 2)])
    return x_edges, y_edges



def read_unix_wildcard_corr_variations(filepath, variation_paths, rebin=False):
    '''
    WARNING: slow in general.
    '''
    import uproot
    corr_variations = {}
    urfile = uproot.open(filepath)
    all_paths_in_rootfile = [key.decode().split(';')[0] for key in urfile.allkeys()]
    for name_pattern, path_pattern in variation_paths.items():
        matched_paths = fnmatch.filter(all_paths_in_rootfile, path_pattern)
        # print(name_pattern, path_pattern, '{0} matches found!'.format(len(matched_paths)))
        for matched_path in matched_paths:
            # Now to find the matched name. This will be the ROOT directory or object name that matches the name pattern
            matched_name_hits = fnmatch.filter(matched_path.split('/'), name_pattern)
            if not matched_name_hits:
                raise RuntimeError('Could not infer variation name corresponding to variation histogram "{path}": the variation name pattern "{name_pattern}" does not match any of the directory/object names in that path.'.format(path=matched_path, name_pattern=name_pattern))
            if len(matched_name_hits) > 1:
                raise RuntimeError('Encountered ambiguity when infering variation name corresponding to variation histogram "{path}": the variation name pattern "{name_pattern}" matches multiple directory/object names in that path.'.format(path=matched_path, name_pattern=name_pattern))
            matched_name = matched_name_hits[0]
            # print(matched_name + ':\t' + matched_path)
            corr_variations[matched_name] = readroot_binareas(filepath, matched_path, rebin=rebin)
    return corr_variations



def read_corr_variations(filepath, variation_paths, rebin=False, ignore_missing_variations=False):
    '''
    Return dictionary of variations located in @rootfile at @variation_paths (that is, paths inside the ROOT file),
    possibly rebinned by @rebin

    Custom wildcards:
        '@' gets replaced by 0, 1, ..., until no more histograms found
        '#' gets replaced by 1, 2, ..., until no more histograms found

    The variation_paths may also contain Unix-style wildcards (see Python module fnmatch!), in which case all encountered
    paths matching the pattern(s) are included in the returned dictionary.
    CAUTION: no error is raised if no paths match a given wildcard.

    CAUTION: mixing different types of wildcard ('@', '#', Unix-style) gives [deterministic but] undefined behaviour!
             Please don't do this.
    '''
    # Split paths into ones containing different types of wildcards and direct paths:
    unix_wildcard_paths = {}
    indexed_from_zero_paths = {}
    indexed_from_one_paths = {}
    direct_paths = {}
    for name, path in variation_paths.items():
        if any(wildcard_indicator in path for wildcard_indicator in ['*', '?', '[']):
            unix_wildcard_paths[name] = path
        elif '@' in path:
            indexed_from_zero_paths[name] = path
        elif '#' in path:
            indexed_from_one_paths[name] = path
        else:
            direct_paths[name] = path
    # First read paths not containing wildcards:
    corr_variations = {}
    for name, path in direct_paths.items():
        try:
            corr_variations[name] = readroot_binareas(filepath, path, rebin=rebin)
        except ReferenceError:
            if not ignore_missing_variations:
                raise
    # corr_variations = {name : readroot_binareas(filepath, path, rebin=rebin) for name, path in direct_paths.items()}

    for starting_index, paths_dictionary in zip([0, 1], [indexed_from_zero_paths, indexed_from_one_paths]):
        for name_pattern, path_pattern in paths_dictionary.items():
            i = starting_index
            while True:
                try:
                    name = name_pattern.replace('@', str(i))
                    path = path_pattern.replace('@', str(i))
                    corr_variations[name] = readroot_binareas(filepath, path, rebin=rebin)
                except:
                    break
                i += 1

    if (unix_wildcard_paths):
        # This is only executed if we have any Unix wildcard paths, because using uproot/matching wildcards may be very slow!
        return {**corr_variations, **read_unix_wildcard_corr_variations(filepath, unix_wildcard_paths, rebin=rebin)}
    return corr_variations



def _readroot2d(th, rootfile, histopath, rebin=False, variation_paths={}, ignore_missing_variations=False, **kwargs):
    '''
    @rootfile may be a ROOT.TFile opened in read mode or the path to an existing ROOT file
    @histopath is the path of the histogram inside the file
    @rebin, if given, is passed to ROOT.TH2.Rebin()
    @variation_paths is a dictionary of variation names (keys) and paths to the variation histograms inside @rootfile (values).
                     The @variation paths may contain the following wildcards:
                         - "@" will be interpreted as a numerical index starting at 0 and continuing until no more histograms are found
                         - "#" is the same as "@", but starting at 1
                         - Arbitrary Unix-style wildcards (see Python module fnmatch). These may not be combined with the above
                           custom wildcards. NOTE: including Unix-style wildcards may be very SLOW and introduces a dependency on
                           uproot. If either of these poses a problem, contact the Heppy maintainers, there's a lot of room for
                           speed optimisation here, and the uproot dependency can in principle be circumvented.
                     CAUTION: no error is raised if no paths match a given wildcard (@, @1, ), BUT if a path not containing wildcards
                              is matched, this DOES raise an error.
    @**kwargs get passed on to histogram constructor. An important one is @areas=False (set to True in _readroot2d by default!) if retrieving ratios
              (e.g. efficiencies), and it may be convenient to pass @name=<something> (default: <ROOT histogram>.GetName())
    '''
    if rebin:
        th = th.Rebin(rebin)
    binedges = readroot_binedges2d(th)
    areas_nominal = rnp.hist2array(th)
    areas_up = np.copy(areas_nominal)
    areas_down = np.copy(areas_nominal)
    for i in range(areas_nominal.shape[0]):
        for j in range(areas_nominal.shape[1]):
            stat_uncert = th.GetBinError(i + 1, j + 1)
            areas_up[i,j] += stat_uncert
            areas_down[i,j] -= stat_uncert
    filepath = rootfile.GetName() if isinstance(rootfile, ROOT.TFile) else rootfile
    attributes = {
        'name' : th.GetName(),
        'title' : th.GetTitle(),
        'provenance' : '{filepath}:{histopath}'.format(filepath=filepath, histopath=histopath),
    }
    corr_variations = read_corr_variations(filepath, variation_paths, rebin=rebin, ignore_missing_variations=ignore_missing_variations)
    if not 'areas' in kwargs:
        kwargs['areas'] = True
    if not 'name' in kwargs:
        kwargs['name'] = th.GetName()
    return hp.histogram2d(binedges, areas_nominal, uncorr_variations={'Statistical__1up' : areas_up, 'Statistical__1down' : areas_down}, corr_variations=corr_variations, attributes=attributes, plot_attributes={'label' : kwargs['name']}, **kwargs)



def _readroot1d(th, rootfile, histopath, rebin=False, variation_paths={}, ignore_missing_variations=False, **kwargs):
    '''
    @rootfile may be a ROOT.TFile opened in read mode or the path to an existing ROOT file
    @histopath is the path of the histogram inside the file
    @rebin, if given, is passed to ROOT.TH1.Rebin()
    @variation_paths is a dictionary of variation names (keys) and paths to the variation histograms inside @rootfile (values).
                     The @variation paths may contain the following wildcards:
                         - "@" will be interpreted as a numerical index starting at 0 and continuing until no more histograms are found
                         - "#" is the same as "@", but starting at 1
                         - Arbitrary Unix-style wildcards (see Python module fnmatch). These may not be combined with the above
                           custom wildcards. NOTE: including Unix-style wildcards may be very SLOW and introduces a dependency on
                           uproot. If either of these poses a problem, contact the Heppy maintainers, there's a lot of room for
                           speed optimisation here, and the uproot dependency can in principle be circumvented.
                     CAUTION: no error is raised if no paths match a given wildcard (@, @1, ), BUT if a path not containing wildcards
                              is matched, this DOES raise an error.
    @**kwargs get passed on to histogram constructor. An important one is @areas=False (set to True in _readroot1d by default!) if retrieving ratios
              (e.g. efficiencies), and it may be convenient to pass @name=<something> (default: <ROOT histogram>.GetName())
    '''
    if rebin:
        th = th.Rebin(rebin)
    binedges = readroot_binedges1d(th)
    areas_nominal = rnp.hist2array(th)
    areas_up = np.copy(areas_nominal)
    areas_down = np.copy(areas_nominal)
    for i in range(len(areas_nominal)):
        stat_uncert = th.GetBinError(i + 1)
        areas_up[i] += stat_uncert
        areas_down[i] -= stat_uncert
    filepath = rootfile.GetName() if isinstance(rootfile, ROOT.TFile) else rootfile
    attributes = {
        'name' : th.GetName(),
        'title' : th.GetTitle(),
        'provenance' : '{filepath}:{histopath}'.format(filepath=filepath, histopath=histopath),
    }
    corr_variations = read_corr_variations(filepath, variation_paths, rebin=rebin, ignore_missing_variations=ignore_missing_variations)
    if not 'areas' in kwargs:
        kwargs['areas'] = True
    if not 'name' in kwargs:
        kwargs['name'] = th.GetName()
    return hp.histogram1d(binedges, areas_nominal, uncorr_variations={'Statistical__1up' : areas_up, 'Statistical__1down' : areas_down}, corr_variations=corr_variations, attributes=attributes, plot_attributes={'label' : kwargs['name']}, **kwargs)



def readroot(rootfile, histopath, rebin=False, variation_paths={}, ignore_missing_variations=False, **kwargs):
    th = get_TH(rootfile, histopath)
    # CAUTION: the order of the if statements matters here, because in ROOT, TH2 inherits from TH1!!!
    if isinstance(th, ROOT.TH2):
        return _readroot2d(th, rootfile, histopath, rebin=rebin, variation_paths=variation_paths, ignore_missing_variations=ignore_missing_variations, **kwargs)
    if isinstance(th, ROOT.TH1):
        return _readroot1d(th, rootfile, histopath, rebin=rebin, variation_paths=variation_paths, ignore_missing_variations=ignore_missing_variations, **kwargs)
    raise TypeError('Can only read ROOT.TH1 and ROOT.TH2 objects, but found {type} object in "{rootfile}" at "{histopath}"'.format(type=type(th), rootfile=rootfile, histopath=histopath))
