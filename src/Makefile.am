## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = length_calc.ui


## The main script
bin_SCRIPTS = length_calc.py

## Directory where .class files will be installed
length_calcdir = $(pythondir)/length_calc


length_calc_PYTHON = \
	length_calc.py \
	calculator_conversion.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
