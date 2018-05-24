#!/usr/bin/env python 
## Using the python 3.6 

import os # Interaction with the operation system
## Package handling the access of the servers of the ECMWF
from ecmwfapi import ECMWFDataServer

def download_queries( server, options ):
	'''
	   This function performs the actual download of the data set.

	   server  - an ecmwfapi.ECMWFDataServer instance.
	   options - a dictionary specifying the dataset and the target
	             file 
	'''
	server.retrieve( options )
	
def erainterim_default_options():
	'''
	Returns a dictionary of the default options for the ERA-Interim
	data set.
	'''
	default_options = {
		## Uses an 'Operational Atmospheric Model'. This specifies
		## the use of the default atmospheric model to simulate the
		## climate in the ERA-Interim run. It has a higher
		## resolution then the one coupled to the Wave model. Get
		## the full list at 
		## http://apps.ecmwf.int/codes/grib/format/mars/stream/ 
		'stream'    : "oper",
		## Determining the level (height) of the data. Here: surface
		'levtype'   : "sfc",
		## Specify meteorolocal parameters, which are going to be
		## retrieved. Get the full list
		## http://apps.ecmwf.int/codes/grib/param-db/
		## 2t  - 2 metre temperature in K
		'param'     : "2t",
		## Download the representation of the data using longitude
		## and latitude.
		'repres'    : "ll",
		## Select the ERA-Interim data set.
		## Full list
		## https://software.ecmwf.int/wiki/display/WEBAPI/Available+ECMWF+Public+Datasets 
		'dataset'   : "interim",
		'class'     : "ei",
		## Do not use any forecast but just the analysis.
		'step'      : "0",
		## Get all four time steps.
		'time'      : "00/06/12/18",
		## Download the whole time series.
		'date'      : "1979-01-01/to/1989-02-31",
		## Type of field to be retrieved. Get the full list
		## http://apps.ecmwf.int/codes/grib/format/mars/type/ 
		## It is set to 'analysis'. What's an analysis? It
		## indicated the state of the climate is set to a certain
		## state (initial conditions/observations) and a forecast
		## is run for e.g. a day. Afterwards the next observations
		## in line are used to adjust the state of the model,
		## another forecast is scheduled and so on.
		## The 'reanalysis' indicates old observations are used. So
		## what we want to have is the reanalysis of type analysis.
		'type'      : "an",
		## Get all data around the globe
		'domain'    : "G",
		## Use the grid of the archived version. This yields the best
		## resolution possible.
		'grid'      : "0.75/0.75", 
		## Don't make the MARS server keep an internal cache copy of the
		## requested files.
		'use'       : "infrequent", 
		'format'    : "netcdf",
		## File to save the netCDF object in.
		'target'    : "era-interim.nc" }
	return default_options 

def cera20_default_options():
	'''
	Returns a dictionary of the default options for the CERA-20C
	data set.
	'''
	default_options = {
		## Uses an 'Operational Atmospheric Model'. This specifies
		## the use of the default atmospheric model to simulate the
		## climate in the ERA-Interim run. It has a higher
		## resolution then the one coupled to the Wave model. Get
		## the full list at 
		## http://apps.ecmwf.int/codes/grib/format/mars/stream/ 
		'stream'    : "oper",
		## Determining the level (height) of the data. Here: surface
		'levtype'   : "sfc",
		## Specify meteorolocal parameters, which are going to be
		## retrieved. Get the full list
		## http://apps.ecmwf.int/codes/grib/param-db/
		## 2t  - 2 metre temperature in K
		'param'     : "2t",
		## Download the representation of the data using longitude
		## and latitude.
		'repres'    : "ll",
		## Select the ERA-Interim data set.
		## Full list
		## https://software.ecmwf.int/wiki/display/WEBAPI/Available+ECMWF+Public+Datasets 
		'dataset'   : "cera20c",
		'class'     : "ep",
		## Do not use any forecast but just the analysis.
		'step'      : "0",
		## Get all four time steps.
		'time'      : "00/03/06/09/12/15/18/21",
		## Download the whole time series.
		'date'      : "1979-01-01/to/1989-02-31",
		## Type of field to be retrieved. Get the full list
		## http://apps.ecmwf.int/codes/grib/format/mars/type/ 
		## It is set to 'analysis'. What's an analysis? It
		## indicated the state of the climate is set to a certain
		## state (initial conditions/observations) and a forecast
		## is run for e.g. a day. Afterwards the next observations
		## in line are used to adjust the state of the model,
		## another forecast is scheduled and so on.
		## The 'reanalysis' indicates old observations are used. So
		## what we want to have is the reanalysis of type analysis.
		'type'      : "an",
		## Get all data around the globe
		'domain'    : "G",
		## Use the grid of the archived version. This yields the best
		## resolution possible.
		'grid'      : "0.75/0.75", 
		## Don't make the MARS server keep an internal cache copy of the
		## requested files.
		'use'       : "infrequent", 
		'format'    : "netcdf",
		## File to save the netCDF object in.
		'target'    : "cera-20c.nc" }
	return default_options 

