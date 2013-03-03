#!/usr/bin/python3
#  ajax.py
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
import json, os, urllib.parse, sys, time, traceback
## IMPORT DELIVERED LIBRARIES:
import libs.config as config
import libs.mpd as mpd
import libs.usermanager as usermanager

class WebMPD_Ajax(object):
	mpd = mpd.MPDClient()
	cookie_env = None

	def get_error(self, code, message):
		return json.dumps({
			"status": "error",
			"code": code,
			"message": message
		})
		sys.exit()
	def mpd_connect(self):
		self.mpd.timeout = config.timeout
		self.mpd.idletimeout = config.idletimeout
		self.mpd.connect(config.host, config.port)
		if config.password is not None:
			self.mpd.password(config.password)
	def mpd_disconnect(self):
		self.mpd.close()
	def check_permission(self, name):
		if usermanager.get_permission(self.cookie_env, name):
			return None
		return self.get_error(201, "Action not allowed! You need permission '%s'!" % name)
	def handle_request(self, qs, environ=None):
		## Get cookie_env:
		if environ is None:
			self.cookie_env = os.getenv("HTTP_COOKIE")
		else:
			if "HTTP_COOKIE" in environ:
				self.cookie_env = environ["HTTP_COOKIE"]
			else:
				self.cookie_env = ""
		
		res = self.check_permission("access")
		if res is not None:
			return res
		if not "action" in qs:
			return self.get_error(100, "No action specified!")
		else:
			action = qs["action"][0]
			if action == "permissions":
				return json.dumps(usermanager.get_permissions(self.cookie_env))
			elif action == "currentsong":
				res = res = self.check_permission("playback.view")
				if res is not None:
					return res
				return json.dumps(self.mpd.currentsong())
			elif action == "status":
				res = self.check_permission("playback.view")
				if res is not None:
					return res
				return json.dumps(self.mpd.status())
			elif action == "stats":
				res = self.check_permission("stats")
				if res is not None:
					return res
				res = self.mpd.stats()
				res["db_update"] = time.mktime(time.localtime())-int(res["db_update"])
				return json.dumps(res)
			elif action == "pause":
				res = self.check_permission("playback.control")
				if res is not None:
					return res
				return json.dumps(self.mpd.pause())
			elif action == "play":
				res = self.check_permission("playback.control")
				if res is not None:
					return res
				return json.dumps(self.mpd.play())
			elif action == "stop":
				res = self.check_permission("playback.control")
				if res is not None:
					return res
				return json.dumps(self.mpd.stop())
			elif action == "setvol":
				res = self.check_permission("playback.change_options")
				if res is not None:
					return res
				try:
					value = int(qs["value"][0])
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.setvol(value))
			elif action == "setxfade":
				res = self.check_permission("playback.change_options")
				if res is not None:
					return res
				try:
					value = int(qs["value"][0])
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.crossfade(value))
			elif action == "seek":
				res = self.check_permission("playback.control")
				if res is not None:
					return res
				try:
					value = int(qs["value"][0])
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.seek(0, value))
			elif action == "prev":
				res = self.check_permission("playback.control")
				if res is not None:
					return res
				return json.dumps(self.mpd.previous())
			elif action == "next":
				res = self.check_permission("playback.control")
				if res is not None:
					return res
				return json.dumps(self.mpd.next())
			elif action == "update_modifiers":
				res = self.check_permission("playback.change_options")
				if res is not None:
					return res
				self.mpd.command_list_ok_begin()
				# repeat:
				try:
					if int(qs["repeat"][0]) == 1:
						self.mpd.repeat(1)
					else:
						self.mpd.repeat(0)
				except:
					pass
				# random:
				try:
					if int(qs["random"][0]) == 1:
						self.mpd.random(1)
					else:
						self.mpd.random(0)
				except:
					pass
				# single:
				try:
					if int(qs["single"][0]) == 1:
						self.mpd.single(1)
					else:
						self.mpd.single(0)
				except:
					pass
				# consume:
				try:
					if int(qs["consume"][0]) == 1:
						self.mpd.consume(1)
					else:
						self.mpd.consume(0)
				except:
					pass
				# send commands & disconnect:
				return json.dumps(self.mpd.command_list_end())
			elif action == "playlist":
				res = self.check_permission("playback.view")
				if res is not None:
					return res
				return json.dumps(self.mpd.playlistinfo())
			elif action == "moveid":
				res = self.check_permission("playlist.change")
				if res is not None:
					return res
				try:
					fr = int(qs["from"][0])
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					try:
						to = int(qs["to"][0])
					except:
						return self.get_error(102, "Invalid argument!")
					else:
						return json.dumps(self.mpd.moveid(fr, to))
			elif action == "deleteid":
				res = self.check_permission("playlist.change")
				if res is not None:
					return res
				try:
					id_ = int(qs["id"][0])
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.deleteid(id_))
			elif action == "artists":
				res = self.check_permission("database.view")
				if res is not None:
					return res
				return json.dumps(self.mpd.list("artist"))
			elif action == "albums":
				res = self.check_permission("database.view")
				if res is not None:
					return res
				if "all" in qs:
					return json.dumps(self.mpd.list("album"))
				else:
					try:
						artist = qs["artist"][0]
					except:
						return self.get_error(102, "Invalid argument!")
					else:
						return json.dumps(self.mpd.list("album", artist))
			elif action == "songs":
				res = self.check_permission("database.view")
				if res is not None:
					return res
				if "all" in qs:
					res = self.mpd.listallinfo()
					res2 = []
					for item in res:
						if "file" in item:
							res2.append(item)
					return json.dumps(res2)
				elif "all_artist" in qs:
					try:
						artist = qs["artist"][0]
					except:
						return self.get_error(102, "Invalid argument!")
					else:
						return json.dumps(self.mpd.find("artist", artist))
				else:
					try:
						artist = qs["artist"][0]
					except:
						return self.get_error(102, "Invalid argument!")
					else:
						try:
							album = qs["album"][0]
						except:
							return self.get_error(102, "Invalid argument!")
						else:
							if artist == "":
								return json.dumps(self.mpd.find("album", album))
							else:
								return json.dumps(self.mpd.find("artist", artist, "album", album))
			elif action == "add":
				res = self.check_permission("playlist.add.file")
				if res is not None:
					return res
				try:
					f = qs["file"][0]
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					res = self.mpd.findadd("file", f)
					if (res == None):
						return json.dumps(self.mpd.lsinfo(f)[0])
					else:
						return json.dumps(res)
			elif action == "addartist":
				res = self.check_permission("playlist.add.artist")
				if res is not None:
					return res
				try:
					artist = qs["artist"][0]
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.findadd("artist", artist))
			elif action == "addalbum":
				res = self.check_permission("playlist.add.album")
				if res is not None:
					return res
				try:
					album = qs["album"][0]
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					try:
						artist = qs["artist"][0]
					except:
						## no artist given
						return json.dumps(self.mpd.findadd("album", album))
					else:
						## artist given
						return json.dumps(self.mpd.findadd("artist", artist, "album", album))
			elif action == "playid":
				res = self.check_permission("playback.control")
				if res is not None:
					return res
				try:
					id_ = int(qs["id"][0])
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.playid(id_))
			elif action == "clear":
				res = self.check_permission("playlist.clear")
				if res is not None:
					return res
				return json.dumps(self.mpd.clear())
			elif action == "ls":
				res = self.check_permission("filesystem.view")
				if res is not None:
					return res
				try:
					path = qs["path"][0]
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					try:
						res = self.mpd.lsinfo(path)
					except mpd.CommandError:
						return json.dumps([])
					else:
						res2 = []
						for item in res:
							if "directory" in item or "file" in item:
								res2.append(item)
						return json.dumps(res2)
			elif action == "search":
				res = self.check_permission("search")
				if res is not None:
					return res
				arg_keys = [ "any", "artist", "title", "album", "file", "composer", "performer", "genre", "date", "comment"]
				args = []
				for key in arg_keys:
					try:
						arg = qs[key][0]
						assert(arg != "")
					except:
						pass
					else:
						args.extend([key, arg])
				if len(args) is 0:
					return json.dumps([])
				else:
					return json.dumps(self.mpd.search(*args))
			elif action == "listplaylists":
				res = self.check_permission("stored_playlists.view")
				if res is not None:
					return res
				return json.dumps(self.mpd.listplaylists())
			elif action == "listplaylistinfo":
				res = self.check_permission("stored_playlists.view")
				if res is not None:
					return res
				try:
					name = qs["name"][0]
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.listplaylistinfo(name))
			elif action == "load":
				res = self.check_permission("stored_playlists.load")
				if res is not None:
					return res
				try:
					name = qs["name"][0]
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.load(name))
			elif action == "rm":
				res = self.check_permission("stored_playlists.remove")
				if res is not None:
					return res
				try:
					name = qs["name"][0]
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.rm(name))
			elif action == "save":
				res = self.check_permission("playlist.save")
				if res is not None:
					return res
				try:
					name = qs["name"][0]
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.save(name))
			elif action == "outputs":
				res = self.check_permission("outputs.view")
				if res is not None:
					return res
				return json.dumps(self.mpd.outputs())
			elif action == "disableoutput":
				res = self.check_permission("outputs.disable")
				if res is not None:
					return res
				try:
					id_ = int(qs["id"][0])
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.disableoutput(id_))
			elif action == "enableoutput":
				res = self.check_permission("outputs.enable")
				if res is not None:
					return res
				try:
					id_ = int(qs["id"][0])
				except:
					return self.get_error(102, "Invalid argument!")
				else:
					return json.dumps(self.mpd.enableoutput(id_))
			elif action == "shuffle":
				res = self.check_permission("playlist.shuffle")
				if res is not None:
					return res
				return json.dumps(self.mpd.shuffle())
			else:
				return self.get_error(101, "Invalid action specified!")

if __name__ == "__main__":
	## HANDLE THE CGI REQUEST:
	try:
		qs = urllib.parse.parse_qs(os.getenv("QUERY_STRING"), keep_blank_values=True)
		ajax = WebMPD_Ajax()
		ajax.mpd_connect()
		res = ajax.handle_request(qs)
		ajax.mpd_disconnect()
	except:
		print("Status: 500")
		print("Content-Type: text/plain")
		print("")
		traceback.print_exc()
	else:
		print("Status: 200")
		print("Content-Type: text/html")
		print("")
		print(res)
