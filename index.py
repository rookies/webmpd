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

## IMPORT STANDARD LIBRARIES:
import sys, urllib.parse, os
## IMPORT DELIVERED LIBRARIES:
import libs.config as config
import libs.usermanager as usermanager
## IMPORT JINJA:
from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment

class WebMPD_Index(object):
	env = Environment()

	def __init__(self):
		self.env.loader = FileSystemLoader(config.path + "templates/")
	def handle_request(self, qs, environ=None):
		## Get cookie_env:
		if environ is None:
			cookie_env = os.getenv("HTTP_COOKIE")
		else:
			if "HTTP_COOKIE" in environ:
				cookie_env = environ["HTTP_COOKIE"]
			else:
				cookie_env = ""
		
		if not "page" in qs:
			if not usermanager.get_permission(cookie_env, "access"):
				return {
					"status": 302,
					"headers": {
						"Location": "index.py?page=login"
					},
					"content": ""
				}
			tpl = self.env.get_template("index_default.html")
			return {
				"status": 200,
				"headers": {
					"Content-Type": "text/html"
				},
				"content": tpl.render(
					loggedin=usermanager.is_loggedin(cookie_env),
					username=usermanager.get_username(cookie_env)
				)
			}
		elif qs["page"][0] == "login":
			if usermanager.is_loggedin(cookie_env):
				return {
					"status": 302,
					"headers": {
						"Location": "index.py"
					},
					"content": ""
				}
			else:
				tpl = self.env.get_template("login.html")
				if "error" in qs:
					err = True
				else:
					err = False
				return {
					"status": 200,
					"headers": {
						"Content-Type": "text/html"
					},
					"content": tpl.render(
						error=err
					)
				}
		elif qs["page"][0] == "loginaction":
			## Read POST data:
			if environ is None:
				data = sys.stdin.read()
			else:
				data = environ['wsgi.input'].read()
			data = dict(urllib.parse.parse_qs(data))
			if (not "password" in data and not b"password" in data) or (not "username" in data and not b"username" in data):
				## No username or no password given:
				return {
					"status": 302,
					"headers": {
						"Location": "index.py?page=login&error"
					},
					"content": ""
				}
			else:
				## Everything seems okay, prepare login data:
				if "username" in data:
					username = data["username"][0].strip()
					password = data["password"][0].strip()
				else:
					username = data[b"username"][0].strip().decode("utf-8")
					password = data[b"password"][0].strip().decode("utf-8")
				## ... and login:
				status = usermanager.login(username, password)
				if isinstance(status, dict):
					ret = {
						"status": 302,
						"headers": {
							"Location": "index.py"
						},
						"content": ""
					}
					for key, val in status.items():
						ret["headers"][key] = val
					return ret
				else:
					return {
						"status": 302,
						"headers": {
							"Location": "index.py?page=login&error"
						},
						"content": ""
					}
		elif qs["page"][0] == "logout":
			status = usermanager.logout(cookie_env)
			ret = {
				"status": 302,
				"headers": {
					"Location": "index.py"
				},
				"content": ""
			}
			if isinstance(status, dict):
				for key, val in status.items():
					ret["headers"][key] = val
			return ret

if __name__ == "__main__":
	## HANDLE THE CGI REQUEST:
	try:
		qs = urllib.parse.parse_qs(os.getenv("QUERY_STRING"), keep_blank_values=True)
		index = WebMPD_Index()
		res = index.handle_request(qs)
	except:
		print("Status: 500")
		print("Content-Type: text/plain")
		print("")
		traceback.print_last()
	else:
		print("Status: " + str(res["status"]))
		for key, val in res["headers"].items():
			print(key + ": " + val)
		print("")
		print(res["content"])
