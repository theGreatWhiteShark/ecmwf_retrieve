import setuptools

with open( "README.md", "r" ) as fh:
	long_description = fh.read()

setuptools.setup(
	name = "ecmwf_retrieve",
	version = "0.0.1",
	author = "Philipp Müller",
	author_email = "thetruephil@googlemail.com",
	description = "A convenience package for downloading large amounts of data from the ECMWF using only a free account (with a formal download restriction of 30GB)",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/thegreatwhiteshark/ecmwf_retrieve",
	packages = setuptools.find_packages(),
	classifiers = (
        "Programming Language :: Python :: 3",
        "License :: GPL-3 License",
        "Operating System :: OS Independent" )
	)
		
	
