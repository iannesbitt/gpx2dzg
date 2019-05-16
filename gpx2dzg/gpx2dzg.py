import os, sys
import getopt
import gpxpy
from geopy.distance import geodesic
import gpx2dzg.functions as fx
import gpx2dzg.help.help_text as help

def convert(dzx='', gpx=''):
	if os.path.exists(gpx) == False:
		fx.printmsg('ERROR: specified gpx file does not exist. exiting.')
		sys.exit(2)
	if os.path.exists(dzx) == False:
		fx.printmsg('ERROR: specified dzx file does not exist. exiting.')
		sys.exit(2)

	fx.printmsg('gpx file: %s' % gpx)
	fx.printmsg('dzx file: %s' % dzx)

	## unclear why there are two different formats of DZX.
	## testing to see which kind this is
	


def main():
	dzx, gpx = None, None

	try:
		opts, args = getopt.getopt(sys.argv[1:],
								   'd:g:', ['dzx=', 'gpx='])
	except getopt.GetoptError as e:
		fx.printmsg('ERROR: invalid argument(s) supplied')
		fx.printmsg('error text: %s' % e)
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-h', '--help'): # the help case
			fx.printmsg(help)
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
	if dzx and gpx:

		convert(dzx=dzx, gpx=gpx)
	elif dzx:
		gpx = os.path.splitext(dzx)[0] + '.gpx'
		convert(dzx=dzx, gpx=gpx)
	else:
		fx.printmsg('ERROR: no input files specified')
		sys.exit(2)


if __name__ == '__main__':
	main()