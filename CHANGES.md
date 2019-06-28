# Changelog

## changes since 0.0.4
- added figure at top of readme
- added "intended audience" classifier in `setup.py`

## changes since 0.0.3
- fixed major bug ([#1](https://github.com/iannesbitt/gpx2dzg/issues/1)) which caused locations to be written incorrectly in NMEA sentences. versions 0.0.3 and down suffer from this bug and should not be used.
- changed name of decimal degree conversion function from `dd2dms` to `dd2ddm` to reflect the change in purpose to address [#1](https://github.com/iannesbitt/gpx2dzg/issues/1)
- added GGA sentence output to accompany RMC, with a calculated egm96 geoid height!
- added [MANIFEST](https://github.com/iannesbitt/gpx2dzg/blob/master/MANIFEST.in), which includes a small and simple 15-arcminute egm96 geoid model
- added mark numbering for ease of mark removal using `-r`, which stays consistent even if marks are removed
- updated README plots to reflect numbering change

## changes since 0.0.2
- added a subplot depicting GPX marks vs time
- added the ability to handle DZX with or without a zero mark
- updated readme examples and text

## changes since 0.0.1
- added the ability to read marks from SIR-3000 DZT files
- added the ability to remove marks read from either DZT or DZX files
- updated readme examples and text
