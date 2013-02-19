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
			<div id="player_volume">
				<img src="res/img/audio-volume-high.png" alt="Full volume" height="32" width="32" />
				<div id="player_volume_bar"></div>
				<img src="res/img/audio-volume-muted.png" alt="Muted" height="32" width="32" />
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
			<div id="player_list_tabs">
				<ul>
					<li><a href="#player_list_tabs-1">Playlist</a></li>
					<li><a href="#player_list_tabs-2">Artists</a></li>
					<li><a href="#player_list_tabs-3">Albums</a></li>
					<li><a href="#player_list_tabs-4">Songs</a></li>
					<li><a href="#player_list_tabs-5">File System</a></li>
				</ul>
				<div id="player_list_tabs-1">
					<table border="1" id="player_playlist">
						<thead>
							<tr>
								<th>Duration</th>
								<th>Artist</th>
								<th>Title</th>
								<th>Year</th>
								<th>Album</th>
							</tr>
						</thead>
						<tbody>
							
						</tbody>
					</table>
				</div>
				<div id="player_list_tabs-2"></div>
				<div id="player_list_tabs-3"></div>
				<div id="player_list_tabs-4"></div>
				<div id="player_list_tabs-5"></div>
			</div>
			XFade: <span id="mpd_xfade"></span>
		</div>
		<div id="clearrow"></div>
	</body>
</html>""")
