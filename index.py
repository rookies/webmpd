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
import sys
## IMPORT DELIVERED LIBRARIES:
import libs.config as config
#from libs.evoque.domain import Domain

## INIT TEMPLATE ENGINE:
#domain = Domain(config.path + "templates")
#domain.get_template("index_default.html")
print("""<html>
	<head>
		<title>WebMPD</title>
		<link href="res/jquery-ui/css/smoothness/jquery-ui-1.10.1.custom.css" rel="stylesheet">
		<script src="res/jquery-ui/js/jquery-1.9.1.js"></script>
		<script src="res/jquery-ui/js/jquery-ui-1.10.1.custom.js"></script>
		<script type="text/javascript" src="res/default.js"></script>
		<link rel="stylesheet" type="text/css" href="res/default.css" />
	</head>
	<body onload="DefaultJS.init();">
		<div id="leftrow">
			<div id="player_controls">
				<a href="#backward" onclick="return !DefaultJS.go_prev();"><img src="res/img/media-skip-backward.png" alt="Skip backward" height="32" width="32" /></a><a href="#stop" onclick="return !DefaultJS.stop();"><img src="res/img/media-playback-stop.png" alt="Stop" height="32" width="32" /></a><a href="#play" onclick="return !DefaultJS.play();" id="player_play"><img src="res/img/media-playback-start.png" alt="Play" height="32" width="32" /></a><a href="#pause" onclick="return !DefaultJS.pause();" id="player_pause" class="invisible"><img src="res/img/media-playback-pause.png" alt="Pause" height="32" width="32" /></a><a href="#forward" onclick="return !DefaultJS.go_next();"><img src="res/img/media-skip-forward.png" alt="Skip forward" height="32" width="32" /></a>
			</div>
			<input type="checkbox" id="player_repeat" onchange="DefaultJS.update_modifiers();" /> <label for="player_repeat">repeat</label><br />
			<input type="checkbox" id="player_random" onchange="DefaultJS.update_modifiers();" /> <label for="player_random">random</label><br />
			<input type="checkbox" id="player_single" onchange="DefaultJS.update_modifiers();" /> <label for="player_single">single</label><br />
			<input type="checkbox" id="player_consume" onchange="DefaultJS.update_modifiers();" /> <label for="player_consume">consume</label>
			<br />
			<div id="player_volume">
				<img src="res/img/audio-volume-high.png" title="Set volume to 100%" alt="Full volume" height="32" width="32" />
				<div id="player_volume_bar"></div>
				<img src="res/img/audio-volume-muted.png" title="Mute sound" alt="Muted" height="32" width="32" />
			</div>
			<div id="player_xfade">
				<img src="res/img/list-add-big.png" title="Set Crossfade to 30 sec" alt="Full XFade" height="32" width="32" />
				<div id="player_xfade_bar"></div>
				<img src="res/img/list-remove-big.png" title="Disable Crossfade" alt="No XFade" height="32" width="32" />
			</div>
		</div>
		<div id="rightrow">
			<div id="player_status">
				<p id="player_time" class="invisible"><span id="player_elapsed">0:00</span> / <span id="player_songduration">0:00</span></p>
				<span id="player_songinfo" class="invisible"></span>
				<br />
				<span id="player_album" class="invisible"></span>
				<br />
				<div id="player_progress"></div>
			</div>
			<div id="player_statusmessage" class="invisible"></div>
			<div id="player_list_tabs">
				<ul>
					<li><a href="#player_list_tabs-1">Playlist</a></li>
					<li><a href="#player_list_tabs-2">Database</a></li>
					<li><a href="#player_list_tabs-3">File System</a></li>
				</ul>
				<div id="player_list_tabs-1">
					<p id="player_playlist_empty" class="invisible">
						The playlist is empty.
					</p>
					<div id="player_playlist_notempty" class="invisible">
						<a href="#clear" onclick="return !DefaultJS.clear_playlist();"><img src="res/img/edit-clear.png" width="32" height="32" alt="Clear playlist" title="Clear playlist" /></a>
						<table id="player_playlist">
							<thead>
								<tr>
									<th class="invisible"></th>
									<th>Duration</th>
									<th>Artist</th>
									<th>Title</th>
									<th>Year</th>
									<th>Album</th>
									<th>Actions</th>
								</tr>
							</thead>
							<tbody>
								
							</tbody>
						</table>
					</div>
				</div>
				<div id="player_list_tabs-2">
					<table id="database_table">
						<thead>
							<th>Artists</th>
							<th id="database_table_albums_header">Albums</th>
							<th id="database_table_songs_header">Songs</th>
						</thead>
						<tbody>
							<tr>
								<td>
									<ul id="database_table_artists"></ul>
								</td>
								<td>
									<ul id="database_table_albums"></ul>
								</td>
								<td>
									<ul id="database_table_songs"></ul>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
				<div id="player_list_tabs-3">
					<ul id="filesystem_list"></ul>
				</div>
			</div>
		</div>
		<div id="clearrow"></div>
	</body>
</html>""")
