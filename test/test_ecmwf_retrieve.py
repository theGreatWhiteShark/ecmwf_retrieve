## Some unit tests for the functions in the `ecmwf_retrieve` package.

import unittest
import ecmwf_retrieve.ecmwf_retrieve as ec

default_era = ec.erainterim_default_options()
default_cera = ec.cera20_default_options()

class TestStringSplitting( unittest.TestCase ):

	def test_exception_handling_in_string_splitting( self ):
		print( 'Test, whether the exception handling in the `split_date_into_list_of_years` functions works.\n' )
		with self.assertRaises( TypeError ):
			ec.split_date_into_list_of_years( 1979 )
		with self.assertRaises( SyntaxError ):
			ec.split_date_into_list_of_years( '1979-01-01/to/' )
		with self.assertRaises( SyntaxError ):
			ec.split_date_into_list_of_years( '1979-01-01/to1982-01-02' )
		with self.assertRaises( SyntaxError ):
			ec.split_date_into_list_of_years( '1979-01-01/to/1989/01/02' )
		with self.assertRaises( SyntaxError ):
			ec.split_date_into_list_of_years( '1979-01-01/to/1989-0102' )
		with self.assertRaises( SyntaxError ):
			ec.split_date_into_list_of_years( '1979-01-01/to/1989-01--02' )
		with self.assertRaises( ValueError ):
			ec.split_date_into_list_of_years( '1982-01-01/to/1981-01-01' )
		with self.assertRaises( ValueError ):
			ec.split_date_into_list_of_years( '1882-01-01/to/1981-01-01' )
		with self.assertRaises( ValueError ):
			ec.split_date_into_list_of_years( '1982-01-01/to/2101-01-01' )

	def test_splitting_of_dates( self ):
		print( 'Test, whether the splitting of the `date` key in a list pairs of the\n individual beginnings and ends of a years works.\n' )
		self.assertEqual(
			ec.split_date_into_list_of_years(
			"1900-02-01/to/1904-02-05" ),
			['1900-02-01/to/1900-12-31',
			 '1901-01-01/to/1901-12-31',
			 '1902-01-01/to/1902-12-31',
			 '1903-01-01/to/1903-12-31',
			'1904-01-01/to/1904-02-05'] )

class TestDictHandling( unittest.TestCase ):

	def test_era_default( self ):
		print( 'Test, whether the ERA-Interim default object has the proper format\n' )
		self.assertEqual( type( default_era ), dict )
		self.assertEqual( "_".join( default_era.keys() ),
						  'stream_levtype_param_repres_dataset_class_time_date_type_domain_grid_use_format_target' )
		self.assertEqual( "_".join( default_era.values() ),
						  'oper_sfc_2t/sst_ll_interim_ei_00/06/12/18_1979-01-01/to/2018-02-28_an_G_0.75/0.75_infrequent_netcdf_era-interim.nc' )

	def test_cera_default( self ):
		print( 'Test, whether the CERA-20C default object has the proper format\n' )
		self.assertEqual( type( default_cera ), dict )
		self.assertEqual( "_".join( default_cera.keys() ),
						  'stream_levtype_param_repres_dataset_class_step_time_date_type_domain_grid_use_format_target' )
		self.assertEqual( "_".join( default_cera.values() ),
						  'enfo_sfc_tp/mx2t/mn2t_ll_cera20c_ep_03/06/12_00/12_1979-01-01/to/1989-02-31_an_G_0.75/0.75_infrequent_netcdf_cera-20c.nc')

	def test_retrieve_exceptions( self ):
		print( 'Test, whether the retrieve function handles exceptions.\n' )
		with self.assertRaises( TypeError ):
			ec.retrieve( 1979 )
		
if __name__ == '__main__':
	unittest.main()
