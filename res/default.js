var DefaultJS = {
	status_data: null,
	get_status_timeout: null,
	volume_bar_locked: false,
	progress_bar_locked: false,
	playlist: [],
	init: function ()
	{
		this.get_status();
		this.get_artists();
		this.get_status_timeout = window.setTimeout(this.get_status, 1000);
		$("#player_progress").slider({
			value: 0,
			min: 0,
			max: 0,
			start: function (event, ui) {
				DefaultJS.progress_bar_locked = true;
			},
			stop: function (event, ui) {
				DefaultJS.progress_bar_locked = false;
				DefaultJS.seek(ui.value);
			}
		});
		$("#player_volume_bar").slider({
			orientation: "vertical",
			value: 100,
			min: 0,
			max: 100,
			start: function (event, ui) {
				DefaultJS.volume_bar_locked = true;
			},
			stop: function (event, ui) {
				DefaultJS.volume_bar_locked = false;
				DefaultJS.set_volume(ui.value);
			}
		});
		$("#player_list_tabs").tabs();
		$("#player_playlist tbody").sortable({
			stop: function (event, ui) {
				/*
				 * Get the new order and send it to the server!
				*/
				$("#player_playlist tbody tr").each(function (pos) {
					id = parseInt($("td:first", this).html());
					if (DefaultJS.playlist[pos] != id)
						DefaultJS.move_playlistitem(id, pos);
				});
			}
		});
	},
	get_status: function ()
	{
		$.getJSON('ajax.py?action=status', function (data) {
			$("#mpd_xfade").html(data.xfade);
			/*
			 * Set volume slider:
			*/
			if (!DefaultJS.volume_bar_locked)
				$("#player_volume_bar").slider("value", parseInt(data.volume));
			/*
			 * Repeat mode:
			*/
			if (data.repeat == '1')
				document.getElementById("player_repeat").checked = true;
			else
				document.getElementById("player_repeat").checked = false;
			/*
			 * Random mode:
			*/
			if (data.random == '1')
				document.getElementById("player_random").checked = true;
			else
				document.getElementById("player_random").checked = false;
			/*
			 * Single mode:
			*/
			if (data.single == '1')
				document.getElementById("player_single").checked = true;
			else
				document.getElementById("player_single").checked = false;
			/*
			 * Consume mode:
			*/
			if (data.consume == '1')
				document.getElementById("player_consume").checked = true;
			else
				document.getElementById("player_consume").checked = false;
			/*
			 * Play / pause icon:
			*/
			if (data.state == "play")
			{
				$("#player_play").addClass("invisible");
				$("#player_pause").removeClass("invisible");
			}
			else
			{
				$("#player_pause").addClass("invisible");
				$("#player_play").removeClass("invisible");
			};
			/*
			 * Player time:
			*/
			if (data.state == "stop")
			{
				$("#player_time").addClass("invisible");
				$("#player_progress").slider("value", 0);
				$("#player_progress").slider("option", "max", 0);
			}
			else
			{
				/*
				 * Elapsed time:
				*/
				t = parseInt(data.time.split(':')[0]);
				min = Math.floor(t/60.);
				sec = t-min*60;
				if (sec < 10)
					sec = '0' + sec;
				$("#player_elapsed").html(min + ':' + sec);
				if (!DefaultJS.progress_bar_locked)
					$("#player_progress").slider("value", t);
				/*
				 * Song duration:
				*/
				t = parseInt(data.time.split(':')[1]);
				min = Math.floor(t/60.);
				sec = t-min*60;
				if (sec < 10)
					sec = '0' + sec;
				$("#player_songduration").html(min + ':' + sec);
				if (!DefaultJS.progress_bar_locked)
					$("#player_progress").slider("option", "max", t);
				/*
				 * Set visible:
				*/
				$("#player_time").removeClass("invisible");
			};
			/*
			 * Check what we have to update:
			*/
			if (DefaultJS.status_data == null || DefaultJS.status_data.songid != data.songid ||DefaultJS.status_data.state != data.state)
				update_songinfo = true;
			else
				update_songinfo = false;
			if (DefaultJS.status_data == null || DefaultJS.status_data.playlist != data.playlist)
				update_playlist = true;
			else
				update_playlist = false;
			/*
			 * Save status data:
			*/
			DefaultJS.status_data = data;
			/*
			 * Update song info and playlist if needed:
			*/
			if (update_songinfo)
				DefaultJS.get_currentsong();
			if (update_songinfo || update_playlist)
				DefaultJS.get_playlist();
			/*
			 * Set new timeout:
			*/
			window.clearTimeout(DefaultJS.get_status_timeout);
			DefaultJS.get_status_timeout = window.setTimeout(DefaultJS.get_status, 1000);
		});
	},
	get_currentsong: function ()
	{
		$.getJSON('ajax.py?action=currentsong', function (data) {
			/*
			 * Set window title:
			*/
			if (data.artist != null && data.title != null && data.album != null)
				status = data.artist + " - " + data.title + " (" + data.album + ")";
			else if (data.artist != null && data.title != null)
				status = data.artist + " - " + data.title;
			else if (data.artist != null && data.file != null)
				status = data.artist + " - " + data.file;
			else if (data.file != null)
				status = data.file;
			else
				status = '';
			if (DefaultJS.status_data.state == "stop")
				window.document.title = 'WebMPD';
			else
				window.document.title = 'WebMPD: ' + status;
			/*
			 * Set song info:
			*/
			if (DefaultJS.status_data.state == "stop")
				$("#player_songinfo").addClass("invisible");
			else
			{
				if (data.artist != null && data.title != null)
					status = data.artist + " - " + data.title;
				else if (data.artist != null && data.file != null)
					status = data.artist + " - " + data.file;
				else
					status = data.file;
				$("#player_songinfo").html(status);
				/*
				 * Set visible:
				*/
				$("#player_songinfo").removeClass("invisible");
			};
			/*
			 * Set album:
			*/
			if (DefaultJS.status_data.state == "stop" || data.album == null)
				$("#player_album").addClass("invisible");
			else
			{
				$("#player_album").html(data.album);
				/*
				 * Set visible:
				*/
				$("#player_album").removeClass("invisible");
			};
		});
	},
	pause: function ()
	{
		$.get('ajax.py?action=pause', function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	play: function ()
	{
		$.get('ajax.py?action=play', function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	stop: function ()
	{
		$.get('ajax.py?action=stop', function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	set_volume: function (value)
	{
		$.get('ajax.py?action=setvol&value=' + value, function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	seek: function (value)
	{
		$.get('ajax.py?action=seek&value=' + value, function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	go_prev: function ()
	{
		$.get('ajax.py?action=prev', function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	go_next: function ()
	{
		$.get('ajax.py?action=next', function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	update_modifiers: function ()
	{
		// repeat:
		if (document.getElementById('player_repeat').checked)
			repeat = 1;
		else
			repeat = 0;
		// random:
		if (document.getElementById('player_random').checked)
			random = 1;
		else
			random = 0;
		// single:
		if (document.getElementById('player_single').checked)
			single = 1;
		else
			single = 0;
		// consume:
		if (document.getElementById('player_consume').checked)
			consume = 1;
		else
			consume = 0;
		$.get('ajax.py?action=update_modifiers&repeat=' + repeat + '&random=' + random + '&single=' + single + '&consume=' + consume, function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	get_playlist: function ()
	{
		$.getJSON('ajax.py?action=playlist', function (data) {
			var i;
			$("#player_playlist tbody tr").remove();
			DefaultJS.playlist = [];
			for (i=0; i < data.length; i++)
			{
				t = parseInt(data[i].time);
				min = Math.floor(t/60.);
				sec = t-min*60;
				if (sec < 10)
					sec = '0' + sec;
				if (data[i].artist == null)
					data[i].artist = '';
				if (data[i].title == null)
					data[i].title = data[i].file;
				if (data[i].date == null)
					data[i].date = '';
				if (data[i].album == null)
					data[i].album = '';
				if (DefaultJS.status_data.songid == data[i].id && DefaultJS.status_data.state != "stop")
					classes = ' class="playing"';
				else
					classes = '';
				$("#player_playlist tbody").append('<tr' + classes + '><td class="invisible">' + data[i].id + '</td><td>' + min + ':' + sec + '</td><td>' + data[i].artist + '</td><td>' + data[i].title + '</td><td>' + data[i].date + '</td><td>' + data[i].album + '</td><td><a href="#remove" onclick="return !DefaultJS.remove_playlistitem(' + data[i].id + ');"><img src="res/img/list-remove.png" width="16" height="16" alt="Remove" /></a></td></tr>');
				DefaultJS.playlist.push(parseInt(data[i].id));
				// data[i]:
				// {
				//--  "file": "openmusic/The Sovereigns/Pick It Up!/01 - Pick It Up! (...And Run).mp3",
				//--  "time": "59",
				//--  "album": "Pick It Up!",
				//--  "id": "59",
				//--  "date": "2010",
				//--  "last-modified": "2010-01-20T15:32:17Z",
				//--  "title": "Pick It Up! (...And Run)",
				//  "track": "1/9",
				//--  "artist": "The Sovereigns",
				//  "pos": "0"
				// }
			}
		});
	},
	move_playlistitem: function (id, pos)
	{
		$.get('ajax.py?action=moveid&from=' + id + '&to=' + pos, function (data) {
			DefaultJS.get_status();
		});
	},
	remove_playlistitem: function (id)
	{
		$.get('ajax.py?action=deleteid&id=' + id, function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	get_artists: function ()
	{
		/*
		 * Clean up & set table headers:
		*/
		$("#database_table_artists li").remove();
		$("#database_table_albums li").remove();
		$("#database_table_albums_header").html("Albums");
		$("#database_table_songs li").remove();
		/*
		 * Receive artists:
		*/
		$.getJSON('ajax.py?action=artists', function (data) {
			var i;
			$("#database_table_songs_header").html("Songs");
			$("#database_table_artists").append('<li><a href="#albums" onclick="return !DefaultJS.get_albums(\'\', true);">ALL ARTISTS</a></li>');
			for (i=0; i < data.length; i++)
			{
				$("#database_table_artists").append('<li><a href="#albums" onclick="return !DefaultJS.get_albums(\'' + data[i] + '\');">' + data[i] + '</a></li>');
			}
		});
	},
	get_albums: function (artist, all=false)
	{
		/*
		 * Clean up & set table headers:
		*/
		if (all)
			$("#database_table_albums_header").html("All Albums");
		else
			$("#database_table_albums_header").html("Albums (" + artist + ")");
		$("#database_table_albums li").remove();
		$("#database_table_songs li").remove();
		$("#database_table_songs_header").html("Songs");
		/*
		 * Receive albums:
		*/
		$.getJSON('ajax.py?action=albums&artist=' + artist + ((all==true)?'&all':''), function (data) {
			var i;
			if (all == true)
				$("#database_table_albums").append('<li><a href="#songs" onclick="return !DefaultJS.get_songs(\'\', \'\', false, true);">ALL SONGS</a></li>');
			else
				$("#database_table_albums").append('<li><a href="#songs" onclick="return !DefaultJS.get_songs(\'' + artist + '\', \'\', true, false);">ALL SONGS</a></li>');
			for (i=0; i < data.length; i++)
			{
				if (data[i] == "")
				{
					if (all == true)
						$("#database_table_albums").append('<li><a href="#songs" onclick="return !DefaultJS.get_songs(\'\', \'\', false, false);">[Unknown album]</a></li>');
					else
						$("#database_table_albums").append('<li><a href="#songs" onclick="return !DefaultJS.get_songs(\'' + artist + '\', \'\', false, false);">[Unknown album]</a></li>');
					break;
				};
			}
			for (i=0; i < data.length; i++)
			{
				if (data[i] != "")
				{
					if (all == true)
						$("#database_table_albums").append('<li><a href="#songs" onclick="return !DefaultJS.get_songs(\'\', \'' + data[i] + '\', false, false);">' + data[i] + '</a></li>');
					else
						$("#database_table_albums").append('<li><a href="#songs" onclick="return !DefaultJS.get_songs(\'' + artist + '\', \'' + data[i] + '\', false, false);">' + data[i] + '</a></li>');
				};
			}
		});
		return true;
	},
	get_songs: function (artist, album, all_artist, all)
	{
		/*
		 * Clean up:
		*/
		$("#database_table_songs li").remove();
		/*
		 * Receive songs:
		*/
		$.getJSON('ajax.py?action=songs&artist=' + artist + '&album=' + album + ((all_artist==true)?'&all_artist':'') + ((all==true)?'&all':''), function (data) {
			var i;
			if (all)
				$("#database_table_songs_header").html("All Songs");
			else if (all_artist)
			{
				if (artist == "")
					$("#database_table_songs_header").html("Songs (Unknown Artist)");
				else
					$("#database_table_songs_header").html("Songs (" + artist + ")");
			}
			else
			{
				if (artist == "" && data[0].artist == null)
					artist = "Unknown artist";
				else if (data[0].artist != null)
					artist = data[0].artist;
				if (album == "")
					album = "Unknown album";
				$("#database_table_songs_header").html("Songs (" + artist + " - " + album +")");
			};
			for (i=0; i < data.length; i++)
			{
				$("#database_table_songs").append('<li>' + data[i].title + '</li>');
			}
		});
		return true;
	}
}
