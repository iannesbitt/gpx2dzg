import os, sys
import getopt
import gpx2dzg.functions as fx
import gpx2dzg.help as help
import gpx2dzg.io as io
import gpx2dzg.plot as px

def convert(dzx='', gpx='', plot=False):
    if os.path.exists(dzx) == False:
        fx.printmsg('ERROR: specified dzx file does not exist. exiting.')
        sys.exit(2)
    if os.path.exists(gpx) == False:
        fx.printmsg('ERROR: specified gpx file does not exist. exiting.')
        sys.exit(2)
    fx.printmsg('dzx file: %s' % dzx)
    fx.printmsg('gpx file: %s' % gpx)

    dzxmarks, gpxmarks = [], []

    dzxmarks = io.readdzx(dzx=dzx)
    fx.printmsg('found %s dzx marks' % len(dzxmarks))

    gpxmarks = io.readgpx(gpx=gpx)
    fx.printmsg('found %s gpx marks' % len(gpxmarks.waypoints))

    if len(gpxmarks.waypoints) == len(dzxmarks):
        fx.printmsg('mark counts match! outputting to DZG now (same directory and name as the DZX)')
        fx.printmsg('if a DZG already exists, another will be written with "-gpx2dzg" in the name.')
        dzg = os.path.splitext(dzx)[0] + '.DZG'
        if os.path.exists(dzg):
            fx.printmsg('a DZG already exists. saving with "-gpx2dzg" in the name.')
            dzg = os.path.splitext(dzx)[0] + '-gpx2dzg.DZG'
        fx.printmsg('output file: %s' % dzg)
        io.write(dzg=dzg, dzxmarks=dzxmarks, gpxmarks=gpxmarks)
    else:
        fx.printmsg('mark counts do not match. foregoing output and generating sanity check plot.')
        plot = True

    if plot:
        px.sanityplot(dzx=dzxmarks, dzxname=dzx, gpx=gpxmarks, gpxname=gpx)


def main():
    dzx, gpx = None, None
    plot = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'pd:g:', ['plot', 'dzx=', 'gpx='])
    except getopt.GetoptError as e:
        fx.printmsg('ERROR: invalid argument(s) supplied')
        fx.printmsg('error text: %s' % e)
        fx.printmsg(help.help_text)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'): # the help case
            fx.printmsg(help.help_text)
            sys.exit()
        if opt in ('-d', '--dzx'): # dzx input file
            if arg:
                dzx = arg
                if '~' in dzx:
                    dzx = os.path.expanduser(dzx) # if using --input=~/... tilde needs to be expanded
        if opt in ('-g', '--gpx'): # gpx input file
            if arg:
                gpx = arg
                if '~' in gpx:
                    gpx = os.path.expanduser(gpx) # if using --input=~/... tilde needs to be expanded
        if opt in ('-p', '--plot'): # plot
            plot = True
    if dzx and gpx:
        convert(dzx=dzx, gpx=gpx, plot=plot)
    elif dzx:
        fx.printmsg('only DZX input specified. gpx2dzg will search for an identically named GPX...')
        gpx = os.path.splitext(dzx)[0] + '.gpx'
        convert(dzx=dzx, gpx=gpx, plot=plot)
    else:
        fx.printmsg('ERROR: no input files specified')
        sys.exit(2)


if __name__ == '__main__':
    main()