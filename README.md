# gpx2dzg

This software takes GPS waypoint information stored in [GPX](https://en.wikipedia.org/wiki/GPS_Exchange_Format) files, tries to align waypoints with user marks in GSSI's proprietary DZX file format, and outputs the results to DZG (an ASCII file containing a mix of NMEA strings and GSSI proprietary strings). The purpose of this translation is to artifically create GPS-aware ground-penetrating radar (GPR) projects.

Sadly, at the moment this software only works with GSSI control units that produce DZX files. This means it should work for projects created with the SIR-4000, but not with the SIR-3000. SIR-3000 support is coming soon, but requires slightly more mathematical finesse, since the 3000 stores marks above the time-zero band of the GPR array instead of in a separate file.


#### Note:
GPX and DZX files **MUST** contain the same number of marks for this process to work. If they do not, the script will bring up a plot showing GPX marks plotted by distance, and DZX marks plotted by scan number for comparison. You can modify either GPX or DZX using a standard text editor, and add or remove marks based on your survey notes. I will do what I can to help, but ultimately I am not responsible for missed GPS or GPR marks in your radar surveys (sorry!)

# usage

Coming soon
