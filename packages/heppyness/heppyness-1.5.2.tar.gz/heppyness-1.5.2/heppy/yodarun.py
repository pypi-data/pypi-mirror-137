import readyoda
import numpy as np

class Run(object):
    '''Information about a run: labels, where to find its data, etc.'''
    def __init__(self, label, nominalpath, pdfvarpaths=[], scalevarpaths=[], altpdfpaths=[]):
        '''NOTE: `pdfvarpaths` are only the variations of the nominal set, not alternative sets.'''
        super(Run, self).__init__()
        self.label = label
        self.nominalpath = nominalpath
        self.pdfvarpaths = pdfvarpaths
        self.scalevarpaths = scalevarpaths
        self.altpdfpaths = altpdfpaths
    
    
    
    def binedges(self, histogram_path):
        return readyoda.get_bin_edges(histogram_path, self.nominalpath)
    
    
    
    def nominal(self, histogram_path):
        return readyoda.get_curve(histogram_path, self.nominalpath, self.nominalpath)
    
    def statistical_uncertainty_up_down(self, histogram_path):
        relative = readyoda.get_relative_error(histogram_path, self.nominalpath)
        return self.nominal(histogram_path) * (1. + relative), self.nominal(histogram_path) * (1. - relative)
    
    
    def pdfvars(self, histogram_path):
        if not self.pdfvarpaths:
            print('Warning: no PDF variations available, returning nominal curve instead!')
            return self.nominal(histogram_path)
        #print self.pdfvarpaths
        return readyoda.get_curves(histogram_path, self.pdfvarpaths, self.nominalpath)
    
    
    
    def scalevars(self, histogram_path):
        if not self.scalevarpaths:
            print('Warning: no QCD scale variations available, returning nominal curve instead!')
            return self.nominal(histogram_path)
        return readyoda.get_curves(histogram_path, self.scalevarpaths + [self.nominalpath], self.nominalpath)
        
    
    
    def altpdf(self, histogram_path, index=0):
        if not self.altpdfpaths:
            print('Warning: no alternative PDFs available, returning nominal curve instead!')
            return self.nominal(histogram_path)
        try:
            altpdfpath = self.altpdfpaths[index]
            return readyoda.get_curve(histogram_path, altpdfpath, self.nominalpath)
        except IndexError:
            raise RuntimeError('You requested the curve for the {0}. alternative PDF, but only {} alternative PDFs are given.'.format(index+1, len(self.altpdfpaths)))
    
    
    
    def pdf_variation_up_down(self, histogram_path, clip_to_zero=True):
        pdfvars = self.pdfvars(histogram_path)
        nominal = self.nominal(histogram_path)
        #BINWIDTH = self.binedges(histogram_path)[1] - self.binedges(histogram_path)[0]
        #print pdfvars[:0] * BINWIDTH # / np.sum(nominal) * 100.
        if not self.pdfvarpaths:
            print('Warning: no PDF variations given, uncertainty band will have zero width.')
            return pdfvars, pdfvars # the band has zero width because no PDF variations were given
        if not len(self.pdfvarpaths) == 100:
            print('Warning: expecting NNPDF 3.0 with 100 PDF variations plus nominal, found {0}. If you use a different PDF set, you need to implement its uncertainty calculation. I will proceed, but using the NNPDF prescription for uncertainties, which may be incorrect for your set.'.format(len(self.pdfvarpaths)))
        shifts = np.sqrt(np.sum((pdfvars - nominal)**2, axis=0) / 100.)
        up = nominal + shifts
        #print shifts / nominal * 100.
        down = (nominal - shifts).clip(min=0) if clip_to_zero else nominal - shifts
        return up, down
    
    
    
    def scale_variation_up_down(self, histogram_path):
        scalevars = self.scalevars(histogram_path)
        if len(scalevars.shape) == 1: return scalevars, scalevars
        return np.max(scalevars, axis=0), np.min(scalevars, axis=0)



    # Make sure the histogram you pass contains all the generated events
    # Returns RELATIVE uncertainty IN PERCENT
    def integrated_yield_uncertainty_scale(self, histogram_path):
        nominal = np.sum(self.nominal(histogram_path)[::2])
        scalevars = [np.sum(var[::2]) for var in self.scalevars(histogram_path)]
        up = (max(scalevars) - nominal) /  nominal * 100.
        down = (min(scalevars) - nominal) /  nominal * 100.
        return up, down


    # Return the scale uncertainty of the inclusive integrated yield
    # or, if jets >= 0, the yield uncertainty in that exclusive jet bin.
    # Returns RELATIVE uncertainty IN PERCENT
    def yield_uncertainty_scale(self, exclusive_njet_histogram_path, jets=-1):
        if jets < 0:
            return self.integrated_yield_uncertainty_scale(exclusive_njet_histogram_path)
        nominal = self.nominal(exclusive_njet_histogram_path)
        upvar, downvar = self.scale_variation_up_down(exclusive_njet_histogram_path)
        up = (upvar[::2][jets] - nominal[::2][jets]) / nominal[::2][jets] * 100.
        down = (downvar[::2][jets] - nominal[::2][jets]) / nominal[::2][jets] * 100.
        return up, down        



    # Make sure the histogram you pass contains all the generated events
    # Returns RELATIVE uncertainty IN PERCENT
    def integrated_yield_uncertainty_pdf(self, histogram_path):
        nominal = np.sum(self.nominal(histogram_path)[::2])
        pdfvars = [np.sum(var[::2]) for var in self.pdfvars(histogram_path)]
        shifts = np.sqrt(np.sum((pdfvars - nominal)**2, axis=0) / 100.)
        up = shifts /  nominal * 100.
        down = -shifts / nominal * 100.
        return up, down



    # Return the PDF uncertainty of the inclusive integrated yield
    # or, if jets >= 0, the yield uncertainty in that exclusive jet bin.
    # Returns RELATIVE uncertainty IN PERCENT
    def yield_uncertainty_pdf(self, exclusive_njet_histogram_path, jets=-1):
        if jets < 0:
            return self.integrated_yield_uncertainty_pdf(exclusive_njet_histogram_path)
        nominal = self.nominal(exclusive_njet_histogram_path)
        upvar, downvar = self.pdf_variation_up_down(exclusive_njet_histogram_path)
        up = (upvar[::2][jets] - nominal[::2][jets]) / nominal[::2][jets] * 100.
        down = (downvar[::2][jets] - nominal[::2][jets]) / nominal[::2][jets] * 100.
        return up, down


