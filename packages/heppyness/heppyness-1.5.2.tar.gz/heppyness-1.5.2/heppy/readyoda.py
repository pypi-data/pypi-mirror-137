import numpy as np
import yoda

# Read the names of all the yoda histograms in the file
def get_histogram_names(yodafile):
    aos = yoda.read(yodafile, asdict=False)
    return [ao.name for ao in aos if ao.type == 'Histo1D']

# Read the paths of all the yoda histograms in the file
def get_histogram_paths(yodafile):
    aos = yoda.read(yodafile, asdict=False)
    return [ao.path for ao in aos if ao.type == 'Histo1D']

# Needs a reference yoda file containing the nominal event counter to whose sum of weights we want to normalise
# This is needed to undo the Athena Sherpa interface's patch/hack where it rescales the variation weights such
# that correct normalisation is obtained by taking (variation_weight_i) / (sum_of_NOMINAL_weights).
# Usually: refyodafile = path to file containing the nominal histograms!
def get_bin_heights(histogram_path, yodafile, refyodafile, debug=False):
    aos = yoda.read(yodafile, asdict=True)
    refaos = yoda.read(refyodafile, asdict=True)
    sow = aos['/_EVTCOUNT'].sumW()
    refsow = refaos['/_EVTCOUNT'].sumW() # in ATLAS usage, this must be the *nominal* sum of weights for the sample
    weight_correction = sow / refsow
    if debug:
        print('Correcting variation weights by {0} (variation SoW: {1}, reference SoW: {2})'.format(weight_correction, sow, refsow))
    return [b.height * weight_correction for b in aos[histogram_path].bins]

def get_curve(histogram_path, yodafile, refyodafile):
    heights = np.array(get_bin_heights(histogram_path, yodafile, refyodafile))
    return np.repeat(heights, 2)

def get_curves(histogram_path, yodafiles, refyodafile):
    return [get_curve(histogram_path, yodafile, refyodafile) for yodafile in yodafiles]

def get_relative_error(histogram_path, yodafile):
    aos = yoda.read(yodafile, asdict=True)
    return np.repeat(np.array([b.relErr for b in aos[histogram_path].bins]), 2)

def get_bin_edges(histogram_path, yodafile):
    binedges = []
    aos = yoda.read(yodafile, asdict=True)
    for b in aos[histogram_path].bins:
        binedges += list(b.xEdges)
    return binedges
