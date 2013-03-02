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
## IMPORT STANDARD LIBRARIES:
import sys, hashlib, random, time, os
sys.path.append("..")
## IMPORT DELIVERED LIBRARIES:
import libs.handler as handler
import libs.config as config
## IMPORT PYODBC:
import pyodbc

DB_CONN = None
SID_CHARS = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]

def gen_sid ():
	global SID_CHARS
	sid = ""
	for i in range(32):
		sid += random.choice(SID_CHARS)
	return sid

def get_cookies ():
	ret = {}
	raw = os.getenv("HTTP_COOKIE")
	if raw is not None:
		if raw.find(";") == -1:
			if raw.find("=") == -1:
				pass
			else:
				raw = raw.split("=")
				ret[raw[0].strip()] = raw[1].strip()
		else:
			raw = raw.split(";")
			for c in raw:
				if c.find("=") != -1:
					c = c.split("=")
					ret[c[0].strip()] = c[1].strip()
	return ret

def database_connect ():
	global DB_CONN
	if DB_CONN:
		return False
	DB_CONN = pyodbc.connect(config.database)
	return True

def login (username, password):
	global DB_CONN
	## Connect to database:
	database_connect()
	cursor = DB_CONN.cursor()
	row = cursor.execute("""
		SELECT
			`id`,
			`password`,
			`salt`,
			`group`
		FROM
			`users`
		WHERE
			`username` = ? AND
			`active` = 1
		LIMIT
			1
	""", (username, )).fetchone()
	if row is not None:
		## The username exists.
		## Create the password hash:
		hash_entered = hashlib.sha1()
		hash_entered.update(password.encode("utf8"))
		hash_entered.update(config.salt.encode("utf8"))
		hash_entered.update(row[2].encode("utf8"))
		hash_entered = hash_entered.hexdigest()
		## Compare the created hash with the hash in the database:
		if hash_entered == row[1]:
			## The password is correct.
			## Create the session id:
			sid = gen_sid()
			## ... write it into the database:
			cursor.execute("""
				INSERT INTO
					`sessions`
				SET
					`sid` = ?,
					`uid` = ?,
					`created` = ?,
					`lastactive` = ?
			""", (sid, row[0], time.mktime(time.gmtime()), time.mktime(time.gmtime())))
			cursor.commit()
			## ... and set the cookie:
			handler.set_header("Set-Cookie", "webmpd_sid=%s" % (sid))
			## Finally, return success:
			return True
	## Login failed:
	return False

def get_permission (name):
	permissions = get_permissions()
	if name.find(".") == -1:
		if permissions[name]:
			return True
	else:
		n = name.split(".")
		perm = permissions
		for i in n:
			perm = perm[i]
		if perm:
			return True
	return False

def get_permissions ():
	## Set default permissions:
	permissions = config.default_permissions
	## Get session cookie:
	cookies = get_cookies()
	if not "webmpd_sid" in cookies:
		return permissions
	## Get permissions from database:
	database_connect()
	cursor = DB_CONN.cursor()
	rows = cursor.execute("""
		SELECT
			`permissions`.`permission`,
			`permissions`.`value`
		FROM
			`permissions`,
			`users`,
			`sessions`
		WHERE
			`sessions`.`sid` = ? AND
			`users`.`id` = `sessions`.`uid` AND
			`permissions`.`group` = `users`.`group`
	""", (cookies["webmpd_sid"], )).fetchmany()
	## Run through database permissions:
	for perm in rows:
		key = perm[0]
		val = perm[1]
		if key.find(".") == -1:
			if key == "*":
				permissions = set_permissions_recursively(permissions, (val==1))
			else:
				permissions[key] = (val==1)
		else:
			key = key.split(".")
			if len(key) == 2:
				if key[1] == "*":
					permissions[key[0]] = set_permissions_recursively(permissions[key[0]], (val==1))
				else:
					permissions[key[0]][key[1]] = (val==1)
			elif len(key) == 3:
				if key[2] == "*":
					permissions[key[0]][key[1]] = set_permissions_recursively(permissions[key[0]][key[1]], (val==1))
				else:
					permissions[key[0]][key[1]][key[2]] = (val==1)
	return permissions

def set_permissions_recursively (permissions, value):
	ret = permissions
	for key, val in permissions.items():
		if isinstance(val, dict):
			ret[key] = set_permissions_recursively(permissions[key], value)
		else:
			ret[key] = value
	return ret
			
def is_loggedin ():
	cookies = get_cookies()
	if not "webmpd_sid" in cookies:
		return False
	database_connect()
	cursor = DB_CONN.cursor()
	row = cursor.execute("""
		SELECT
			`id`
		FROM
			`sessions`
		WHERE
			`sid` = ?
		LIMIT
			1
	""", (cookies["webmpd_sid"], )).fetchone()
	if int(row[0]) > 0:
		return True
	else:
		return False

def get_username ():
	cookies = get_cookies()
	if not "webmpd_sid" in cookies:
		return None
	database_connect()
	cursor = DB_CONN.cursor()
	row = cursor.execute("""
		SELECT
			`sessions`.`uid`,
			`users`.`username`
		FROM
			`sessions`,
			`users`
		WHERE
			`sessions`.`sid` = ? AND
			`users`.`id` = `sessions`.`uid`
		LIMIT
			1
	""", (cookies["webmpd_sid"], )).fetchone()
	return row[1]

def logout ():
	cookies = get_cookies()
	if not "webmpd_sid" in cookies:
		return False
	database_connect()
	cursor = DB_CONN.cursor()
	## Delete from database:
	row = cursor.execute("""
		DELETE FROM
			`sessions`
		WHERE
			`sid` = ?
		LIMIT
			1
	""", (cookies["webmpd_sid"], ))
	cursor.commit()
	## And delete the cookie:
	handler.set_header("Set-Cookie", "webmpd_sid=; Expires=Thu, 01-Jan-1970 00:00:01 GMT")
	return True
