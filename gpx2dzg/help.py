from datetime import datetime
from gpx2dzg.__init__ import __version__, name

year = datetime.now().year
author = 'Ian Nesbitt'
affil = 'School of Earth and Climate Sciences, University of Maine'

help_text = u'''Help text:
############################################################
 gpx2dzg version %s

 Copyleft (GPLv3) %s %s 2017-%s
 %s
############################################################

usage:
gpx2dzg -d input.DZX -g input.gpx [OPTIONS]

required flags:
    FLAG     |       ARGUMENT       |       FUNCTIONALITY
-d, --dzx    | file: /dir/f.DZX|DZT | specify an input DZX or DZT file
-g, --gpx    | file: /dir/f.gpx     | specify an input gpx file

options:
   OPTION    |       ARGUMENT       |       FUNCTIONALITY
-w, --write  |  n/a                 | if set, write a DZG file in the same directory as the DZX/DZT.
-p, --plot   |  n/a                 | if set, show a troubleshooting plot comparing distance per GPX mark versus scan number per DZX mark.
''' % (__version__, u'\U0001F12F', author, year, affil)