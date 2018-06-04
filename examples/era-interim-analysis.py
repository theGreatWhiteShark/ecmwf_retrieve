#!/usr/bin/env python 
## Using the python 3.6 

import ecmwf_retrieve.ecmwf_retrieve as ec

ec.retrieve( options = { 'date' : '1979-01-01/to/2018-02-28',
							 'param' : '2t/sst',
							 'target' : 'era-interim-analysis.nc' } )
