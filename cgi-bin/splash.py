#!/usr/bin/env python3

# import modules from Python Standard library
import cgi
import cgitb
cgitb.enable()

# import custom modules
from config import config
import utils
import components

# connect to a database
db = utils.db_connect( config )

# tell browser to expect HTML 
print("Content-Type: text/html\n")

# render header HTML
print( utils.render_template( config['TEMPLATE_DIR'] + 'header.html') )

# get any data sent with the GET or POST request
# this may be required by multiple components
sent_data = cgi.FieldStorage()

# -------- START OF FUNCTIONAL COMPONENTS ----------->>>

# ---------- HANDLE LOGIN FORM SUBMISSIONS ----------

# check if login form was submitted
if 'btn_login' in sent_data:
	# it was, so call the login function
	result = components.login(db, sent_data)
	msg = result['msg']
else:
	# message displayed in login form will be empty
	msg = ""

print( utils.render_template( config['TEMPLATE_DIR'] + 'login.html', data=[msg] ) )

# ---------- HANDLE FLUCK FORM SUBMISSIONS -----------

# check if fluck occurred
if 'btn_fluck' in sent_data:
	# user flucked, so is_flucked is 1
	result = components.insert_fluck(db, sent_data['img_id'].value, 1)
# check if skip occurred
elif 'btn_skip' in sent_data:
	# user skipped, so is_flucked is 0
	result = components.insert_fluck(db, sent_data['img_id'].value, 0)

# ------ GET LATEST FLUCKED CAT -------

# call latest_fluck to get image details
image = components.latest_fluck( db )
# check image isn't empty before proceeding...
if image:
	# it isn't so render the template
	print( utils.render_template( config['TEMPLATE_DIR']+'latest_fluck.html', data=[image["url"],image["alt"]] ) )
	
# ------ GET MOST FLUCKED CAT -------

# call latest_fluck to get image details
image = components.most_flucked( db )
# check image isn't empty before proceeding...
if image:
	# it isn't so render the template
	print( utils.render_template( config['TEMPLATE_DIR']+'most_flucked.html', data=[image["url"],image["alt"]] ) )

# ------ SERVE UP A RANDOM CAT WITH STATS ------

# get one random document from images collection
current_cat = components.random_cat( db )

if current_cat:
	# render serve_cat template, passing it dynamic data
	print( utils.render_template( config['TEMPLATE_DIR']+'serve_cat.html', data=[current_cat['src'], current_cat['alt']] ) )

	# count flucks of current cat
	num_flucks = components.count_flucks( db, current_cat['id'] )

# check num_flucks exists
if num_flucks:
	# render cat_stats template, passing it dynamic data
	print( utils.render_template( config['TEMPLATE_DIR']+'cat_stats.html', data=[num_flucks] ) )

# ------- OUTPUT FLUCK/SKIP FORM ----------

if current_cat:
	# render form_fluck template, passing it dynamic data
	print( utils.render_template( config['TEMPLATE_DIR']+'form_fluck.html', data=["/cgi-bin/splash.py", current_cat['id']] ) )

# --------- /END OF COMPONENTS --------

# render footer
print( utils.render_template( config['TEMPLATE_DIR']+'footer.html' ) )