def split_date_into_list_of_years( date_string ):
	'''
	   Takes the string residing in `date` key of the data set options
	   and splits it into a list of date string if the series spans
	   multiple years. 

	   Since there is a fixed limit of the size of the data, which
	   can be downloaded using a free account at the ECMWF servers
	   (30GB), the request will be splitted into individual years and
	   concatenated into a single NetCDF file later on.

	   The function expects the input string to be either of the
	   format `1999-01-01` or `1999-01-01/to/2000-01-01`.

	   Value: List containing the different years. The first and the
	          last entry define the temporal range of the query.
	'''
	## Check the format of the input.
	if date_string is not str:
		raise Exception(
			'Wrong type of the "date_string" argument. A string is required.' )

	## Split the string to extract the start and the end of the date
	## range.
	date_string_split = date_string.split( "/" )

	if len( date_string_split ) == 1:
		## Only one date is specified. Return the string without
		return [ date_string_split ]
	elif: len( date_string_split ) != 3:
		raise Exception( 'Unexpected input format.' )
	else:
		## Verifying the format of the input
		if len( date_string_split[ 0 ] ) != 10 or
			len( date_string_split[ 2 ] ) != 10:
			raise Exception( 'Unexpected input format.' )
		
		## Extract the years of the query range as numerical values
		## and generate a sequence of all years within it.
		year_start = int( date_string_split[ 0 ][ 0 : 4 ] )
		year_end = int( date_string_split[ 2 ][ 0 : 4 ] )

		## Sanity check of the extracted years.
		if year_end < year_start:
			raise Exception(
				'Wrong format in the *date* key: Starting point dates after the end point.' )
		elif: year_start == year_end:
			## Since the query is only over one year, there shouldn't
			## be any problems with the maximum download size.
			return [ date_string_split[ 0 ], date_string_split[ 2 ] ]
		if year_start < 1890:
			raise Expection( 
				'Wrong format in the *date* key: The ECWMF data set date back so many years?' )
		if year_start > 2100:
			raise Expection( 
				'Wrong format in the *date* key: The ECWMF data set date so far in the future?' )

		## Each year, except of the first and last one, will just
		## have the 1st of January as date. The two exceptions are
		## added as is.
		date_list = [ date_string_split[ 0 ] ]
		date_list.extend( list( map( lambda ss: str( ss ) + '-01-01',
									list( range( year_start + 1,
												year_end ) ) ) ) )
		date_list.append( date_string_split[ 2 ] )
		return date_list

def split_query_into_list_of_queries( options, 			

def retrieve( options = None ):
	'''
	   This function downloads a data set of the ECMWF. 

	   options - A dictionary specifying the dataset and the target
	             file. You are free to use just a couple of options of
				 the MARS service. The remaining ones (or all if
				 missing) will be filled with those specified in
				 `ecmwf_erainterim_default_options`.

	   The function will internally generate an instance of an
	   ecmwfapi.ECMWFDataServer object to handle the actual download.

	   Using the second argument you can choose various parameters to
	   determine the query to the ECMWF server. See
	   https://software.ecmwf.int/wiki/display/UDOC/MARS+keywords for
	   a comprehensive list of all possible parameter options.
	   Per default the ones defined in the function
	   `ecmwf_erainterim_default_options` will be used.

	   In order to not reach the limit of 30 GB maximum download size
	   for the free access to the public data sets of the ECWMF,
	   regradless of the amount of specified parameters and times, the
	   query will be split into the individual year, downloaded
	   separately, and combined into a single file afterwards. This
	   splitting is performed in favor of downloading just one
	   parameter a time since it is less demanding for the servers of
	   the ECMWF and thus rewarded by a quicker introduction into
	   their queueing system.
	   
	   The resulting data set will be stored in a folder names
	   according to the `dataset` field in the options.
	'''
	## Check the type of the provided input
	if options is not None and type( options ) is not dict:
		raise Exception(
			'Wrong type of the "options" argument. A dict is required.' )
	
	## Integrate the specified options into the default ones.
	default_options = eratinterim_default_options()

	## In case the user supplied some options, override their
	## corresponding counterpart in the default setting.
	if options is not None:
		for kkey in list( options.keys() ):
			default_options[ kkey ] = options.get( kkey )

	## Split the date into the individual years.
	options_date_split = split_date_into_list_of_years(
		default_options.get( 'date' ) )

	## Separate the provided query in multiple ones according to the
	## number of years provided in the temporal range.
	options_split = split_query_into_list_of_queries(
		default_options, options_date_split )

	## Download the content in a folder named after the 'target' key in
	## the options dictionary
	if not os.path.isdir( options.get( 'target' ) ):
		## This folder can be used by the user herself and the group
		## she is belonging to.
		## Mind the 'o' for an octal!
		os.mkdir( options.get( 'target' ), 0o770 ) 

	## Object representing the data server of the ECMWF
	server = ECMWFDataServer()

	## Download the list of provided queries
	download_queries()

	## Combine the individual NetCDF files into a single,
	## comprehensive one.

	
	return 0
