#!/usr/bin/env python 
## Using the python 3.6 

import ecmwf_retrieve.ecmwf_retrieve as ec

request = ec.cera20_default_options()
request[ 'stream' ] = 'enda'
request[ 'param' ] = '2t/sst'
request[ 'target' ] = 'cera-20c-analysis.nc'
request[ 'time' ] = "00:00:00/03:00:00/06:00:00/09:00:00/12:00:00/15:00:00/18:00:00/21:00:00",
request[ 'date' ] = '1901-01-01/to/2010-12-13'
request[ 'step' ] = '0'
request[ 'expver' ] = '1'
request[ 'number' ] = '0'
request[ 'resol' ] = 'av'
		
ec.retrieve( request )
