/*
 * default.js
 * 
 * Copyright 2013 Robert Knauer <robert@privatdemail.net>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */

var DefaultJS = {
	status_data: null,
	progress_bar_locked: false,
	first_statuscheck: true,
	update_currentsong: false,
	playlist: [],
	permissions: null,
	volume: -1,
	xfade: -1,
	increase_time_interval: null,
	songduration: 0,
	songelapsed: 0,
	init: function ()
	{
		this.get_permissions();
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
			},
			disabled: true
		});
		$("#player_volume_bar").slider({
			orientation: "vertical",
			value: 0,
			min: 0,
			max: 100,
			stop: function (event, ui) {
				DefaultJS.set_volume(ui.value);
			},
			disabled: true
		});
		$("#player_xfade_bar").slider({
			orientation: "vertical",
			value: 0,
			min: 0,
			max: 30,
			stop: function (event, ui) {
				DefaultJS.set_xfade(ui.value);
			},
			disabled: true
		});
		$("#player_list_tabs").tabs({
			beforeActivate: function (event, ui) {
				switch (ui.newPanel.prop("id"))
				{
					case "player_list_tabs-1":
						// Playlist
						break;
					case "player_list_tabs-2":
						// Database
						DefaultJS.get_artists();
						break;
					case "player_list_tabs-3":
						// File System
						DefaultJS.list_filesystem();
						break;
					case "player_list_tabs-4":
						// Search
						break;
					case "player_list_tabs-5":
						// Stored Playlists
						DefaultJS.list_playlists();
						break;
					case "player_list_tabs-6":
						// Audio Outputs
						DefaultJS.list_outputs();
						break;
					case "player_list_tabs-7":
						// Statistics
						DefaultJS.get_stats();
						break;
				}
			},
			disabled: [ 1, 2, 3, 4, 5, 6 ]
		});
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
			},
			disabled: true
		});
		$("#playlist_saver_dialog").removeClass("invisible");
	},
	get_permissions: function ()
	{
		$.getJSON('ajax.py?action=permissions', function (data) {
			DefaultJS.permissions = data;
			/*
			 * playback.control
			*/
			if (data.playback.control)
			{
				$("#player_controls").removeClass("invisible");
				$("#player_progress").slider("enable");
				
			}
			else
			{
				$("#player_controls").addClass("invisible");
				$("#player_progress").slider("disable");
			};
			/*
			 * playback.change_options
			*/
			if (data.playback.change_options)
			{
				$("#player_volume_bar").slider("enable");
				$("#player_xfade_bar").slider("enable");
				$("#player_repeat").prop("disabled", false);
				$("#player_random").prop("disabled", false);
				$("#player_single").prop("disabled", false);
				$("#player_consume").prop("disabled", false);
			}
			else
			{
				$("#player_volume_bar").slider("disable");
				$("#player_xfade_bar").slider("disable");
				$("#player_repeat").prop("disabled", true);
				$("#player_random").prop("disabled", true);
				$("#player_single").prop("disabled", true);
				$("#player_consume").prop("disabled", true);
			};
			/*
			 * playlist.change
			*/
			if (data.playlist.change)
			{
				$("#player_playlist tbody").sortable("enable");
			}
			else
			{
				$("#player_playlist tbody").sortable("disable");
			};
			/*
			 * playlist.clear
			*/
			if (data.playlist.clear)
			{
				$("#playlist_clear_link").removeClass("invisible");
			}
			else
			{
				$("#playlist_clear_link").addClass("invisible");
			};
			/*
			 * playlist.save
			*/
			if (data.playlist.save)
			{
				$("#playlist_save_link").removeClass("invisible");
			}
			else
			{
				$("#playlist_save_link").addClass("invisible");
			};
			/*
			 * playlist.shuffle
			*/
			if (data.playlist.shuffle)
			{
				$("#playlist_shuffle_link").removeClass("invisible");
			}
			else
			{
				$("#playlist_shuffle_link").addClass("invisible");
			};
			/*
			 * database.view
			*/
			if (data.database.view)
			{
				$("#player_list_tabs").tabs("enable", 1);
			}
			else
			{
				$("#player_list_tabs").tabs("disable", 1);
			};
			/*
			 * database.update
			*/
			if (data.database.update)
			{
				$("#database_update").removeClass("invisible");
			}
			else
			{
				$("#database_update").addClass("invisible");
			};
			/*
			 * database.rescan
			*/
			if (data.database.rescan)
			{
				$("#database_rescan").removeClass("invisible");
			}
			else
			{
				$("#database_rescan").addClass("invisible");
			};
			/*
			 * filesystem.view
			*/
			if (data.filesystem.view)
			{
				$("#player_list_tabs").tabs("enable", 2);
			}
			else
			{
				$("#player_list_tabs").tabs("disable", 2);
			};
			/*
			 * search
			*/
			if (data.search)
			{
				$("#leftrow_box2").removeClass("invisible");
				$("#player_list_tabs").tabs("enable", 3);
			}
			else
			{
				$("#leftrow_box2").addClass("invisible");
				$("#player_list_tabs").tabs("disable", 3);
			};
			/*
			 * stored_playlists.view
			*/
			if (data.stored_playlists.view)
			{
				$("#player_list_tabs").tabs("enable", 4);
			}
			else
			{
				$("#player_list_tabs").tabs("disable", 4);
			};
			/*
			 * outputs.view
			*/
			if (data.outputs.view)
			{
				$("#player_list_tabs").tabs("enable", 5);
			}
			else
			{
				$("#player_list_tabs").tabs("disable", 5);
			};
			/*
			 * stats
			*/
			if (data.stats)
			{
				$("#player_list_tabs").tabs("enable", 6);
			}
			else
			{
				$("#player_list_tabs").tabs("disable", 6);
			};
			/*
			 * Start polling:
			*/
			DefaultJS.idle();
			DefaultJS.get_status();
		});
	},
	idle: function ()
	{
		$.getJSON('ajax.py?action=idle', function (data) {
			var i;
			for (i=0; i < data.length; i++)
			{
				switch (data[i])
				{
					case "player":
						DefaultJS.update_currentsong = true;
						DefaultJS.get_status();
						DefaultJS.get_playlist();
						break;
					case "playlist":
						DefaultJS.get_playlist();
						break;
					case "mixer":
						DefaultJS.get_status();
						break;
					case "options":
						DefaultJS.get_status();
						break;
					default:
						alert('Idle event: ' + data[i]);
				}
			}
			DefaultJS.idle();
		});
	},
	increase_time: function ()
	{
		DefaultJS.songelapsed++;
		t = DefaultJS.songelapsed;
		min = Math.floor(t/60.);
		sec = t-min*60;
		if (sec < 10)
			sec = '0' + sec;
		$("#player_elapsed").html(min + ':' + sec);
		if (!DefaultJS.progress_bar_locked)
			$("#player_progress").slider("value", t);
	},
	get_status: function ()
	{
		$.getJSON('ajax.py?action=status', function (data) {
			/*
			 * Set volume:
			*/
			$("#player_volume_bar").slider("value", parseInt(data.volume));
			if (DefaultJS.volume == -1)
			{
				DefaultJS.volume = data.volume;
			}
			else
			{
				if (DefaultJS.volume != data.volume)
				{
					DefaultJS.show_status('Volume set to ' + data.volume + '%.');
					DefaultJS.volume = data.volume;
				};
			};
			/*
			 * Set xfade:
			*/
			$("#player_xfade_bar").slider("value", parseInt(data.xfade));
			if (DefaultJS.xfade == -1)
			{
				DefaultJS.xfade = data.xfade;
			}
			else
			{
				if (DefaultJS.xfade != data.xfade)
				{
					DefaultJS.show_status('Crossfade set to ' + data.xfade + ' sec.');
					DefaultJS.xfade = data.xfade;
				};
			};
			/*
			 * Set error message:
			*/
			if (data.error != null)
			{
				$("#player_error").html("Error: " + data.error);
				$("#player_error").removeClass("invisible");
			}
			else
				$("#player_error").addClass("invisible");
			/*
			 * Repeat mode:
			*/
			if (data.repeat == '1' && document.getElementById("player_repeat").checked == false)
			{
				document.getElementById("player_repeat").checked = true;
				if (!DefaultJS.first_statuscheck)
					DefaultJS.show_status('Activated repeat mode by remote client.');
			}
			else if (data.repeat == '0' && document.getElementById("player_repeat").checked == true)
			{
				document.getElementById("player_repeat").checked = false;
				if (!DefaultJS.first_statuscheck)
					DefaultJS.show_status('Deactivated repeat mode by remote client.');
			};
			/*
			 * Random mode:
			*/
			if (data.random == '1' && document.getElementById("player_random").checked == false)
			{
				document.getElementById("player_random").checked = true;
				if (!DefaultJS.first_statuscheck)
					DefaultJS.show_status('Activated random mode by remote client.');
			}
			else if (data.random == '0' && document.getElementById("player_random").checked == true)
			{
				document.getElementById("player_random").checked = false;
				if (!DefaultJS.first_statuscheck)
					DefaultJS.show_status('Deactivated random mode by remote client.');
			};
			/*
			 * Single mode:
			*/
			if (data.single == '1' && document.getElementById("player_single").checked == false)
			{
				document.getElementById("player_single").checked = true;
				if (!DefaultJS.first_statuscheck)
					DefaultJS.show_status('Activated single mode by remote client.');
			}
			else if (data.single == '0' && document.getElementById("player_single").checked == true)
			{
				document.getElementById("player_single").checked = false;
				if (!DefaultJS.first_statuscheck)
					DefaultJS.show_status('Deactivated single mode by remote client.');
			};
			/*
			 * Consume mode:
			*/
			if (data.consume == '1' && document.getElementById("player_consume").checked == false)
			{
				document.getElementById("player_consume").checked = true;
				if (!DefaultJS.first_statuscheck)
					DefaultJS.show_status('Activated consume mode by remote client.');
			}
			else if (data.consume == '0' && document.getElementById("player_consume").checked == true)
			{
				document.getElementById("player_consume").checked = false;
				if (!DefaultJS.first_statuscheck)
					DefaultJS.show_status('Deactivated consume mode by remote client.');
			};
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
			window.clearInterval(DefaultJS.increase_time_interval);
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
				DefaultJS.songelapsed = t;
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
				DefaultJS.songduration = t;
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
			if (data.state == "play")
				DefaultJS.increase_time_interval = window.setInterval(DefaultJS.increase_time, 1000);
			/*
			 * Save status data:
			*/
			DefaultJS.status_data = data;
			/*
			 * Get currentsong & playlist:
			*/
			if (DefaultJS.first_statuscheck)
			{
				if (data.state != "stop")
					DefaultJS.get_currentsong();
				if (parseInt(data.playlistlength) > 0)
					DefaultJS.get_playlist();
				else
					$("#player_playlist_empty").removeClass("invisible");
			};
			if (DefaultJS.update_currentsong)
			{
				DefaultJS.update_currentsong = false;
				DefaultJS.get_currentsong();
			};
			/*
			 * Set first_statuscheck variable:
			*/
			DefaultJS.first_statuscheck = false;
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
				if (data.date == null)
					$("#player_album").html(data.album);
				else
					$("#player_album").html(data.album + ' (' + data.date + ')');
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
	set_xfade: function (value)
	{
		$.get('ajax.py?action=setxfade&value=' + value, function (data) {
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
			DefaultJS.show_status('Updated playback modifiers! Repeat=' + repeat + ' Random=' + random + ' Single=' + single + ' Consume=' + consume);
		});
		return true;
	},
	get_playlist: function ()
	{
		$.getJSON('ajax.py?action=playlist', function (data) {
			var i;
			$("#player_playlist tbody tr").remove();
			var playlist_len = data.length;
			var playlist_time = 0;
			DefaultJS.playlist = [];
			for (i=0; i < data.length; i++)
			{
				var t = parseInt(data[i].time);
				playlist_time += t;
				var min = Math.floor(t/60.);
				var sec = t-min*60;
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
				else if (i%2 == 0)
					classes = ' class="even"';
				else
					classes = '';
				$("#player_playlist tbody").append('<tr' + classes + '><td class="invisible">' + data[i].id + '</td><td>' + min + ':' + sec + '</td><td>' + data[i].artist + '</td><td>' + data[i].title + '</td><td>' + data[i].date + '</td><td>' + data[i].album + '</td><td>' + ((DefaultJS.permissions.playlist.change)?'<a href="#remove" onclick="return !DefaultJS.remove_playlistitem(' + data[i].id + ');"><img src="res/img/list-remove.png" width="16" height="16" alt="Remove" title="Remove" /></a>':'') + ' ' + ((DefaultJS.permissions.playback.control)?('<a href="#play" onclick="return !DefaultJS.play_playlistitem(' + data[i].id + ');"><img src="res/img/media-playback-start.png" width="16" height="16" alt="Start playback here" title="Start playback here" /></a>'):'') + ' ' + ((DefaultJS.permissions.playlist.change && i != 0)?'<a href="#moveup" onclick="return !DefaultJS.move_playlistitem_up(' + data[i].id + ');"><img src="res/img/go-up.png" height="16" width="16" alt="Move up" title="Move up" /></a>':'') + ' ' + ((DefaultJS.permissions.playlist.change && i != data.length-1)?'<a href="#movedown" onclick="return !DefaultJS.move_playlistitem_down(' + data[i].id + ');"><img src="res/img/go-down.png" height="16" width="16" alt="Move down" title="Move down" /></a>':'') + '</td></tr>');
				DefaultJS.playlist.push(parseInt(data[i].id));
			}
			$("#player_playlist_length").html(playlist_len);
			var secs = parseInt(playlist_time);
			if (secs >= 3600)
			{
				var mins = Math.floor(secs/60.);
				secs -= mins*60;
				var hours = Math.floor(mins/60.);
				mins -= hours*60;
				if (mins < 10)
					mins = '0' + mins;
				if (secs < 10)
					secs = '0' + secs;
				$("#player_playlist_time").html(hours + 'h ' + mins + 'm ' + secs + 's');
			}
			else if (secs >= 60)
			{
				var mins = Math.floor(secs/60.);
				secs -= mins*60;
				if (mins < 10)
					mins = '0' + mins;
				if (secs < 10)
					secs = '0' + secs;
				$("#player_playlist_time").html(mins + 'm ' + secs + 's');
			}
			else
			{
				if (secs < 10)
					secs = '0' + secs;
				$("#player_playlist_time").html(secs + 's');
			};
			if (data.length > 0)
			{
				$("#player_playlist_empty").addClass("invisible");
				$("#player_playlist_notempty").removeClass("invisible");
			}
			else
			{
				$("#player_playlist_empty").removeClass("invisible");
				$("#player_playlist_notempty").addClass("invisible");
			};
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
		if (!confirm("Do you really want to delete this song from the playlist?"))
		{
			return true;
		}
		else
		{
			$.get('ajax.py?action=deleteid&id=' + id, function (data) {
				DefaultJS.get_status();
			});
		};
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
			data.sort();
			for (i=0; i < data.length; i++)
			{
				$("#database_table_artists").append('<li>' + ((DefaultJS.permissions.playlist.add.artist)?'<a href="#add" onclick="return !DefaultJS.addto_playlist_artist(\'' + data[i].replace(/'/g, "\\'") + '\');"><img src="res/img/list-add.png" alt="Add to playlist" height="16" width="16" /></a>':'') + ' <a href="#albums" onclick="return !DefaultJS.get_albums(\'' + data[i].replace(/'/g, "\\'") + '\', false);">' + ((data[i])?data[i]:'[Unknown Artist]') + '</a></li>');
			}
		});
	},
	get_albums: function (artist, all)
	{
		/*
		 * Clean up & set table headers:
		*/
		if (all)
			$("#database_table_albums_header").html("All Albums");
		else if (artist)
			$("#database_table_albums_header").html("Albums (" + artist + ")");
		else
			$("#database_table_albums_header").html("Albums ([Unknown Artist])");
		$("#database_table_albums li").remove();
		$("#database_table_songs li").remove();
		$("#database_table_songs_header").html("Songs");
		/*
		 * Receive albums:
		*/
		$.getJSON('ajax.py?action=albums&artist=' + encodeURIComponent(artist) + ((all==true)?'&all':''), function (data) {
			var i;
			if (all == true)
				$("#database_table_albums").append('<li><a href="#songs" onclick="return !DefaultJS.get_songs(\'\', \'\', false, false, true);">ALL SONGS</a></li>');
			else
				$("#database_table_albums").append('<li><a href="#songs" onclick="return !DefaultJS.get_songs(\'' + artist.replace(/'/g, "\\'") + '\', \'\', true, false, false);">ALL SONGS</a></li>');
			data.sort();
			for (i=0; i < data.length; i++)
			{
				if (data[i] == "")
				{
					if (all == true)
						$("#database_table_albums").append('<li>' + ((DefaultJS.permissions.playlist.add.album)?'<a href="#add" onclick="return !DefaultJS.addto_playlist_album(\'\');"><img src="res/img/list-add.png" alt="Add to playlist" height="16" width="16" /></a>':'') + ' <a href="#songs" onclick="return !DefaultJS.get_songs(\'\', \'\', false, true, false);">[Unknown Album]</a></li>');
					else
						$("#database_table_albums").append('<li>' + ((DefaultJS.permissions.playlist.add.album)?'<a href="#add" onclick="return !DefaultJS.addto_playlist_album(\'\', \'' + artist.replace(/'/g, "\\'") + '\');"><img src="res/img/list-add.png" alt="Add to playlist" height="16" width="16" /></a>':'') + ' <a href="#songs" onclick="return !DefaultJS.get_songs(\'' + artist.replace(/'/g, "\\'") + '\', \'\', false, false, false);">[Unknown Album]</a></li>');
					break;
				};
			}
			for (i=0; i < data.length; i++)
			{
				if (data[i] != "")
				{
					if (all == true)
						$("#database_table_albums").append('<li>' + ((DefaultJS.permissions.playlist.add.album)?'<a href="#add" onclick="return !DefaultJS.addto_playlist_album(\'' + data[i].replace(/'/g, "\\'") + '\');"><img src="res/img/list-add.png" alt="Add to playlist" height="16" width="16" /></a>':'') + ' <a href="#songs" onclick="return !DefaultJS.get_songs(\'\', \'' + data[i].replace(/'/g, "\\'") + '\', false, false, false);">' + data[i] + '</a></li>');
					else
						$("#database_table_albums").append('<li>' + ((DefaultJS.permissions.playlist.add.album)?'<a href="#add" onclick="return !DefaultJS.addto_playlist_album(\'' + data[i].replace(/'/g, "\\'") + '\', \'' + artist.replace(/'/g, "\\'") + '\');"><img src="res/img/list-add.png" alt="Add to playlist" height="16" width="16" /></a>':'') + ' <a href="#songs" onclick="return !DefaultJS.get_songs(\'' + artist.replace(/'/g, "\\'") + '\', \'' + data[i].replace(/'/g, "\\'") + '\', false, false, false);">' + data[i] + '</a></li>');
				};
			}
		});
		return true;
	},
	get_songs: function (artist, album, all_artist, all_album, all)
	{
		/*
		 * Clean up:
		*/
		$("#database_table_songs li").remove();
		/*
		 * Receive songs:
		*/
		$.getJSON('ajax.py?action=songs&artist=' + encodeURIComponent(artist) + '&album=' + encodeURIComponent(album) + ((all_artist==true)?'&all_artist':'') + ((all_album==true)?'&all_album':'') + ((all==true)?'&all':''), function (data) {
			var i;
			if (all)
				$("#database_table_songs_header").html("All Songs");
			else if (all_artist)
			{
				if (artist == "")
					$("#database_table_songs_header").html("Songs ([Unknown Artist])");
				else
					$("#database_table_songs_header").html("Songs (" + artist + ")");
			}
			else if (all_album)
			{
				$("#database_table_songs_header").html("Songs ([Unknown Album])");
			}
			else
			{
				if (artist == "" && data[0].artist == null)
					artist = "[Unknown Artist]";
				else if (data[0].artist != null)
					artist = data[0].artist;
				if (album == "")
					album = "[Unknown Album]";
				$("#database_table_songs_header").html("Songs (" + artist + " - " + album +")");
			};
			for (i=0; i < data.length; i++)
			{
				if (data[i].title == null)
					showtitle = data[i].file;
				else
					showtitle = data[i].title;
				if (data[i].track != null)
				{
					if (data[i].track.match(/\//) != null)
					{
						var track = data[i].track.split("/")[0];
						if (track.length == 1)
							track = '0' + track;
						showtitle = track + ' - ' + showtitle;
					}
					else
					{
						var track = data[i].track;
						if (track.length == 1)
							track = '0' + track;
						showtitle = track + ' - ' + showtitle;
					};
				};
				$("#database_table_songs").append('<li>' + ((DefaultJS.permissions.playlist.add.file)?'<a href="#add" onclick="return !DefaultJS.addto_playlist(\'' + data[i].file.replace(/'/g, "\\'") + '\');"><img src="res/img/list-add.png" alt="Add to playlist" height="16" width="16" /></a>':'') + ' ' + showtitle + '</li>');
			}
		});
		return true;
	},
	addto_playlist: function (file)
	{
		$.getJSON('ajax.py?action=add&file=' + encodeURIComponent(file), function (data) {
			DefaultJS.get_status();
			/*
			 * Show status:
			*/
			if (data.artist != null && data.title != null && data.album != null)
				status = data.artist + ' - ' + data.title + ' (' + data.album + ')';
			else if (data.artist != null && data.title != null)
				status = data.artist + ' - ' + data.title;
			else
				status = data.file;
			DefaultJS.show_status('<em>' + status + '</em> successfully added to playlist!', "info");
		});
		return true;
	},
	addto_playlist_artist: function (artist)
	{
		$.get('ajax.py?action=addartist&artist=' + encodeURIComponent(artist), function (data) {
			DefaultJS.get_status();
			/*
			 * Show status:
			*/
			DefaultJS.show_status('All songs of <em>' + artist + '</em> successfully added to playlist!');
		});
		return true;
	},
	addto_playlist_album: function (album, artist)
	{
		$.get('ajax.py?action=addalbum&album=' + encodeURIComponent(album) + ((artist!=null)?('&artist=' + encodeURIComponent(artist)):''), function (data) {
			DefaultJS.get_status();
			/*
			 * Show status:
			*/
			if (album == "")
				album = "[Unknown Album]";
			if (artist == null)
			{
				DefaultJS.show_status('All songs of the album <em>' + album + '</em> successfully added to playlist!');
			}
			else
			{
				DefaultJS.show_status('All songs of the album <em>' + album + '</em> by <em>' + artist + '</em> successfully added to playlist!');
			};
		});
		return true;
	},
	status_timeout: null,
	show_status: function (status, type, timeout)
	{
		if (type == null)
			type = "info";
		if (timeout == null)
			timeout = 10000;
		$("#player_statusmessage").html(status);
		switch (type)
		{
			case "error":
				$("#player_statusmessage").css("background-image", "url('res/img/dialog-error.png')");
				break;
			case "warning":
				$("#player_statusmessage").css("background-image", "url('res/img/dialog-warning.png')");
				break;
			default:
				$("#player_statusmessage").css("background-image", "url('res/img/dialog-information.png')");
		}
		$("#player_statusmessage").removeClass("invisible");
		window.clearTimeout(this.status_timeout);
		this.status_timeout = window.setTimeout(this.clear_status, timeout);
	},
	clear_status: function ()
	{
		$("#player_statusmessage").addClass("invisible");
	},
	play_playlistitem: function (id)
	{
		$.get('ajax.py?action=playid&id=' + id, function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	clear_playlist: function ()
	{
		if (!confirm("Do you really want to clear the playlist?"))
		{
			return true;
		}
		else
		{
			$.get('ajax.py?action=clear', function (data) {
				DefaultJS.get_status();
			});
			return true;
		};
	},
	list_filesystem: function (path)
	{
		if (path == null)
			path = "";
		$.getJSON('ajax.py?action=ls&path=' + encodeURIComponent(path), function (data) {
			var i;
			$("#filesystem_list li").remove();
			/*
			 * List .. directory:
			*/
			if (path != "")
			{
				lastpath = path.split('/');
				lastpath.pop();
				lastpath = lastpath.join('/');
				$("#filesystem_list").append('<li class="folder"><a href="#filesystem" onclick="return !DefaultJS.list_filesystem(\'' + lastpath.replace(/'/g, "\\'") + '\');">..</a></li>');
			};
			/*
			 * List directories:
			*/
			directories = [];
			for (i=0; i < data.length; i++)
			{
				if (data[i].directory != null)
				{
					directories.push(data[i].directory);
				};
			}
			directories.sort();
			for (i=0; i < directories.length; i++)
			{
				$("#filesystem_list").append('<li class="folder"><a href="#filesystem" onclick="return !DefaultJS.list_filesystem(\'' + directories[i].replace(/'/g, "\\'") + '\');">' + directories[i].split('/').pop() + '</a></li>');
			}
			/*
			 * List files:
			*/
			files = [];
			for (i=0; i < data.length; i++)
			{
				if (data[i].file != null)
				{
					files.push(data[i].file);
				};
			}
			files.sort();
			for (i=0; i < files.length; i++)
			{
				$("#filesystem_list").append('<li class="music">' + ((DefaultJS.permissions.playlist.add.file)?'<a href="#add" onclick="return !DefaultJS.addto_playlist(\'' + files[i].replace(/'/g, "\\'") + '\');">' + files[i].split('/').pop() + '</a>':files[i].split('/').pop()) + '</li>');
			}
		});
		return true;
	},
	normal_search: function ()
	{
		/*
		 * Fill the 'any' field of the advanced search form:
		*/
		$("#advanced_search_any").prop('value', $("#search_query").prop('value'));
		/*
		 * Clear the field of the normal search form:
		*/
		$("#search_query").prop('value', 'Query');
		$("#search_query").css('color', 'grey');
		/*
		 * Go to the search tab:
		*/
		$("#player_list_tabs").tabs("option", "active", 3);
		/*
		 * Submit the advanced search form:
		*/
		$("#advanced_search_submit").click();
	},
	advanced_search: function ()
	{
		$.getJSON('ajax.py?action=search&any=' + encodeURIComponent($("#advanced_search_any").prop('value')) + '&artist=' + encodeURIComponent($("#advanced_search_artist").prop('value')) + '&title=' + encodeURIComponent($("#advanced_search_title").prop('value')) + '&album=' + encodeURIComponent($("#advanced_search_album").prop('value')) + '&file=' + encodeURIComponent($("#advanced_search_filename").prop('value')) + '&composer=' + encodeURIComponent($("#advanced_search_composer").prop('value')) + '&performer=' + encodeURIComponent($("#advanced_search_performer").prop('value')) + '&genre=' + encodeURIComponent($("#advanced_search_genre").prop('value')) + '&date=' + encodeURIComponent($("#advanced_search_year").prop('value')) + '&comment=' + encodeURIComponent($("#advanced_search_comment").prop('value')), function (data) {
			if (data.length == 0)
			{
				/*
				 * Show the right column:
				*/
				$("#search_results_nosearch").addClass("invisible");
				$("#search_results_noresults").removeClass("invisible");
				$("#search_results").addClass("invisible");
			}
			else
			{
				var i;
				/*
				 * Clean up:
				*/
				$("#search_results_list li").remove();
				/*
				 * Add results:
				*/
				for (i=0; i < data.length; i++)
				{
					if (data[i].artist != null && data[i].title != null && data[i].album != null)
						name = data[i].artist + ' - ' + data[i].title + ' (' + data[i].album + ')';
					else if (data[i].artist != null && data[i].title != null)
						name = data[i].artist + ' - ' + data[i].title;
					else
						name = data[i].file.split('/').pop();
					$("#search_results_list").append('<li>' + ((DefaultJS.permissions.playlist.add.file)?'<a href="#add" onclick="return !DefaultJS.addto_playlist(\'' + data[i].file.replace(/'/g, "\\'") + '\');">' + name + '</a>':name) + '</li>');
				}
				/*
				 * Show the right column:
				*/
				$("#search_results_nosearch").addClass("invisible");
				$("#search_results_noresults").addClass("invisible");
				$("#search_results").removeClass("invisible");
			};
		});
	},
	list_playlists: function ()
	{
		$.getJSON('ajax.py?action=listplaylists', function (data) {
			var i;
			$("#stored_playlists li").remove();
			for (i=0; i < data.length; i++)
			{
				$("#stored_playlists").append('<li>' + ((DefaultJS.permissions.stored_playlists.load)?'<a href="#load" onclick="return !DefaultJS.load_stored(\'' + data[i].playlist.replace(/'/g, "\\'") + '\');"><img src="res/img/list-add.png" alt="Add" title="Add to playlist" width="16" height="16" /></a>':'') + ' ' + ((DefaultJS.permissions.stored_playlists.remove)?'<a href="#remove" onclick="return !DefaultJS.rm_stored(\'' + data[i].playlist.replace(/'/g, "\\'") + '\');"><img src="res/img/list-remove.png" alt="Remove" title="Remove stored playlist" width="16" height="16" /></a>':'') + ' <a href="#playlistinfo" onclick="return !DefaultJS.list_playlist_items(\'' + data[i].playlist.replace(/'/g, "\\'") + '\');">' + data[i].playlist + '</a></li>');
			}
		});
	},
	list_playlist_items: function (name)
	{
		$.getJSON('ajax.py?action=listplaylistinfo&name=' + encodeURIComponent(name), function (data) {
			var i;
			$("#stored_playlists_table_items_header").html('Items (' + name + ')');
			$("#stored_playlist_items li").remove();
			for (i=0; i < data.length; i++)
			{
				if (data[i].artist != null && data[i].title != null && data[i].album != null)
					name = data[i].artist + ' - ' + data[i].title + ' (' + data[i].album + ')';
				else if (data[i].artist != null && data[i].title != null)
					name = data[i].artist + ' - ' + data[i].title;
				else
					name = data[i].file.split('/').pop();
				$("#stored_playlist_items").append('<li>' + name + '</li>');
			}
		});
		return true;
	},
	load_stored: function (name)
	{
		$.get('ajax.py?action=load&name=' + encodeURIComponent(name), function (data) {
			DefaultJS.get_status();
			DefaultJS.show_status('All songs of the stored playlist <em>' + name + '</em> successfully added to playlist!');
		});
		return true;
	},
	rm_stored: function (name)
	{
		if (!confirm("Really delete the playlist '" + name + "'?"))
		{
			return true;
		}
		else
		{
			$.get('ajax.py?action=rm&name=' + encodeURIComponent(name), function (data) {
				$("#stored_playlists_table_items_header").html('Items');
				$("#stored_playlist_items li").remove();
				DefaultJS.list_playlists();
				DefaultJS.show_status('Successfully deleted the stored playlist <em>' + name + '</em>!');
			});
			return true;
		};
	},
	show_playlist_saver: function ()
	{
		// Try to get playlist name from user:
		var name = '';
		while (name != null && name.replace(/^\s+|\s+$/g, '') == '')
			name = prompt("Please enter a name for the playlist.", "");
		if (name == null)
		{
			return true;
		}
		else
		{
			name = name.replace(/^\s+|\s+$/g, '');
			// Save the playlist:
			DefaultJS.save_playlist(name);
			return true;
		};
	},
	save_playlist: function (name)
	{
		$.get('ajax.py?action=save&name=' + encodeURIComponent(name), function (data) {
			DefaultJS.show_status('Playlist successfully saved as <em>' + name + '</em>!');
		});
		return true;
	},
	move_playlistitem_up: function (id)
	{
		var i, pos;
		// Get old position:
		for (i=0; i < DefaultJS.playlist.length; i++)
		{
			if (DefaultJS.playlist[i] == id)
				pos = i;
		}
		// Get new position:
		pos--;
		// Send request:
		DefaultJS.move_playlistitem(id, pos);
		return true;
	},
	move_playlistitem_down: function (id)
	{
		var i, pos;
		// Get old position:
		for (i=0; i < DefaultJS.playlist.length; i++)
		{
			if (DefaultJS.playlist[i] == id)
				pos = i;
		}
		// Get new position:
		pos++;
		// Send request:
		DefaultJS.move_playlistitem(id, pos);
		return true;
	},
	list_outputs: function ()
	{
		$.getJSON('ajax.py?action=outputs', function (data) {
			var i;
			$("#audio_outputs li").remove();
			for (i=0; i < data.length; i++)
			{
				$("#audio_outputs").append('<li>' + (((data[i].outputenabled=='0' && DefaultJS.permissions.outputs.enable) || (data[i].outputenabled=='1' && DefaultJS.permissions.outputs.disable))?'<input type="checkbox" onclick="return DefaultJS.set_output(' + data[i].outputid + ', ' + (data[i].outputenabled=='0') + ');"' + ((data[i].outputenabled=='1')?' checked="checked"':'') + ' />':'') + ' ' + data[i].outputname + '</li>');
			}
		});
	},
	set_output: function (id, enabled)
	{
		if (enabled)
			var action = 'enableoutput';
		else
			var action = 'disableoutput';
		$.get('ajax.py?action=' + action + '&id=' + id, function (data) {
			DefaultJS.list_outputs();
			if (enabled)
				DefaultJS.show_status('Output successfully enabled.');
			else
				DefaultJS.show_status('Output successfully disabled.');
		});
		return true;
	},
	format_time: function (secs)
	{
		if (secs >= 86400)
		{
			var mins = Math.floor(secs/60.);
			secs -= mins*60;
			var hours = Math.floor(mins/60.);
			mins -= hours*60;
			var days = Math.floor(hours/24.);
			hours -= days*24;
			if (hours < 10)
				hours = '0' + hours;
			if (mins < 10)
				mins = '0' + mins;
			if (secs < 10)
				secs = '0' + secs;
			return days + 'd ' + hours + 'h ' + mins + 'm ' + secs + 's';
		}
		else if (secs >= 3600)
		{
			var mins = Math.floor(secs/60.);
			secs -= mins*60;
			var hours = Math.floor(mins/60.);
			mins -= hours*60;
			if (mins < 10)
				mins = '0' + mins;
			if (secs < 10)
				secs = '0' + secs;
			return hours + 'h ' + mins + 'm ' + secs + 's';
		}
		else if (secs >= 60)
		{
			var mins = Math.floor(secs/60.);
			secs -= mins*60;
			if (secs < 10)
				secs = '0' + secs;
			return mins + 'm ' + secs + 's';
		}
		else
		{
			if (secs < 10)
				secs = '0' + secs;
			return secs + 's';
		};
	},
	get_stats: function ()
	{
		$.getJSON('ajax.py?action=stats', function (data) {
			/*
			 * artists:
			*/
			$("#statistics_artists").html(data.artists);
			/*
			 * albums:
			*/
			$("#statistics_albums").html(data.albums);
			/*
			 * songs:
			*/
			$("#statistics_songs").html(data.songs);
			/*
			 * playtime:
			*/
			$("#statistics_playtime").html(DefaultJS.format_time(parseInt(data.playtime)));
			/*
			 * db_playtime:
			*/
			$("#statistics_db_playtime").html(DefaultJS.format_time(parseInt(data.db_playtime)));
			/*
			 * db_update:
			*/
			$("#statistics_db_update").html(DefaultJS.format_time(parseInt(data.db_update)) + ' ago');
			/*
			 * uptime:
			*/
			$("#statistics_uptime").html(DefaultJS.format_time(parseInt(data.uptime)));
		});
	},
	shuffle_playlist: function ()
	{
		$.get('ajax.py?action=shuffle', function (data) {
			DefaultJS.get_status();
		});
		return true;
	},
	update_database: function ()
	{
		$.get('ajax.py?action=update', function (data) {
			DefaultJS.show_status('Database update started.');
		});
		return true;
	},
	rescan_database: function ()
	{
		if (confirm("Do you REALLY want to rescan the database? This may take a lot of time."))
		{
			$.get('ajax.py?action=rescan', function (data) {
				DefaultJS.show_status('Database rescan started.');
			});
		};
		return true;
	}
}
