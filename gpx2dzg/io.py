import os, sys
import gpxpy
import geomag
import pynmea2
import xml.etree.ElementTree as et
from geopy.distance import geodesic
import gpx2dzg.functions as fx

def readdzx(dzx=''):
    dzxmarks = [0,]

    ## unclear why there are (possibly multiple) different formats of DZX.
    ## we have to test to see which kind this is
    with open(dzx, 'r') as f:
        tree = et.parse(f)
    root = tree.getroot()

    try:
        # try the 'TargetGroup' type
        fx.printmsg('testing DZX data type (currently supported types are "File" and "TargetGroup")')
        for item in root.findall('./{www.geophysical.com/DZX/1.02}TargetGroup'):
            for child in item:
                if 'TargetWayPt' in child.tag:
                    for gchild in child:
                        if 'scanSampChanProp' in gchild.tag:
                            dzxmarks.append(int(gchild.text.split(',')[0]))
        assert len(dzxmarks) > 1
        fx.printmsg('INFO: DZX type is standard ("TargetGroup")')
    except AssertionError as e:
        try:
            # the standard type: 'File'
            dzxmarks = []
            for item in root.findall('./{www.geophysical.com/DZX/1.02}File'):
                for child in item:
                    if 'Profile' in child.tag:
                        for gchild in child:
                            if 'WayPt' in gchild.tag:
                                for ggchild in gchild:
                                    if 'scan' in ggchild.tag:
                                        dzxmarks.append(int(ggchild.text))
            assert len(dzxmarks) > 1
            fx.printmsg('INFO: DZX type is atypical ("File")')
            fx.printmsg('DZX read successful. marks: %s' % len(dzxmarks))
            fx.printmsg('                    traces: %s' % dzxmarks[-1])
        except AssertionError as e:
            fx.printmsg('ERROR: could not read DZX information because the data type is not one we recognize. keep calm and read below.')
            fx.dzxerror(e)
            sys.exit(2)

    return dzxmarks


def readgpx(gpx=''):
    g = []
    try:
        with open(gpx, 'r') as f:
            g = gpxpy.parse(f) # devastatingly simple, in comparison to the mess above
        assert len(g.waypoints) > 0
        fx.printmsg('GPX read successful. marks: %s' % len(g.waypoints))
    except AssertionError as e:
        fx.printmsg('ERROR: no waypoints in file. please check GPX contents.')
        fx.gpxerror(e)
    return g

def write(dzg='', dzxmarks=None, gpxmarks=None):
    g = gpxmarks.waypoints
    try:
        with open(dzg, 'w') as f:
            m = 0
            for mark in dzxmarks:
                f.write('$GSSIS,%s,-1\n' % (mark))

                t = '%02d%02d%02d' % (g[m].time.hour, g[m].time.minute, g[m].time.second)
                a = 'A'
                lat = '%02d%02d.%s' % fx.dd2dms(abs(g[m].latitude))
                lon = '%03d%02d.%s' % fx.dd2dms(abs(g[m].longitude))
                if g[m].latitude >= 0:
                    latd = 'N'
                else:
                    latd = 'S'
                if g[m].longitude >= 0:
                    lond = 'E'
                else:
                    lond = 'W'
                if m == 0:
                    kt = '%05.1f' % fx.sog(lon=g[m+1].longitude, lat=g[m+1].latitude, time=g[m+1].time,
                                           lon0=g[m].longitude, lat0=g[m].latitude, time0=g[m].time)
                    crs = '%05.1f' % 0.
                else:
                    kt = '%05.1f' % fx.sog(lon=g[m].longitude, lat=g[m].latitude, time=g[m].time,
                                           lon0=lon0, lat0=lat0, time0=time0)
                    crs = '%05.1f' % fx.course((lat0, lon0),(g[m].latitude, g[m].longitude))
                lat0, lon0, time0 = g[m].latitude, g[m].longitude, g[m].time
                d = '%s%02d%02d' % (str(g[m].time.year)[2:], g[m].time.month, g[m].time.day)
                v = geomag.declination(g[m].latitude, g[m].longitude)
                var = '%05.1f' % abs(v)
                if v >= 0:
                    vard = 'E'
                else:
                    vard = 'W'
                rmc = pynmea2.RMC(talker='GP', sentence_type='RMC',
                                  data=(t, a, lat, latd, lon, lond, kt, crs, d, var, vard))
                f.write(str(rmc) + '\n\n\n')

                m += 1

    except PermissionError as e:
        fx.writeerror(e)
        sys.exit(2)
