"""
	This module contains some test functions that
	can be called to check if a certain component
	is doing what we expect it to do
"""

from config import config
import utils
import components

def test_connect_db( config ):
	db = utils.db_connect( config )
	print(db)
	if db:
		print("Connected to database. Trying to get a document...")
		doc = db.flucks.find_one({})
		if doc:
			#print( doc )
			print("PASS: db_connect")
	else:
		print("Error in db_connect. No handle returned.")
	

def test_insert_fluck( config ):
	db = utils.db_connect( config )
	result = components.insert_fluck( db, "5a15779bbc93104b641721d2", 1 )
	if result['status']:
		print("PASS: insert_fluck. Fluck {} inserted in database".format(result))
	else:
		print(result['query'])
		print("FAIL: Error in insert_fluck")
	

# run tests...
test_connect_db(config)
test_insert_fluck(config)
