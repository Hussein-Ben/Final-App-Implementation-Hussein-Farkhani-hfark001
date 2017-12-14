#!/usr/bin/env python3

""" 
	This module provides a set of reuseable functions
	which provide the main app functionality.
	We could even go a stage further and separate
	database interactions from logic...
"""

# import modules from Python standard library
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt

def login( db, form ):
	""" Logs a user in if the Username and Password
	    submitted in a form match a record in database

	Params:
		db: 	handle to a database
		form: 	FieldStorage object
	
	Returns:
		Dict 
	"""
	# login status is false by default
	status = False
	try:
		# get the username from the form
		username = form['username'].value
		# get the unhashed password sent in the form
		pw = form['password'].value
	except KeyError:
		# a field must be missing from the form data
		response = "I don't think you filled all the fields in..."
	else:
		# look for an account with the username
		account = db.accounts.find_one({
			"username":username,
			})
		# check if an account came back 
		if account is not None:
			# compare the unhashed password from the form
			# with the hashed version in the database
			if bcrypt.checkpw( pw.encode('utf-8'), account['password'].encode('utf-8') ):
				# if they match, output a personal greeting
				# was this a DP student?
				if account['username'] == "Sunday":
					response = "What a good kitty. Now fill in the <a href='https://moduleevaluation.gold.ac.uk/surveyPrivacyStatement/Kf4iWgP74kSxYCxRA'>module feedback form</a> and you shall have some pie."
				else:
					response = "Hello {}!".format( account['name']['first'] )
					status = True
			else:
				# if not, we know it was a wrong password
				response = "Wrong password."
		else:
			# their username didn't match, so tell them that
			response = "Sorry, I don't think I know you!"
	# return a dict with the result and a message
	return {"status":status,"msg":response}

def register_account( db, form ):
	""" Registers a new user by inserting an account
	    in the accounts collection

	Params:
		db: 	handle to a database
		form: 	FieldStorage object
	
	Returns:
		Dict 
	"""
	# registration status false by default
	status = False
	try:
		# get the username from the form
		username = form['username'].value
		# get the email from the form
		email = form['email'].value
		# get the unhashed password from the form
		password = form['password'].value
	except KeyError:
		# a field must be missing from the form data
		response = "I don't think you filled all the fields in..."
	else:
		# check if there is already an account with the email
		# or username
		result = db.accounts.find_one( { '$or': [
			{ 'username' : username },
			{ 'email': email }
		]} )
		# if so, send back a useful response
		if result:
			if email in result.values():
				response = "Email address already registered."
			else:
				response = "Username taken."
		# otherwise go ahead and make the account
		else:
			hashed_pw = bcrypt.hashpw( password.encode('utf-8'), bcrypt.gensalt() )
			query = {
				"username": username,
				"password": hashed_pw.decode('utf-8'),
				"is_admin": 0,
				"created" : datetime.now().timestamp()
			}
			# make sure name fields aren't empty
			# if they are, give them empty string values
			if 'first' in form:
				first = form['first'].value
			else:
				first = ""
			if 'last' in form:
				last = form['last'].value
			else:
				last = ""
			# append name to query
			query["name"] = { "first": first, "last": last }
			# insert the account in the database
			doc = db.accounts.insert( query )
			if doc:
				status = True
				response = "New account registered. <a href='/cgi-bin/splash.py' title='login'>Click here</a> to go Log in!"
			else:
				response = "Problem registering your account. Please refresh the page to try again."
	# return something useful...
	return {'status': status, 'msg': response}

def latest_fluck( db ):
	""" Returns details of the most recently flucked
	    cat in the database

	Params:
		db: 	handle to a database
	
	Returns:
		Dict 
	"""
	# start with an empty dict
	image = {}
	# get details of last flucked cat
	result = db.flucks.find({"is_flucked":1}).sort([('timestamp', -1)]).limit(1)
	# get the associated image
	for fluck in result:
		result2 = db.images.find({"_id":fluck["image_id"]})
	# if a doc was returned, put the bits we want in the image dict
	for doc in result2:
		image = {"url":doc["url"],"alt":doc["alt"]}
	return image

def most_flucked( db ):
	""" Returns details of the most flucked
	    cat in the database

	Params:
		db: 	handle to a database
	
	Returns:
		Dict 
	"""
	# start with an empty dict
	image = {}
	# define a pipeline of operations to get most flucked image id
	# from flucks collection
	pipeline = [
		{"$group": {"_id": "$image_id", "count": {"$sum": 1}}},
		{"$sort": {"count":-1}},
		{"$limit":1}
		]

	# apply pipeline of operations using aggregate
	result = db.flucks.aggregate( pipeline )

	# check if a result was returned
	if result:
		for fluck in result:
			# get the associated image document
			doc = db.images.find_one({"_id": fluck["_id"]})

	# if a doc was returned, put the bits we want in the image dict
	if doc:
		image = {"url":doc["url"],"alt":doc["alt"]}
	return image

def random_cat( db ):
	""" Returns details of a random cat in the database

	Params:
		db: 	handle to a database
	
	Returns:
		Dict 
	"""
	# start with an empty dict
	image = {}
	# get a random sample from images collection of size '1'
	result = db.images.aggregate(
		[{ '$sample': { 'size': 1 } }]
	)
	# if a result came back, do stuff with it...
	if result:
		# iterate through objects in the cursor (should only be 1)
		for doc in result:
			# put the bits we want in the image dict
			image = {
				'src': doc['url'],
				'alt': doc['alt'],
				'id': doc['_id']
			}
	return image

def count_flucks( db, img_id ):
	""" Returns details of a random cat in the database

	Params:
		db: 	handle to a database
		img_id:	object id of an image document
	
	Returns:
		Dict 
	"""
	# try to count flucks associated with image id
	try:
		num_flucks = db.flucks.find( {"image_id": img_id, "is_flucked":1} ).count()
	# if img_id invalid, return false rather than crashing
	except NameError:
		return False
	else:
		return num_flucks

def insert_fluck( db, img_id, is_flucked ):
	""" Inserts new fluck in flucks collection
	    based on form data

	Params:
		db: 	handle to a database
		form: 	FieldStorage object
	
	Returns:
		Bool 
	"""
	# try to insert a fluck
	query =	{ 
			"image_id": ObjectId(img_id),
			"is_flucked":is_flucked,
			"timestamp":datetime.now().timestamp() 
		} 
	try:
		result = db.flucks.insert( query )
	# if img_id invalid, return something useful
	except NameError:
		return {'status': False, 'query': query}
	# else return info about the inserted document
	else:
		return {'status': True, 'fluck_id': result}

