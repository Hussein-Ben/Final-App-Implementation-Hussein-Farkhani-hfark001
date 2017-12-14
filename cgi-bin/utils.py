#!/usr/bin/env python3

""" 
	This module provides a set of reuseable utility functions
	This is a Google style docstring by the way.
	Read more about them here: 
	https://www.python.org/dev/peps/pep-0257/
"""

from pymongo import MongoClient

def db_connect( config ):
	""" Provides a connection to mongoDB database
	
	Returns:
		Object: A handle to a mongoDB database 
	"""
	# try to create instance of MongoClient object
	try:
		client = MongoClient( config['SERVER_ADDRESS'], config['PORT'] )
	except:
		# raise a custom exception
		raise Exception("Problem connecting to the database!")
	# if we have a mongo client...
	else:
		# switch to the specified database
		db = client[ config['DATABASE_NAME'] ]

		# check a handle was returned
		if db is not None:
			# return a handle to the database
			return db

def render_template( temp_path, data=[] ):
	""" Reads in an HTML string from file
	    replacing any placeholders with values
	    supplied in data list.

	    Input params:
		temp_path: the path to the template file
		data: optional list of data values

	    Returns:
		String: A formatted string of HTML
	"""
	try:
		# open and read the template file
		with open(temp_path, 'r') as f:
			html = f.read()
	except:
		raise Exception("Could not open template")
	else:
		if data is not None:
			try:
				# replace placeholders with data in list
				html = html.format(*data)
			except:
				raise Exception("Problem parsing data to template")
		return html	
