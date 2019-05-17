import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from geopy.distance import geodesic


def setup(ax, xmax=5):
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