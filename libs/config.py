#  config.py
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

################################################################################
#### This is the main configuration file of WebMPD. ############################
#### Please change all the configuration variables to fit your environment. ####
#### If you delete some of the variables, WebMPD won't work anymore. ###########
################################################################################


## Type: string
## Description: The absolute path to the main directory of WebMPD.
## IMPORTANT: You have to add a trailing slash and it has to be absolute, not relative.
## Example: /srv/http/webmpd/
## WRONG Example: /srv/http/webmpd
## WRONG Example: ./webmpd/
path = "/srv/http/webmpd/"

## Type: string
## Description: The address of the MPD server, without port or protocol.
## Example: localhost
## Example: mpd.example.org
## Example: 127.0.0.1
## WRONG Example: localhost:6600
host = "localhost"

## Type: integer
## Description: The port of the MPD server.
## MPD's default: 6600
port = 6600

## Type: string or None
## Description: The password for the MPD server. If None, WebMPD won't login on the server.
## MPD's default: None
## Example: "password123"
password = None

## Type: integer or None
## Description: The timeout for the connection with the MPD server. If None, no timeout.
timeout = 10

## Type: integer or None
## Description: The timeout for idle commands to the MPD server.
##   If you set it too low, the clients do too many requests to the server.
##   If you set it too high, the processes are locked too long and are not available for
##   other requests.
idletimeout = 5

## Type: string
## Description: The universal salt for the user password hashes.
##   Choose a random string with 10 characters.
##   If you change this, all existing passwords in the user database become invalid.
salt = "-1Znnq1%z,"

## Type: string
## Description: The ODBC connection string.
##   This string gets directly to the connect method of pyodbc.
database = "driver=mysql1;server=localhost;database=webmpd;uid=root;pwd=password"

## Type: dict
## Description: The permissions for a guest user.
default_permissions = {
	# If this is set to False, guest users will get redirected to the login form:
	"access": True,
	"playback": {
		# This permission is necessary to view the current song, the playlist
		# and general playback options. Normally, it's not useful to set this
		# to False. Use access instead to force the guests to login:
		"view": True,
		# This permission is necessary for stopping, starting or pausing playback,
		# seeking, playing a specific song and for going to the next or previous song:
		"control": False,
		# This permission is necessary for changing volume and xfade or setting
		# playback modifiers (repeat, random, single and consume):
		"change_options": False
	},
	"playlist": {
		# This permission is necessary for deleting songs from the playlist or
		# resorting it:
		"change": False,
		# This permission is necessary to clear the playlist:
		"clear": False,
		"add": {
			# This permission is necessary to add a single file to the playlist:
			"file": False,
			# This permission is necessary to add all songs of an artist to the playlist:
			"artist": False,
			# This permission is necessary to add all songs of an album to the playlist:
			"album": False
		},
		# This permission is necessary to save the current playlist as a stored playlist:
		"save": False,
		# This permission is necessary to shuffle the current playlist:
		"shuffle": False
	},
	"database": {
		# This permission is necessary to browse through the database:
		"view": True
	},
	"filesystem": {
		# This permission is necessary to browse through the server filesystem:
		"view": True
	},
	# This permission is necessary to search:
	"search": True,
	"stored_playlists": {
		# This permission is necessary to view the stored playlists:
		"view": True,
		# This permission is necessary to load a stored playlist into the
		# current playlist:
		"load": False,
		# This permission is necessary to remove a stored playlist,
		# use carefully if you have important playlists on the server:
		"remove": False
	},
	"outputs": {
		# This permission is necessary to view the audio outputs:
		"view": True,
		# This permission is necessary to disable audio outputs:
		"disable": False,
		# This permission is necessary to enable audio outputs:
		"enable": False
	},
	# This permission is necessary to view the statistics:
	"stats": True
}

## Type: int or None
## Description: The timeout for sessions since their creation. (in seconds)
session_created_timeout = 3600

## Type: int or None
## Description: The timeout for sessions since the last user action. (in seconds)
session_lastactive_timeout = None
