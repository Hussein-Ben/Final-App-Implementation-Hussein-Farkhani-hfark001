#!/usr/bin/env python3

"""
	This script handles the processing
	of the register form in the catflucks application.
	Note: 
		there is code repetition here...
		What could we do about that?
	Also note:
		this functionality is not yet integrated
		with the rest of the application.
		How could it be?
"""

# import modules from Python standard library
import cgi
import cgitb
cgitb.enable()
import bcrypt

# import custom modules
from config import config
import utils
import components

# connect to database
db = utils.db_connect( config )

# tell the browser we are outputting HTML
print("Content-Type: text/html\n")

# render header HTML
print( utils.render_template( config['TEMPLATE_DIR'] + 'header.html') )

# get the form data
form = cgi.FieldStorage()

# check that register form was submitted
if 'btn_register' in form:
	result = components.register_account( db, form )
	msg = result['msg']
else:
	msg = ""

# output the form as HTML
print( utils.render_template( config['TEMPLATE_DIR'] + 'register.html', data=[msg] ) )

# render footer
print( utils.render_template( config['TEMPLATE_DIR']+'footer.html' ) )
