var DefaultJS = {
	status_data: null,
	get_status_timeout: null,
	volume_bar_locked: false,
	progress_bar_locked: false,
	init: function ()
	{
		this.get_status();
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
		/*$("#player_repeat").button();
		$("#player_random").button();
		$("#player_single").button();
		$("#player_consume").button();*/
	},
	get_status: function ()
	{
		$.getJSON('ajax.py?action=status', function (data) {
			$("#mpd_xfade").html(data.xfade);
			$("#mpd_playlistlength").html(data.playlistlength);
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
				$("#player_playlist tbody").append('<tr' + classes + '><td>' + min + ':' + sec + '</td><td>' + data[i].artist + '</td><td>' + data[i].title + '</td><td>' + data[i].date + '</td><td>' + data[i].album + '</td></tr>');
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
	}
}
