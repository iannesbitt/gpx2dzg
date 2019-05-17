# gpx2dzg

[![PyPI version](https://badge.fury.io/py/gpx2dzg.svg)](https://badge.fury.io/py/gpx2dzg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/iannesbitt/gpx2dzg/blob/master/LICENSE)

This software takes GPS waypoint information stored in [GPX](https://en.wikipedia.org/wiki/GPS_Exchange_Format) files, tries to align waypoints with user marks in GSSI's proprietary DZX file format, and outputs the results to DZG (an ASCII file containing a mix of [RMC](http://aprs.gids.nl/nmea/#rmc) and/or [GGA](http://aprs.gids.nl/nmea/#gga) NMEA strings and "NMEA-like" GSSI proprietary strings). The purpose of this translation is to artifically create GPS-aware ground-penetrating radar (GPR) projects.

Sadly, at the moment this software only works with GSSI control units that produce DZX files. This means it should work for projects created with the SIR-4000, but not with the SIR-3000. SIR-3000 support is coming soon (see [future](#future)), but requires slightly more mathematical finesse, since the 3000 stores marks above the time-zero band of the GPR array instead of in a separate file.


#### Note:
GPX and DZX files **MUST** contain the same number of marks for this process to work. If they do not, the script will bring up a plot showing GPX marks plotted by distance, DZX marks plotted by scan number, and velocity between GPX points for comparison. You can modify either GPX or DZX using a standard text editor, and add or remove marks based on your survey notes. I will do what I can to help, but ultimately I am not responsible for missed GPS or GPR marks in your radar surveys (sorry!)

# installation

Installation should be simple. If you've installed python packages before you may not need this. If you're uncomfortable installing python packages, read on. All requirements are on the Python Package Interface (PyPI), which means that you do not need to install anything else in order for this to work. Simply download this repository using the "Clone or download" button above. Unzip the package to your Downloads folder, then execute the following command in an Anaconda Prompt or `bash` terminal to install:

```bash
pip install ~/Downloads/gpx2dzg
```

If that doesn't work, you may need to unzip differently. Try making a folder called `gpx2dzg` in your Downloads folder, then unzip all of the contents of this package to it, so that `setup.py` is located at `~/Downloads/gpx2dzg/setup.py`. 

# usage

## in python

```python
>>> import gpx2dzg.gpx2dzg as g2d
>>> g2d.convert(dzx='/path/to/dzx.DZX', gpx='/path/to/gpx.gpx')
```

#### sanity check plotting

This software contains the ability to plot GPX and DZX marks next to each other, along with speed over ground, in order to visually check which points may have been missed or created erroneously in the field.

This will happen automatically if GPX and DZX mark numbers are not equal. An example is shown below:

![Sanity check plot with differing mark counts](https://github.com/iannesbitt/gpx2dzg/raw/master/img/Figure_1.png)

To force the sanity check plot, simply add `plot=True`.

```python
>>> g2d.convert(dzx='/path/to/dzx.DZX', gpx='/path/to/gpx.gpx', plot=True)
```

![Sanity check plot with identical mark counts](https://github.com/iannesbitt/gpx2dzg/raw/master/img/Figure_2.png)

*This might not seem like a "sane" way to do a sanity check, but if you have a better idea I would love to hear from you.*

## on a `bash` or Anaconda Prompt command line

```bash
gpx2dzg -d /path/to/dzx.DZX -g /path/to/gpx.gpx
```

#### sanity check plotting

Simply add the `-g` flag.

```bash
gpx2dzg -d /path/to/dzx.DZX -g /path/to/gpx.gpx -g
```

## usage notes:

If no GPX file is specified, the software will look for a GPX named the same as the DZX (for example, if the DZX is named `file.DZX`, the script will look for a file named `file.gpx`).

# future:

- SIR-3000 support (please [create an issue](https://github.com/iannesbitt/gpx2dzg/issues/new) if you would like this to happen sooner rather than later)
