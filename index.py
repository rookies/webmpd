#!/usr/bin/python3
#  index.py
#  
#  Copyright 2013 Robert Knauer <robert@privatdemail.net>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#

## IMPORT EXCEPTION HANDLER:
try:
	import libs.handler as handler
except BaseException as e:
	print("Content-Type: text/html")
	print("Status: 500")
	print("")
	print("Failed to import Handler library!")
	print(e)
	exit()
## IMPORT STANDARD LIBRARIES:
import sys, urllib.parse, os
## IMPORT DELIVERED LIBRARIES:
import libs.config as config
import libs.usermanager as usermanager
## IMPORT JINJA:
from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
## INIT TEMPLATE ENGINE:
env = Environment()
env.loader = FileSystemLoader(config.path + "templates/")
## PARSE QUERY STRING:
qs = urllib.parse.parse_qs(os.getenv("QUERY_STRING"), keep_blank_values=True)
## RENDER PAGE:
if not "page" in qs:
	if not usermanager.get_permission("access"):
		handler.set_status(302)
		handler.set_header("Location", "index.py?page=login")
	tpl = env.get_template("index_default.html")
	print(tpl.render(
		loggedin=usermanager.is_loggedin()
	))
elif qs["page"][0] == "login":
	if usermanager.is_loggedin():
		handler.set_status(302)
		handler.set_header("Location", "index.py")
	else:
		tpl = env.get_template("login.html")
		if "error" in qs:
			err = True
		else:
			err = False
		print(tpl.render(
			error=err
		))
elif qs["page"][0] == "loginaction":
	## Read POST data:
	data = urllib.parse.parse_qs(sys.stdin.read())
	if not "password" in data or not "username" in data:
		## No username or no password given:
		handler.set_status(302)
		handler.set_header("Location", "index.py?page=login&error")
	else:
		## Everything seems okay, prepare login data:
		username = data["username"][0].strip()
		password = data["password"][0].strip()
		## ... and login:
		if usermanager.login(username, password):
			handler.set_status(302)
			handler.set_header("Location", "index.py")
		else:
			handler.set_status(302)
			handler.set_header("Location", "index.py?page=login&error")
elif qs["page"][0] == "logout":
	usermanager.logout()
	handler.set_status(302)
	handler.set_header("Location", "index.py")
