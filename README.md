# gpx2dzg

[![PyPI version](https://badge.fury.io/py/gpx2dzg.svg)](https://badge.fury.io/py/gpx2dzg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/iannesbitt/gpx2dzg/blob/master/LICENSE)

This software takes GPS waypoint information stored in [GPX](https://en.wikipedia.org/wiki/GPS_Exchange_Format) files, tries to align waypoints with user marks in GSSI's proprietary DZX file format, and outputs the results to DZG (an ASCII file containing a mix of [RMC](http://aprs.gids.nl/nmea/#rmc) and/or [GGA](http://aprs.gids.nl/nmea/#gga) NMEA strings and "NMEA-like" GSSI proprietary strings). The purpose of this translation is to artifically create GPS-aware ground-penetrating radar (GPR) projects.

Sadly, at the moment this software only works with GSSI control units that produce DZX files. This means it should work for projects created with the SIR-4000, but not with the SIR-3000. SIR-3000 support is coming soon (see [future](#future)), but requires slightly more mathematical finesse, since the 3000 stores marks above the time-zero band of the GPR array instead of in a separate file.


### Note:
GPX and DZX or DZT files **MUST** contain the same number of marks for this process to work. That's because each GPS point has to be matched up with a scan number in order to tie the GPS points to marks made in the DZX or DZT by the control unit. If they do not, the script will bring up a plot showing GPX marks plotted by distance, DZX/DZT marks plotted by scan number, and velocity between GPX points for comparison. You can modify either GPX or DZX using a standard text editor, and add or remove marks based on your survey notes. If you're reading a DZT file from a SIR-3000 survey, you can remove marks 4, 5, and the mark second from the end in the mark list, by specifying `drops=[3,4,-2]` if you're using the python console, or `-r 3,4,-2` if you're using the command line. Remember, the list index starts at 0, so `drops=[3]` or `-r 3` will drop the 4th mark.

I urge you to take copious notes in the field so that you know if there will be errant marks you need to remove later. I will do what I can to help, but ultimately I am not responsible for missed GPS or GPR marks in your radar surveys (sorry!)

# installation

### simple install

If you've installed python packages before you may not need this. If you're uncomfortable installing python packages, read on. All requirements are on the Python Package Interface (PyPI), which means that you do not need to manually anything else in order for this to work (requirements should theoretically install automatically). Execute the following command in an Anaconda Prompt or `bash` terminal to install:

```bash
pip install gpx2dzg
```

### installing development versions

If you wish to install the very latest commit from github (which may be more up-to-date than the version on PyPI but also may have more bugs), simply download this repository using the "Clone or download" button above. Unzip the package to your Downloads folder, then execute the following command in an Anaconda Prompt or `bash` terminal:

```bash
pip install ~/Downloads/gpx2dzg
```

If that doesn't work, you may need to unzip differently. Try making a folder called `gpx2dzg` in your Downloads folder, then unzip all of the contents of this package to it, so that `setup.py` is located at `~/Downloads/gpx2dzg/setup.py`. 

# usage

## in python

**Note that although many of these examples use SIR-4000 DZX files, this program also works with DZTs created with the SIR-3000, which stores marks in the second row of the radar profile.**

```python
>>> import gpx2dzg.gpx2dzg as g2d
>>> g2d.convert(dzx='/path/to/dzx.DZX', gpx='/path/to/gpx.gpx', write=True)
```

### sanity check plotting

This software contains the ability to plot GPX and DZX marks next to each other, along with speed over ground, in order to visually check which points may have been missed or created erroneously in the field.

This will happen automatically if GPX and DZX mark numbers are not equal. An example is shown below:

![Sanity check plot with differing mark counts](https://github.com/iannesbitt/gpx2dzg/raw/master/img/Figure_1a.png)

### DZX/DZT point removal

You can remove mark points from the list of DZX or DZT marks by specifying `drops=[4,5,-2]`. It may be beneficial to do this and check the plot a couple of times until the GPS and SIR marks match up. Remember, the list index starts at 0, so `drops=[3]` or `-r 3` will drop the 4th mark. Adding a negative number will remove from the end of the list, so `drops=[3,-2]` will remove both the fourth point in the list and the second to last point in the list. **This software will not let you drop the first or last point** (i.e. `drops=[0]` or `drops=[-1]`) **since these are required to properly normalize the full extents of your DZT files**.

In this case, we only need to drop the second-to-last point in order to get matching DZX and GPX mark counts.

```python
>>> g2d.convert(dzx='/path/to/dzt.DZX', gpx='/path/to/gpx.gpx', plot=True, drops=[-2])
```

Note that the second to last point is removed in this second example.

![Sanity check plot with identical mark counts](https://github.com/iannesbitt/gpx2dzg/raw/master/img/Figure_1b.png)

### write results to a `.DZG` file

Add `write=True` to the function call. The program will not overwrite if there's a DZG already named the same as the DZT or DZX, instead it will name it something like `dzt-gpx2dzg.DZG`.

```python
>>> g2d.convert(dzx='/path/to/dzt.DZX', gpx='/path/to/gpx.gpx', drops=[-2], write=True)
```

### forcing a sanity check plot

To force the sanity check plot even if mark numbers are equal, simply add `plot=True`.

```python
>>> g2d.convert(dzx='/path/to/dzx.DZX', gpx='/path/to/gpx.gpx', plot=True)
```

![Sanity check plot with identical mark counts](https://github.com/iannesbitt/gpx2dzg/raw/master/img/Figure_2.png)

*This might not seem like a "sane" way to do a sanity check, but if you have a better idea I would love to hear from you.*

## on a `bash` or Anaconda Prompt command line

```bash
gpx2dzg -d /path/to/dzx.DZX -g /path/to/gpx.gpx
```

### sanity check plotting

Simply add the `-p` flag.

```bash
gpx2dzg -d /path/to/dzx.DZX -g /path/to/gpx.gpx -p
```

### DZX/DZT point removal

You can remove mark points from the list of DZX or DZT marks by adding the `-r` flag with a list of integers. Again, it may be beneficial to do this a couple of times to check that the GPS/SIR mark points in the plot match up the way you want them to. Remember, the list index starts at 0, so `-r 3` will drop the 4th mark. Adding a negative number will remove from the end of the list, so `-r 3,-2` will remove both the fourth point in the list and the second to last point in the list. **This software will not let you drop the first or last point** (i.e. `-r 0` or `-r -1`) **since these are required to properly normalize your DZT files**.

Notice in this example that the value of `-d` can point to either a SIR-3000 `DZT` file or a SIR-4000 `DZX` file.

```bash
gpx2dzg -d /path/to/dzt.DZT -g /path/to/gpx.gpx -p -r 4,5,-2
```

### write results to a `.DZG` file

Simply add the `-w` flag. The program will not overwrite if there's a DZG already named the same as the DZT or DZX, instead it will name it something like `dzt-gpx2dzg.DZG`.

```bash
gpx2dzg -d /path/to/dzt.DZT -g /path/to/gpx.gpx -p -r 4,5,-2 -w
```

## usage notes:

If no GPX file is specified, the software will look for a GPX named the same as the DZX or DZT (for example, if the DZX/DZT is named `file.DZX` or `file.DZT`, the script will look for a file named `file.gpx`).

# future:

- please [create an issue](https://github.com/iannesbitt/gpx2dzg/issues/new) if you have a feature suggestion
