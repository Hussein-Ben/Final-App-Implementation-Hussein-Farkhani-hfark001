#!/usr/bin/env python3 

""" A Simple Web Server
	Run with ./simpleServer.py
	Make sure all cgi scripts are executable
	for single script:
		 chmod +x simpleServer.py
	or for a whole directory:
		 chmod -r +x cgi-bin/
"""

import http.server										# import http.server module
import cgitb; cgitb.enable()							# import and enable cgitb module for exception handling

PORT = 8000												# specifies the port number to accept connections on

server = http.server.HTTPServer 						# provides simple web server
handler = http.server.CGIHTTPRequestHandler 			# provides request handler
server_address = ("", PORT)								# specify server directory and port number
handler.cgi_directories = ["/","/cgi-bin","/htbin"]		# where CGI scripts will reside in relation to the `server' directory

print("Starting server...")					# outputs a message 
httpd = server(server_address, handler)		# creates the server, passing it the server address and port number, as well as the CGI handler (httpd stands for HTTP Daemon)
print("serving at port", PORT)				# outputs a message
httpd.serve_forever()						# puts program in infinite loop so that the server can `serve_forever'
