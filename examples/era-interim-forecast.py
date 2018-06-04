#!/usr/bin/env python 
## Using the python 3.6 

import ecmwf_retrieve.ecmwf_retrieve as ec

ec.retrieve( options = { 'date' : '1979-01-01/to/2018-02-28',
							 ## Use the forecast to extract
							 ## information from the climate model
							 ## instead of the observation data.
							 'type' : 'fc',
							 ## tp - total precipitation
							 ## mx2t - max. temp. since the last step
							 ## mn2t - min. temp. since the last step
							 'param' : 'tp/mx2t/mn2t',
							 ## Some steps to accumulate the data in
							 ## (in order to explore the data set).
							 'step' : '03/06/12',
							 'time' : '00/12',
							 'target' : 'era-interim-forecast.nc' } )
