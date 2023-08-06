class panel(object):
    '''
    A panel holds histograms and other information that describe a panel of a plot

    :param title: title of the panel
    :type title: `str`
    :param height: relative height of the panel with respect to any other panels in a plot
    :type height: `float`
    :param xlabel: x-axis label
    :type xlabel: `str`
    :param ylabel: y-axis label
    :type ylabel: `str`
    :param logx: plot x-axis on a logarithmic scale?
    :type logx: `bool`
    :param logy: plot y-axis on a logarithmic scale?
    :type logy: `bool`
    :param stack: histogram stack to plot
    :type stack: :py:class:`heppy.histostack`, or `None`
    :param curves: histograms to plot as curves
    :type curves: list of :py:class:`heppy.histogram1d`
    :param bands: histograms to plot as (uncertainty) bands
    :type bands: list of :py:class:`heppy.histogram1d`
    :param points: histograms to plot as points located at the centre of each of their bins
    :type points: list of :py:class:`heppy.histogram1d`
    :param pointshift: distance to shift points by horizontally to avoid overlap and improve readability. This functionality is poorly tested and may be broken
    :type pointshift: `float`
    :param scatters: this is a bit of an oddball. You can use it to plot 2D scatters that aren't really histograms. The x-values are lower bin edges (the uppermost binedge is not used for anything) while the y-values are the areas.
    :type scatters: list of :py:class:`heppy.histogram1d`
    :param ylims: can be used to manually set lower and upper y-axis limits, e.g. ylims=(0.0, 2.0)
    :type ylims: `tuple` of `float`, or `None`
    :param legend_title: legend title
    :type legend_title: `str`
    '''
    def __init__(self, title='', height=1., xlabel='', ylabel='', logx=False, logy=False, stack=None, curves=[], bands=[], points=[], pointshift=0., scatters=[], ylims=None, nolegend=False, legend_title=None):
        super(panel, self).__init__()
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.logx = logx
        self.logy = logy
        self.stack = stack
        self.curves = curves
        self.bands = bands
        self.points = points
        self.pointshift = pointshift
        self.scatters = scatters
        self.height = height
        self.ylims = ylims
        self.nolegend = nolegend
        self.legend_title = legend_title
