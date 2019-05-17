from datetime import datetime
from geopy.distance import geodesic
import math


def printmsg(msg):
    '''Prints with date/timestamp.'''
    print('%s - %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg))


def genericerror(type='file'):
    printmsg('please attach this %s to a new github issue (https://github.com/iannesbitt/gpx2dzg/issues/new)')
    printmsg('        or send it to ian.nesbitt@gmail.com in order to have the format assessed. please also')
    printmsg('        include the output of the program (i.e. copy and paste this text and the text above in')
    printmsg('        the message) as this will drastically speed up my ability to help you! thanks!')
    printmsg('  ~!~>  I am happy to help but please note that I am not responsible for the content of your')
    printmsg('  ~!~>  files, only the working-ness of this software. I appreciate your understanding!')


def gpxerror(e=''):
    printmsg('ERROR TEXT: %s' % e)
    genericerror('GPX')


def dzxerror(e=''):
    printmsg('ERROR TEXT: %s' % e)
    genericerror('DZX')


def writeerror(e=''):
    printmsg('ERROR: could not write the file because you do not have write permission in this directory.')
    printmsg('ERROR TEXT: %s' % e)


def dd2dms(dd): # credit to stackoverflow user Erik L (https://stackoverflow.com/a/10286690/4648080)
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,str(seconds).replace('.',''))


def course(pointA, pointB): # credit to github user jeromer (https://gist.github.com/jeromer/2005586)
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def sog(lat0=0, lon0=0, time0=datetime.now(), lat=0, lon=0, time=datetime.now()):
    '''
    takes lat/lon at time=0 and time=1, plus time0 and time1
    returns speed over ground in knots
    '''

    sog = geodesic((lat, lon), (lat0, lon0)).meters / (time - time0).seconds

    return sog/0.514444444
