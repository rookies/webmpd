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
## Description: The idle timeout for the connection with the MPD server.
##   Normally we don't need to set this, because we close the connection
##   a few moments after opening it.
idletimeout = None

## Type: string
## Description: The universal salt for the user password hashes.
##   Choose a random string with 10 characters.
##   If you change this, all existing passwords in the user database become invalid.
salt = "-1Znnq1%z,"

## Type: string
## Description: The ODBC connection string.
database = "driver=mysql1;server=localhost;database=webmpd;uid=root;pwd=password"

## Type: dict
## Description: The permissions for a guest user.
default_permissions = {
	"access": True,
	"playback": {
		"view": True,
		"control": False,
		"change_options": False
	},
	"playlist": {
		"change": False,
		"clear": False,
		"add": {
			"file": False,
			"artist": False,
			"album": False
		}
	},
	"database": {
		"view": True
	},
	"filesystem": {
		"view": True
	},
	"search": True,
	"stored_playlists": {
		"view": True,
		"load": False,
		"remove": False
	}
}
