#!/usr/bin/python3
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
import json, os, urllib.parse
## IMPORT DELIVERED LIBRARIES:
import libs.config as config
import libs.mpd as mpd

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
## PARSE QUERY STRING:
qs = urllib.parse.parse_qs(os.getenv("QUERY_STRING"), keep_blank_values=True)
## CHECK ACTION ARGUMENT:
if not "action" in qs:
	send_error(100, "No action specified!")
else:
	action = qs["action"][0]
	if action == "currentsong":
		mpd_connect()
		print(json.dumps(MPD_CLIENT.currentsong()))
		mpd_disconnect()
	elif action == "status":
		mpd_connect()
		print(json.dumps(MPD_CLIENT.status()))
		mpd_disconnect()
	elif action == "stats":
		mpd_connect()
		print(json.dumps(MPD_CLIENT.stats()))
		mpd_disconnect()
	elif action == "pause":
		mpd_connect()
		print(json.dumps(MPD_CLIENT.pause()))
		mpd_disconnect()
	elif action == "play":
		mpd_connect()
		print(json.dumps(MPD_CLIENT.play()))
		mpd_disconnect()
	elif action == "stop":
		mpd_connect()
		print(json.dumps(MPD_CLIENT.stop()))
		mpd_disconnect()
	elif action == "setvol":
		try:
			value = int(qs["value"][0])
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.setvol(value)))
			mpd_disconnect()
	elif action == "seek":
		try:
			value = int(qs["value"][0])
		except:
			send_error(102, "Invalid argument!")
		else:
			mpd_connect()
			print(json.dumps(MPD_CLIENT.seek(0, value)))
			mpd_disconnect()
	elif action == "prev":
		mpd_connect()
		print(json.dumps(MPD_CLIENT.previous()))
		mpd_disconnect()
	elif action == "next":
		mpd_connect()
		print(json.dumps(MPD_CLIENT.next()))
		mpd_disconnect()
	elif action == "update_modifiers":
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
		mpd_connect()
		print(json.dumps(MPD_CLIENT.playlistinfo()))
		mpd_disconnect()
	elif action == "moveid":
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
	else:
		send_error(101, "Invalid action specified!")
