# PolSpectra
A package for creating and manipulating tables of polarized radio spectra.

This package was motivated for the need for a volume-efficient way of storing the Stokes IQUV spectra of compact sources: avoiding massive duplication of information (in FITS headers) and also avoiding the need for very large numbers of files (potentially half a billion files for the entirety of POSSUM!). The design set out to fulfill these goals: it would be space efficient (minimal duplication), easily readable (without requiring special software), and flexible in terms of combining data from separate instruments and observations into a single file if desired.

This has been implemented using the FITS table format. The use of variable-length array columns allow the spectra to be stored efficiently, even if different rows have different numbers of channels (although this has only limited official support under the FITS standard). The basic unit for a row is a single source-observation (the same source observed multiple times gets a row for each individual observation), with a 'source_number' column that can group together multiple observations under the same source.

The resulting tables should be readable by anything that supports FITS tables (with the variable-length array column standard). This Python package offers a streamlined way to create these tables as objects in Python and read/write them to FITS format.

Designed for use by the [CIRADA](cirada.org) Polarization pipeline, for processing of data for the POSSUM and VLASS radio surveys, and for use in the [RM-tools](https://github.com/CIRADA-Tools/RM-Tools) polarization analysis package (not yet supported).

Cameron Van Eck (cameron.van.eck (at) dunlap.utoronto.ca)

