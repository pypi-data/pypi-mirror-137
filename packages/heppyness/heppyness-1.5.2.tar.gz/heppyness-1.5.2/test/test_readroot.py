# Auxiliary modules
import numpy as np
from numpy.testing import assert_almost_equal as assert_approx
from os.path import join, dirname
import root_numpy as rnp
import ROOT
import sys

# Module to be tested
sys.path.append(join(dirname(__file__), '..'))
import heppy


#
# Set up
#
testfile = join(dirname(__file__), 'example.root')
hist2d_path = 'root_histogram_2d_name'
areas2d = np.array([[1., 5.],
       				[2., 6.],
       				[3., 7.],
       				[4., 8.]])
# Reference 2D ROOT histogram
reference_th2 = ROOT.TH2F('reference_th2', 'reference_th2', 4, -1.0, 1.0, 2, -1.0, 1.0)
# The zero padding is for the under-/overflows
reference_areas = np.transpose(np.array([
	[0., 0., 0., 0., 0., 0.],
	[0., 1., 2., 3., 4., 0.],
	[0., 5., 6., 7., 8., 0.],
	[0., 0., 0., 0., 0., 0.],]))
reference_area_errors = np.transpose(np.array([
	[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
	[0.0, 0.4, 0.3, 0.2, 0.1, 0.0],
	[0.0, 0.8, 0.7, 0.6, 0.5, 0.0],
	[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],]))
rnp.array2hist(reference_areas, reference_th2, errors=reference_area_errors)





def test_read_TH2F():
	'''
	Reading a TH2F histogram from ROOT file
	'''
	th2 = heppy.get_TH(testfile, hist2d_path)
	assert th2.GetName() == hist2d_path
	assert th2.GetNbinsX() == 4
	assert th2.GetNbinsY() == 2
	# Remember that bin indexing in ROOT starts from 1, while 0 is the underflow bin
	assert_approx( th2.GetBinContent(4, 2), 8.0 )
	assert_approx( th2.GetBinError(3, 1), 0.2 )



def test_read_binareas_2d():
	'''
	Read bin areas of a 2D histogram from ROOT file
	'''
	areas = heppy.readroot_binareas(testfile, hist2d_path)
	np.testing.assert_array_almost_equal( areas, areas2d )



def test_read_binedges_2d():
	'''
	Read bin edges of a 2D histogram from ROOT file
	'''
	binedges = heppy.readroot_binedges2d(reference_th2)
	assert len(binedges) == 2
	np.testing.assert_array_almost_equal( binedges[0], np.array([-1.0, -0.5, 0.0, 0.5, 1.0]) )
	np.testing.assert_array_almost_equal( binedges[1], np.array([-1.0, 0.0, 1]) )



def test_read_histogram_2d():
	'''
	Test reading a ROOT TH2F and creating a Heppy histogram from it
	'''
	h = heppy.readroot(testfile, hist2d_path)
	assert isinstance(h, heppy.histogram2d)
	np.testing.assert_array_almost_equal( h.areas, areas2d )
	np.testing.assert_array_almost_equal( h.binsizes, np.ones_like(areas2d) * 0.5 )
	np.testing.assert_array_almost_equal( h.heights, areas2d / 0.5 )
	statistical__1up = (reference_areas + reference_area_errors)[1:-1,1:-1]
	np.testing.assert_array_almost_equal( h.uncorr_variations['Statistical__1up'], statistical__1up )
	statistical__1down = (reference_areas - reference_area_errors)[1:-1,1:-1]
	np.testing.assert_array_almost_equal( h.uncorr_variations['Statistical__1down'], statistical__1down )
