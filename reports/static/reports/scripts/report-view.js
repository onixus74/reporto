/* jshint strict: true, browser: true, devel: true */
/* global angular, $, L, Dropzone, reform */
'use strict';


reform.widgets.map = {};
reform.widgets.map.init = function() {

	var widget = reform.widgets.map;

	var location = reform.data.report.location.split(',');
	location[0] = parseFloat(location[0], 10);
	location[1] = parseFloat(location[1], 10);
	console.log('location', location);

	// create a map in the "map" div, set the view to a given place and zoom
	var map = widget.object = L.map('map', {
		center: new L.LatLng(location[0], location[1]),
		zoom: 8
	});

	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

	L.marker(location).addTo(map);

	L.control.scale().addTo(map);

	map.setMaxBounds(map.getBounds());

	//map.scrollWheelZoom.disable();

}

$(reform.widgets.map.init);


reform.widgets.comment = {};
reform.widgets.comment.init = function() {
	var widget = reform.widgets.comment;

	var input = $('#ui-add-comment');
	var button = $('#ui-add-comment-button');
	var comments = $('#ui-comments');
	var comments_formset = document.getElementById('ui-comments-area');
	button.on('click', function(e) {
		comments_formset.disabled = true;
		$.post(reform.urls.comment, {
			'csrfmiddlewaretoken': csrf_token,
			content: input.val()
		}).done(function(data) {
			//location.reload();
			comments.append('<li>' + data.object.content + '</li>');
			input.val('');
			comments_formset.disabled = false;
		}).fail(function(err) {
			console.log(err)
		});
	})

}

$(reform.widgets.comment.init);
