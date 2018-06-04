#!/usr/bin/env python 
## Using the python 3.6 

import os # Interaction with the operation system
import copy # Copy objects without sideeffects (actual copying instead
			# of references)
import datetime
import time # two time packages are necessary to get the current POSIX
			# time. (Used as a session key)
import netCDF4 # Handling of the NetCDF files.
## Package handling the access of the servers of the ECMWF
from ecmwfapi import ECMWFDataServer

def download_queries( server, options_list ):
	'''This function performs the actual download of the data set.

	It is intended to work with a list of requests. If the user wants
	to download just a single file, she either has to use the raw
	:func:`ecmwfapi.ECMWFDataServer.retrieve` function of the
	**ecmwfapi** package or to embed the request into a list.

	Parameters
	----------
	server : ecmwfapi.api.ECMWFDataServer
	    An instance created using :class:`ecmwfapi.ECMWFDataServer`. 
		It will be used to communicate with the MARS server of the
		ECMWF and to retrieve the data. 
	options_list : list
	    A list of dictionaries. Each of the specifies the data set and
	    the target file of a valid ECMWF retrieve.

	Returns
	-------
	bool
	    Returns 0 if no error was thrown during the download(s).

	See Also
	--------
	retrieve : Function handling the whole request.
	ecmwfapi.ECMWFDataServer.retrieve
	'''
	for ooptions in options_list:
		server.retrieve( ooptions )

	return 0
	
