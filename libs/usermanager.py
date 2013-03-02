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

GUEST_PERMISSIONS = {
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

def login (username, password):
	return False

def get_permission (name):
	if name.find(".") == -1:
		if GUEST_PERMISSIONS[name]:
			return True
	else:
		n = name.split(".")
		perm = GUEST_PERMISSIONS
		for i in n:
			perm = perm[i]
		if perm:
			return True
	return False

def get_permissions ():
	return GUEST_PERMISSIONS
