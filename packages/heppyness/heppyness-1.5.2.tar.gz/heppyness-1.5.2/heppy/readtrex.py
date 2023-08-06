#!/usr/bin/env python3

import numpy as np
import heppy as hp
import os


def readtrex(trexfile, unfolded_format=False):
    """Reads Heppy histogram from TRExFitter YAML format.

    Requires PyYAML.

    IMPORTANT: the uncertainties are treated as correlated uncertainties, since
    their actual correlations cannot be inferred from the histogram. So treat
    them with care: they're fine for plotting and looking at individual bins,
    but do not rebin the histogram or do statistical testing involving its shape
    and assume that you will find correct results.

    :param trexfile: path to input file.
    :type trexfile: ``str``
    :param unfolded_format: set this to True if reading the YAML format that
    TRExFitter uses for unfolded cross sections.
    :type unfolded_format: ``bool``
    """
    import yaml
    if not unfolded_format:
        raise NotImplementedError('Reading TRExFitter YAML has only been '
            'implemented for its format used for unfolded cross sections so '
            'far.')
    with open(trexfile, 'r') as infile:
        bin_properties = yaml.safe_load(infile)
        binedges = [bin_properties[0]['range'][0]] # lower edge of first bin
        nominals = []
        ups = []
        downs = []
        for bin_property in bin_properties:
            binedges.append(bin_property['range'][1]) # append upper bin edge
            nominal = bin_property['mean']
            upshift = bin_property['uncertaintyUp'] # signed!
            downshift = bin_property['uncertaintyDown'] # signed!
            nominals.append(nominal)
            ups.append(nominal+upshift)
            downs.append(nominal+downshift)
        name = os.path.splitext(trexfile)[0]
        provenance = os.path.expandvars(os.path.abspath(trexfile))
        return hp.histogram1d(np.array(binedges), np.array(nominals),
            areas=True, name=name, corr_variations={
            'TRExFitter_unfolding__up' : np.array(ups),
            'TRExFitter_unfolding__down' : np.array(downs)},
            attributes={'provenance' : provenance})
    raise ValueError('Could not successfully read histogram from TRExFitter '
        f'YAML file {trexfile}.')