def erainterim_default_options():
	'''Returns a dictionary of the default options for the ERA-Interim
	data set.

	The default request is tailored to download the sea surface and
	the 2 metre temperature created in the analysis step using the
	operational atmospheric model. It will contain the whole grid
	spanning the earth at all times up to March 28th 2018.

	For a detailed description of the individual parameters please see
	comments in the code of this function or the documentation of the
	MARS server of the ECMWF.
	https://software.ecmwf.int/wiki/display/UDOC/MARS+user+documentation

	Parameters
	----------

	Returns
	-------
	dict
	    An example request to download the ERA-Interim data set of the
		ECMWF.

	See Also
	--------
	retrieve : Function handling the whole request.
	cera20_default_options : Function returning a request to download
	    the CERA-20C data set.
	'''
	default_options = {
		## Uses an 'Operational Atmospheric Model'. This specifies
		## the use of the default atmospheric model (IFS) to produce
		## the forecast step in the reanalysis in the ERA-Interim run
		## (the Cy31r2 system used for `oper`). It has a higher
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
		## sst - sea surface temperature in K
		'param'     : "2t/sst",
		## Download the representation of the data using longitude
		## and latitude.
		'repres'    : "ll",
		## Select the ERA-Interim data set.
		## Full list
		## https://software.ecmwf.int/wiki/display/WEBAPI/Available+ECMWF+Public+Datasets 
		'dataset'   : "interim",
		'class'     : "ei",
		## Get all four time steps.
		'time'      : "00/06/12/18",
		## Download the whole time series.
		'date'      : "1979-01-01/to/2018-02-28",
		## Type of field to be retrieved. Get the full list
		## http://apps.ecmwf.int/codes/grib/format/mars/type/ 
		## It is set to 'analysis'. What's an analysis? It is a run of
		## the 4D-Var system used to assimilate 'new' observation data
		## into the current trajectory of the climate model. 
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
	'''Returns a dictionary of the default options for the CERA-20C
	data set.

	The default request is tailored to download the sea surface and
	the 2 metre temperature created in the analysis step using the
	operational atmospheric model. It will contain the whole grid
	spanning the earth at all times up to March 28th 2018.

	For a detailed description of the individual parameters please see
	comments in the code of this function or the documentation of the
	MARS server of the ECMWF.
	https://software.ecmwf.int/wiki/display/UDOC/MARS+user+documentation

	Parameters
	----------

	Returns
	-------
	dict
	    An example request to download the CERA-20C data set of the
		ECMWF.

	See Also
	--------
	retrieve : Function handling the whole request.
	erainterim_default_options : Function returning a request to download
	    the ERA-Interim data set.
	'''
	default_options = {
		## Uses an 'Operational Atmospheric Model'. This specifies
		## the use of the default atmospheric model to simulate the
		## climate in the ERA-Interim run. It has a higher
		## resolution then the one coupled to the Wave model. Get
		## the full list at 
		## http://apps.ecmwf.int/codes/grib/format/mars/stream/ 
		'stream'    : "enfo",
		## Determining the level (height) of the data. Here: surface
		'levtype'   : "sfc",
		## Specify meteorolocal parameters, which are going to be
		## retrieved. Get the full list
		## http://apps.ecmwf.int/codes/grib/param-db/
		## 2t  - 2 metre temperature in K
		'param'     : "tp/mx2t/mn2t",
		## Download the representation of the data using longitude
		## and latitude.
		'repres'    : "ll",
		## Select the ERA-Interim data set.
		## Full list
		## https://software.ecmwf.int/wiki/display/WEBAPI/Available+ECMWF+Public+Datasets 
		'dataset'   : "cera20c",
		'class'     : "ep",
		## Do not use any forecast but just the analysis.
		'step'      : "03/06/12",
		## Get all four time steps.
		'time'      : "00/12",
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
	'''Split a date range in a ECMWF request into a list of the
	individual years.

	Since there is a fixed limit of the size of the data, which
	can be downloaded using a free account at the ECMWF servers
	(30GB), the request will be splitted into individual years and
	concatenated into a single NetCDF file later on.
	
	Parameters
	----------
	date_string : str
	    A string specifying the temporal range of the data set. It
	    is expected to be either of the format *1999-01-01* or
	    *1999-01-01/to/2000-01-01*.
	   
	Returns
	-------
	list
	    If the `date_string` is either a single date or just
	    covers data within the range of a single year, the output
	    will be list with `date_string` as its sole element.
	    If, on the other hand, `date_string` spanned multiple years,
	    the output will be a list with each element spanning a single
	    year.

	Raises:
	   TypeError: If `date_string` is not a string.
	   SyntaxError: If `date_string` is not of the format *1999-01-01* or *1999-01-01/to/2000-01-01*.
	   ValueError: If the beginning of the temporal range in `date_string` starts before 1890, after the end of the range, or if the range ends later than 2100.

	Notes
	-----
	Takes the string residing in the *date* key of a dictionary
	specifying a request to the MARS API of the ECMWF.

	See Also
	--------
	retrieve : Function handling the whole request.
	split_query_into_list_of_queries : Split one request into several
 	   requests using the splitting of its *date* key performed by
 	   this function.
	'''
	## Check the format of the input.
	if type( date_string ) is not str:
		raise TypeError(
			'Wrong type of the "date_string" argument. A string is required.' )

	## Split the string to extract the start and the end of the date
	## range.
	date_string_split = date_string.split( "/" )

	if len( date_string_split ) == 1:
		## Only one date is specified. Return the string without
		return [ date_string_split ]
	elif len( date_string_split ) != 3:
		raise SyntaxError( 'Unexpected input format.' )
	else:
		## Verifying the format of the input
		if len( date_string_split[ 0 ] ) != 10 or len( date_string_split[ 2 ] ) != 10:
			raise SyntaxError( 'Unexpected input format.' )
		
		## Extract the years of the query range as numerical values
		## and generate a sequence of all years within it.
		year_start = int( date_string_split[ 0 ][ 0 : 4 ] )
		year_end = int( date_string_split[ 2 ][ 0 : 4 ] )

		## Sanity check of the extracted years.
		if year_end < year_start:
			raise ValueError(
				'Wrong format in the *date* key: Starting point dates after the end point.' )
		elif year_start == year_end:
			## Since the query is only over one year, there shouldn't
			## be any problems with the maximum download size.
			return [ date_string_split[ 0 ], date_string_split[ 2 ] ]
		if year_start < 1890:
			raise ValueError( 
				'Wrong format in the *date* key: The ECWMF data set date back so many years?' )
		if year_end > 2100:
			raise ValueError( 
				'Wrong format in the *date* key: The ECWMF data set date so far in the future?' )

		## The start and end of the temperoral range have to be
		## handled with care. For all other years it's just the
		## XXXX-01-01 till the XXXX-12-31
		## Each year, except of the first and last one, will just
		## have the 1st of January as date. The two exceptions are
		## added as is.
		date_list = [ date_string_split[ 0 ] + "/to/" + \
						  str( year_start ) + "-12-31" ]
		for ll in range( year_start + 1, year_end ):
			date_list.append( str( ll ) + "-01-01/to/" + \
							  str( ll ) + "-12-31" )
							  
		date_list.append( str( year_end ) + "-01-01/to/" + \
				date_string_split[ 2 ] )
		
		return date_list

def split_query_into_list_of_queries( options ):
	'''Split the dictionary specifying a request to ECWMF server
	separate dictionaries according to its temporal range. 

	The splitting of the *date* key in `options` will be performed
	using the :func:`split_date_into_list_of_years` function.

	Parameters:
	   options : dict:
	      A dictionary specifying all parameters of the MARS API of
		  ECMWF. For a full list of all available keywords please see 
		  https://software.ecmwf.int/wiki/display/UDOC/MARS+user+documentation

    Returns:
	   list:
	       A list of dictionaries with each one being a valid request via the MARS API.

	See Also:
	   retrieve : Function handling the whole request.
	   split_date_into_list_of_years : Performs the splitting of the temporal range of `options` according to the string in `options.date`.
	'''

	## Split the date into the individual years.
	options_date_split = split_date_into_list_of_years(
		options.get( 'date' ) )

	## Create a list of option
	options_list = []
	for ll in range( len( options_date_split ) ):
		options_list.append( copy.deepcopy( options ) )
		## Use only one slide in the time domain
		options_list[ ll ][ 'date' ] = options_date_split[ ll ]
		## Write the slide to a separate output
		options_list[ ll ][ 'target' ] = \
		  ".".join( options_list[ ll ].get( 'target'
											).split( "." )[ :-1 ] ) + \
						'_' + str( ll ).zfill( 3 ) + '_.nc'
		
	return options_list

def combine_netcdf_files( output_name, session_key = None, delete = True ):
	'''Combines all NetCDF files downloaded during one MARS session (a
	single request split into the individual years) into a single file.

	The combination itself will **not** be performed in Python itself
	but the system function *ncrcat* will be called instead. Please
	make sure the program is properly installed on your system.
	http://nco.sf.net/

	Parameters
	----------
	output_name : str
	   String specifying the name of the combined netCDF file. In
	   general this will be the value of the *target* key of the
	   original ECMWF request.
	session_key : int, optional
	   String specifying the individual session. It is generated using
	   the current time and date. If *None*, all NetCDF files in the
	   current directory will be joined. Default = None.
	delete : bool, optional
	   Logical value specifying whether or not to delete the
	   downloaded chunk NetCDF files joined by this function. Default
	   = True. 

	Returns
	-------
	int
	   Returns 0 if everything worked out and no error was thrown.

	Notes
	-----
	This function assumes all the netCDF files, which should be
	combined, share exactly the same format. Any change in the
	dimensionality or amount of variables will cause the function to
	fail. 

	See Also
	--------
	retrieve : Function handling the whole request.
	'''
	## Get all NetCDF files present in the current directory.
	files_present = os.listdir()
	files_netcdf = [] # This list will contain all netCDF file names.
	for ffile in files_present:
		if ffile.find( '.nc' ) > -1:
			## The file has an .nc extension
			if session_key is None or \
				ffile.find( str( session_key ) ) > -1:
				## The session_key is valid
				files_netcdf.append( ffile )

	## Use the command line program `ncrcat` to join the NetCDF files.
	## It is provided by the NCO toolkit http://nco.sourceforge.net/
	print( "\nCombining the chunk requests into one NetCDF file...\n" )
	os.system( "ncrcat " + " ".join( files_netcdf ) + \
			   " -o " + str( output_name ) )

	if delete:
		## Delete all the retrieved files containing chunks of full
		## request.
		print( "\nDeleting the chunk request files...\n" )
		for ffiles in files_netcdf:
			os.remove( ffiles )
			
	return 0

def retrieve( options = None, delete = True ):
	'''Downloads a public data set of arbitrary size from the ECMWF
	using only a free account.

	In order to not reach the limit of 30 GB maximum download size for
	the free access to the public data sets of the ECWMF, regardless
	of the amount of specified parameters and times, the query will be
	split into the individual years, downloaded separately, and
	combined into a single file afterwards. This kind of splitting is
	performed in favor of downloading just one parameter a time since
	it is less demanding for the servers of the ECMWF and thus
	rewarded by a quicker introduction into their queueing system. In
	addition the request for a single data set at all times in the
	CERA-20C data set can easily exceed the 30GB limit.

	The resulting data set will be stored in the current folder the
	python script is called in.

	Parameters
	----------
	options : dict, optional
	   A dictionary specifying all parameters of the MARS API of
	   ECMWF. For a full list of all available keywords please see 
	   https://software.ecmwf.int/wiki/display/UDOC/MARS+user+documentation
	   You are free to use no or just a couple of options of the MARS
	   service. The remaining ones (or all, if missing) will be filled
	   with those specified in the output of the function
	   :func:`ecmwf_erainterim_default_options`. Default = None.
	delete : bool, optional
	   Logical value specifying whether or not to delete the
	   downloaded chunk NetCDF files joined by this function. Default
	   = True. 

	Returns
	-------
	int
	   Returns 0 if everything worked out and no error was thrown.

	Notes
	-----
	The function will internally generate an instance of an
	:class:`ecmwfapi.ECMWFDataServer` object to handle the actual download. 

	See Also
	--------
	erainterim_default_options : Default options for a request to the
	   MARS API of the ECMWF.
	split_query_into_list_of_queries : Splits the original request
	   into smaller parts, which do not exceed the 30GB limit.
	download_queries : Downloads a list of requests.
	combine_netcdf_files : Combines the individual requests into a
	   single netCDF file.
	'''
	## Check the type of the provided input
	if options is not None and type( options ) is not dict:
		raise TypeError(
			'Wrong type of the "options" argument. A dict is required.' )
	
	## Integrate the specified options into the default ones.
	default_options = erainterim_default_options()

	## In case the user supplied some options, override their
	## corresponding counterpart in the default setting.
	if options is not None:
		for kkey in list( options.keys() ):
			default_options[ kkey ] = options.get( kkey )
	options = default_options

	## Separate the provided query in multiple ones according to the
	## number of years provided in the temporal range.
	options_split = split_query_into_list_of_queries( options )

	## In addition there will also be a session key created from the
	## current time and date to identify all the files in the download
	## folder produced by this script
	session_key = int( time.mktime(
		datetime.datetime.now().timetuple() ) )
	## Append the session key to the filenames
	for ll in range( len( options_split ) ):
		options_split[ ll ][ 'target' ] = \
		  ".".join( options_split[ ll ].get( 'target'
											).split( "." )[ :-1 ] ) + \
						'_' + str( session_key ) + '_.nc'

	## Object representing the data server of the ECMWF
	server = ECMWFDataServer()

	## Download the list of provided queries
	download_queries( server, options_split )

	## Combine the individual NetCDF files into a single,
	## comprehensive one.
	combine_netcdf_files( output_name = options.get( 'target' ),
						  session_key = session_key, delete = delete )
	
	return 0
