#!/usr/bin/python3
#  fastcgi.py
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
import urllib.parse, sys, traceback, io
## IMPORT DELIVERED LIBRARIES:
import libs.config as config
from ajax import WebMPD_Ajax
from index import WebMPD_Index
## IMPORT FLUP:
from flup.server.fcgi import WSGIServer

class WebMPD_FastCGI(object):
	ajax = WebMPD_Ajax()
	index = WebMPD_Index()
	responses = {200: 'OK', 201: 'Created', 202: 'Accepted', 203: 'Non-Authoritative Information', 204: 'No Content', 205: 'Reset Content', 206: 'Partial Content', 400: 'Bad Request', 401: 'Unauthorized', 402: 'Payment Required', 403: 'Forbidden', 404: 'Not Found', 405: 'Method Not Allowed', 406: 'Not Acceptable', 407: 'Proxy Authentication Required', 408: 'Request Timeout', 409: 'Conflict', 410: 'Gone', 411: 'Length Required', 412: 'Precondition Failed', 413: 'Request Entity Too Large', 414: 'Request-URI Too Long', 415: 'Unsupported Media Type', 416: 'Requested Range Not Satisfiable', 417: 'Expectation Failed', 100: 'Continue', 101: 'Switching Protocols', 300: 'Multiple Choices', 301: 'Moved Permanently', 302: 'Found', 303: 'See Other', 304: 'Not Modified', 305: 'Use Proxy', 306: '(Unused)', 307: 'Temporary Redirect', 500: 'Internal Server Error', 501: 'Not Implemented', 502: 'Bad Gateway', 503: 'Service Unavailable', 504: 'Gateway Timeout', 505: 'HTTP Version Not Supported'}
	
	def __init__(self):
		self.ajax.mpd_connect()
	def handle_request(self, environ, start_response):
		if "SCRIPT_FILENAME" in environ:
			## Parse query string:
			qs = urllib.parse.parse_qs(environ["QUERY_STRING"], keep_blank_values=True)
			## REQUEST TO ajax.py:
			if environ["SCRIPT_FILENAME"] == config.path + "ajax.py":
				try:
					res = self.ajax.handle_request(qs)
				except:
					start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
					s = io.StringIO()
					traceback.print_last(file=s)
					return s.getvalue()
				else:
					start_response('200 OK', [('Content-Type', 'text/html')])
					return res
			## REQUEST TO index.py:
			elif environ["SCRIPT_FILENAME"] == config.path + "index.py":
				try:
					res = self.index.handle_request(qs, environ)
				except:
					start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
					s = io.StringIO()
					traceback.print_last(file=s)
					return s.getvalue()
				else:
					start_response(str(res["status"]) + ' ' + self.responses[res["status"]], list(res["headers"].items()))
					return res["content"]
		else:
			start_response('400 Bad Request', [('Content-Type', 'text/html')])
			return '<h1>400 Bad Request</h1>'

if __name__ == "__main__":
	fcgi = WebMPD_FastCGI()
	WSGIServer(fcgi.handle_request).run()
