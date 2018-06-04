A wrapper library around the [Python
package](https://software.ecmwf.int/wiki/display/WEBAPI/Access+ECMWF+Public+Datasets)
provided by the [ECMWF](https://software.ecmwf.int/wiki/) to download
data sets via the MARS API.

# Motivation

It is rather easy and convenient to get a **free account at the
ECMWF** and to use their Python package to download publicly 
available data sets, like ERA-Interim or CERA-20C. But if you want to
include multiple parameters at all time steps, dates, and grid
points you very soon reach the **download limit of 30GB** superimposed
onto the free account. 

This package helps you to circumvent this maximum size by splitting
your requests into separated ones (one for every year) and combining
all the downloaded netCDF files into a single file afterwards. Note:
**this only works with netCDF** and not with the GRIB data type.

# Requirements

Make sure you have the [netCDF
operator](http://nco.sourceforge.net/) tools installed on your system.

``` bash
## On Debian-based systems
sudo apt install nco
```
Or, if you are working with Anaconda

``` bash
conda install -c conda-forge nco
```

In addition, be sure you have the **netcdf4** and **ecmwfapi** package
installed.

``` bash
pip install https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz
```

Apart from the requirements on the software side you still need to
register a free account at the ECMWF. See
[this](https://software.ecmwf.int/wiki/display/WEBAPI/Access+ECMWF+Public+Datasets)
guide for instructions.

# Installation

First, clone the package to your local computer

``` bash
git clone https://github.com/theGreatWhiteShark/ecmwf_retrieve
```

jump to the folder containing the project, and install it using the
*setup.py*.

``` bash
cd ecmwf_retrieve
python setup.py install
```

# Documentation

The documentation of the project is provided as *HTML* file and can be
accessed (from the root of the repository) via

``` bash
firefox doc/_build/html/index.html
```

If you want to build the documentation on your own, be sure to have
both the **sphinx** and **sphinxcontrib-napoleon** package
installed. Afterwards, jump to the *doc* folder and compile the it to
the format you are interested in. E.g.

``` bash
# Compile the HTML version of the documentation.
cd doc
make html
```

# Usage

The main function of the provided package is called *retrieve* as in
the package provided by the ECMWF. But it also comes with some
convenience functions specifying default parameters for a ERA-Interim
requests allowing the user to just specify the key-value pairs she
once to alter.

``` python
# Load the module as 'ec'
import ecmwf_retrieve.ecmwf_retrieve as ec

# View the default options
ec.erainterim_default_options()

# Download data from the ECMWF
ec.retrieve( options = { 
	'date' : '1979-01-01/to/1981-02-28',
	'param' : '2t', 
	'target' : 'era-interim-analysis.nc' } )
```

More examples can be found in the [examples](examples/) folder.
