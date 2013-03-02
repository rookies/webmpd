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
import json, os, urllib.parse, sys
## IMPORT DELIVERED LIBRARIES:
import libs.config as config
import libs.mpd as mpd
import libs.usermanager as usermanager

## GLOBAL VARIABLES:
MPD_CLIENT = mpd.MPDClient()
## DEFINE FUNCTIONS:
def send_error(code, message):
	print(json.dumps({
		"status": "error",
		"code": code,
		"message": message
	}))
	sys.exit()
def mpd_connect():
	MPD_CLIENT.timeout = config.timeout
	MPD_CLIENT.idletimeout = config.idletimeout
	MPD_CLIENT.connect(config.host, config.port)
	if config.password is not None:
		MPD_CLIENT.password(config.password)
def mpd_disconnect():
	MPD_CLIENT.close()
def check_permission(name):
	if usermanager.get_permission(name):
		return True
	send_error(201, "Action not allowed! You need permission '%s'!" % name)
	return False
## PARSE QUERY STRING:
qs = urllib.parse.parse_qs(os.getenv("QUERY_STRING"), keep_blank_values=True)
## CHECK ACCESS PERMISSION:
check_permission("access")
## CHECK ACTION ARGUMENT:
if not "action" in qs:
	send_error(100, "No action specified!")
