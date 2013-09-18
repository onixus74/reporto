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

	var content = $('#ui-add-comment-content');
	var attachment = $('#ui-add-comment-attachment');
	var attachmentButton = $('#ui-add-comment-attachment-button');
	var attachmentIcon = $('#ui-comment-attachment-icon');
	var attachmentImage = $('#ui-comment-attachment-image');
	var updateButton = $('#ui-add-update-comment-button');
	var correctionButton = $('#ui-add-correction-comment-button');
	var comments = $('#ui-comments');
	var comments_formset = document.getElementById('ui-comments-area');

	attachment.on('change', function(e){
		var files = e.target.files;
		var f = files[0];
		var reader = new FileReader();

		reader.onload = (function(theFile) {
			return function(e) {
				attachmentImage.attr('src', e.target.result);
				attachmentIcon.hide();
				attachmentImage.show();
			};
		})(f);

		reader.readAsDataURL(f);
	})

	attachmentButton.on('click', function(e){
		attachment.click();
	});

	function handleClick(e) {

		var type = 'U';
		console.log(e.target);
		if(e.target.id == 'ui-add-correction-comment-button')
			type = 'C';

		var formdata = new FormData();
		//formdata.append('csrfmiddlewaretoken': csrf_token);
		formdata.append('content', content.val());
		formdata.append('type', type);
		formdata.append('attachment', attachment.get(0).files[0]);
		console.log(attachment.get(0).files[0])

		comments_formset.disabled = true;
		$.ajax({
			type: "POST",
			url: reform.urls.comment,
			data: formdata,
			processData: false,
			contentType: false,
			//dataType: dataType
			headers: {
				"X-CSRFToken": csrf_token
			}
		}).done(function(data) {
			//location.reload();
			$('#ui-no-comments').remove();
			comments.append(data.html);
			comments.find(".fancybox").fancybox();
			content.val('');
			attachment.val(null);
			$.pnotify({
				title: 'Adding Comment - Done',
				text: 'Comment added',
				type: 'success',
				nonblock: true
			});
			attachmentImage.attr('src', '');
			attachmentIcon.show();
			attachmentImage.hide();
			comments_formset.disabled = false;
		}).fail(function(err) {
			console.log(err);
			$.pnotify({
				title: 'Adding Comment - Failure',
				text: 'Failed to add comment',
				type: 'error',
				//nonblock: true
			});
			comments_formset.disabled = false;
		});
	}
	updateButton.on('click', handleClick);
	correctionButton.on('click', handleClick);

}

$(reform.widgets.comment.init);
