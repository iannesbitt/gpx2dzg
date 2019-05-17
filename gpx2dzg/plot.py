import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from geopy.distance import geodesic


def setup(ax, xmax=5):
    """Gets the axis ready for number line style plotting.

    Parameters
    ----------
    ax : matplotlib axis instance
        The plot axis to operate on.
    xmax : int or float
        The maximum x value to plot on the number line.
    """

    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, 1)
    ax.patch.set_alpha(0.0)

def distance(gpx=None):
    """Converts list of GPX waypoints to a list of distances (in meters) from the origin (0).

    Parameters
    ----------
    gpx : gpxpy.GPX
        The list of GPX waypoints to process.

    Returns
    -------
    list
        A list of distances (in meters) from the origin for plotting.

    """
    i = 0
    dist = [0]
    for pt in gpx.waypoints:
        lat = pt.latitude
        lon = pt.longitude
        if i > 0:
            dist.append(geodesic((lat, lon), (lat0, lon0)).meters + dist[-1])
        lat0 = lat
        lon0 = lon
        i += 1
    return dist

def sanityplot(gpx=None, gpxname='GPX', dzx=None, dzxname='DZX'):
    """Creates two number line plots for comparison of mark location and scan number.

    Parameters
    ----------
    gpx : gpxpy.GPX
        The list of GPX waypoints to plot.
    gpxname : str
        The name of the GPX file being read. This will be used as axis label text.
    dzx : list
        The list of DZX marks to plot. Each item in the list is a scan number at which a mark was recorded.
    gpxname : str
        The name of the DZX file being read. This will be used as axis label text.

    Returns
    -------
    plot instance
        Creates a matplotlib figure with two axes showing number lines with mark locaitons plotted on each.
    """
    n = 1
    name = [gpxname, dzxname]
    label = ['distance (m)', 'scan number']
    title = ['Sanity check plot: GPX and DZT marks', '']
    dist = distance(gpx)
    fig = plt.figure(figsize=(10, 2.5))
    fig.set_facecolor('white')
    for data in [dist, dzx]:
        ax = plt.subplot(2, 1, n)
        setup(ax, xmax=data[-1])
        ax.xaxis.set_major_locator(ticker.LinearLocator(3))
        ax.xaxis.set_minor_locator(ticker.LinearLocator(31))
        ax.text(0.0, 0.4, "%s marks - count: %s" % (name[n-1], len(data)),
                fontsize=10, transform=ax.transAxes)
        plt.xlabel(label[n-1])
        plt.title(title[n-1])
        for x in data:
            ax.scatter(x,0.1)
        n += 1
    plt.tight_layout()
    plt.show()