else:
	action = qs["action"][0]
	if action == "permissions":
		print(json.dumps(usermanager.get_permissions()))
	elif action == "currentsong":
		check_permission("playback.view")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.currentsong()))
		mpd_disconnect()
	elif action == "status":
		check_permission("playback.view")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.status()))
		mpd_disconnect()
	elif action == "stats":
		check_permission("playback.view")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.stats()))
		mpd_disconnect()
	elif action == "pause":
		check_permission("playback.control")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.pause()))
		mpd_disconnect()
	elif action == "play":
		check_permission("playback.control")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.play()))
		mpd_disconnect()
	elif action == "stop":
		check_permission("playback.control")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.stop()))
		mpd_disconnect()
	elif action == "setvol":
		check_permission("playback.change_options")
		try:
			value = int(qs["value"][0])
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.setvol(value)))
			mpd_disconnect()
	elif action == "setxfade":
		check_permission("playback.change_options")
		try:
			value = int(qs["value"][0])
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.crossfade(value)))
			mpd_disconnect()
	elif action == "seek":
		check_permission("playback.control")
		try:
			value = int(qs["value"][0])
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.seek(0, value)))
			mpd_disconnect()
	elif action == "prev":
		check_permission("playback.control")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.previous()))
		mpd_disconnect()
	elif action == "next":
		check_permission("playback.control")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.next()))
		mpd_disconnect()
	elif action == "update_modifiers":
		check_permission("playback.change_options")
		mpd_connect()
		MPD_CLIENT.command_list_ok_begin()
		# repeat:
		try:
			if int(qs["repeat"][0]) == 1:
				MPD_CLIENT.repeat(1)
			else:
				MPD_CLIENT.repeat(0)
		except:
			pass
		# random:
		try:
			if int(qs["random"][0]) == 1:
				MPD_CLIENT.random(1)
			else:
				MPD_CLIENT.random(0)
		except:
			pass
		# single:
		try:
			if int(qs["single"][0]) == 1:
				MPD_CLIENT.single(1)
			else:
				MPD_CLIENT.single(0)
		except:
			pass
		# consume:
		try:
			if int(qs["consume"][0]) == 1:
				MPD_CLIENT.consume(1)
			else:
				MPD_CLIENT.consume(0)
		except:
			pass
		# send commands & disconnect:
		print(json.dumps(MPD_CLIENT.command_list_end()))
		mpd_disconnect()
	elif action == "playlist":
		check_permission("playback.view")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.playlistinfo()))
		mpd_disconnect()
	elif action == "moveid":
		check_permission("playlist.change")
		try:
			fr = int(qs["from"][0])
		except:
			send_error(102, "Invalid argument!")
		else:
			try:
				to = int(qs["to"][0])
			except:
				send_error(102, "Invalid argument!")
			else:
				mpd_connect()
				print(json.dumps(MPD_CLIENT.moveid(fr, to)))
				mpd_disconnect()
	elif action == "deleteid":
		check_permission("playlist.change")
		try:
			id_ = int(qs["id"][0])
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.deleteid(id_)))
			mpd_disconnect()
	elif action == "artists":
		check_permission("database.view")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.list("artist")))
		mpd_disconnect()
	elif action == "albums":
		check_permission("database.view")
		if "all" in qs:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.list("album")))
			mpd_disconnect()
		else:
			try:
				artist = qs["artist"][0]
			except:
				send_error(102, "Invalid argument!")
			else:
				mpd_connect()
				print(json.dumps(MPD_CLIENT.list("album", artist)))
				mpd_disconnect()
	elif action == "songs":
		check_permission("database.view")
		if "all" in qs:
			mpd_connect()
			res = MPD_CLIENT.listallinfo()
			res2 = []
			for item in res:
				if "file" in item:
					res2.append(item)
			print(json.dumps(res2))
			mpd_disconnect()
		elif "all_artist" in qs:
			try:
				artist = qs["artist"][0]
			except:
				send_error(102, "Invalid argument!")
			else:
				mpd_connect()
				print(json.dumps(MPD_CLIENT.find("artist", artist)))
				mpd_disconnect()
		else:
			try:
				artist = qs["artist"][0]
			except:
				send_error(102, "Invalid argument!")
			else:
				try:
					album = qs["album"][0]
				except:
					send_error(102, "Invalid argument!")
				else:
					mpd_connect()
					if artist == "":
						print(json.dumps(MPD_CLIENT.find("album", album)))
					else:
						print(json.dumps(MPD_CLIENT.find("artist", artist, "album", album)))
					mpd_disconnect()
	elif action == "add":
		check_permission("playlist.add.file")
		try:
			f = qs["file"][0]
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			res = MPD_CLIENT.findadd("file", f)
			if (res == None):
				print(json.dumps(MPD_CLIENT.lsinfo(f)[0]))
			else:
				print(json.dumps(res))
			mpd_disconnect()
	elif action == "addartist":
		check_permission("playlist.add.artist")
		try:
			artist = qs["artist"][0]
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.findadd("artist", artist)))
			mpd_disconnect()
	elif action == "addalbum":
		check_permission("playlist.add.album")
		try:
			album = qs["album"][0]
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			try:
				artist = qs["artist"][0]
			except:
				## no artist given
				print(json.dumps(MPD_CLIENT.findadd("album", album)))
			else:
				## artist given
				print(json.dumps(MPD_CLIENT.findadd("artist", artist, "album", album)))
			mpd_disconnect()
	elif action == "playid":
		check_permission("playback.control")
		try:
			id_ = int(qs["id"][0])
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.playid(id_)))
			mpd_disconnect()
	elif action == "clear":
		check_permission("playlist.clear")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.clear()))
		mpd_disconnect()
	elif action == "ls":
		check_permission("filesystem.view")
		try:
			path = qs["path"][0]
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			try:
				res = MPD_CLIENT.lsinfo(path)
			except mpd.CommandError:
				print(json.dumps([]))
			else:
				res2 = []
				for item in res:
					if "directory" in item or "file" in item:
						res2.append(item)
				print(json.dumps(res2))
			mpd_disconnect()
	elif action == "search":
		check_permission("search")
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
			print(json.dumps([]))
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.search(*args)))
			mpd_disconnect()
	elif action == "listplaylists":
		check_permission("stored_playlists.view")
		mpd_connect()
		print(json.dumps(MPD_CLIENT.listplaylists()))
		mpd_disconnect()
	elif action == "listplaylistinfo":
		check_permission("stored_playlists.view")
		try:
			name = qs["name"][0]
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.listplaylistinfo(name)))
			mpd_disconnect()
	elif action == "load":
		check_permission("stored_playlists.load")
		try:
			name = qs["name"][0]
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.load(name)))
			mpd_disconnect()
	elif action == "rm":
		check_permission("stored_playlists.remove")
		try:
			name = qs["name"][0]
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.rm(name)))
			mpd_disconnect()
	else:
		send_error(101, "Invalid action specified!")
