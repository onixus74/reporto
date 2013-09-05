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
	var updateButton = $('#ui-add-update-comment-button');
	var correctionButton = $('#ui-add-correction-comment-button');
	var comments = $('#ui-comments');
	var comments_formset = document.getElementById('ui-comments-area');
	function handleClick(e) {

		var type = 'U';
		console.log(e.target);
		if(e.target.id == 'ui-add-correction-comment-button')
			type = 'C';

		comments_formset.disabled = true;
		$.post(reform.urls.comment, {
			'csrfmiddlewaretoken': csrf_token,
			type: type,
			content: input.val()
		}).done(function(data) {
			//location.reload();
			$('#ui-no-comments').remove();
			//comments.append('<li class="ui-comment' + (data.object.type == 'C' ? ' text-error' : '') + '"">' + data.object.content + '</li>');
			comments.append(data.html);
			input.val('');
			comments_formset.disabled = false;
		}).fail(function(err) {
			console.log(err);
			comments_formset.disabled = false;
		});
	}
	updateButton.on('click', handleClick);
	correctionButton.on('click', handleClick);

}

$(reform.widgets.comment.init);
