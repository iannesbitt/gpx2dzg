# gpx2dzg

This software takes GPS waypoint information stored in [GPX](https://en.wikipedia.org/wiki/GPS_Exchange_Format) files, tries to align waypoints with user marks in GSSI's proprietary DZX file format, and outputs the results to DZG (an ASCII file containing a mix of [RMC](http://aprs.gids.nl/nmea/#rmc) and/or [GGA](http://aprs.gids.nl/nmea/#gga) NMEA strings and "NMEA-like" GSSI proprietary strings). The purpose of this translation is to artifically create GPS-aware ground-penetrating radar (GPR) projects.

Sadly, at the moment this software only works with GSSI control units that produce DZX files. This means it should work for projects created with the SIR-4000, but not with the SIR-3000. SIR-3000 support is coming soon, but requires slightly more mathematical finesse, since the 3000 stores marks above the time-zero band of the GPR array instead of in a separate file.


#### Note:
GPX and DZX files **MUST** contain the same number of marks for this process to work. If they do not, the script will bring up a plot showing GPX marks plotted by distance, and DZX marks plotted by scan number for comparison. You can modify either GPX or DZX using a standard text editor, and add or remove marks based on your survey notes. I will do what I can to help, but ultimately I am not responsible for missed GPS or GPR marks in your radar surveys (sorry!)

# installation

Installation should be simple. If you've installed python packages before you may not need this. If you're uncomfortable installing python packages, read on. All requirements are on the Python Package Interface (PyPI), which means that you do not need to install anything else in order for this to work. Simply download this repository using the "Clone or download" button above. Unzip the package to your Downloads folder, then execute the following command to install:

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

This will happen automatically if GPX and DZX mark numbers are not equal. To force the sanity check plot, simply add `plot=True`.

```python
>>> g2d.convert(dzx='/path/to/dzx.DZX', gpx='/path/to/gpx.gpx', plot=True)
```

## on a `bash` command line

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