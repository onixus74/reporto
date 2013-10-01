/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';

reform.widgets.map = function() {

	// create a map in the "map" div, set the view to a given place and zoom
	var map = reform.widgets.map = L.map('map')

	map.setView([34.161818161230386, 9.3603515625], 5);

	map.setMaxBounds(map.getBounds());

	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

};

$(document).ready(reform.widgets.map);


reform.widgets.geosearch = function() {};

$(document).ready(reform.widgets.geosearch);


reform.widgets.timeline = function() {
	var marker;
	$('.ui-timeline-story').on('mouseover', function(e) {
		e.stopPropagation();
		console.log(marker, e.target, e.currentTarget, e.relatedTarget, e.delegateTarget);
		var loc = $(e.target).closest('li').data('latlng').split(',');
		loc = new L.LatLng(loc[0], loc[1]);
		if (!marker) {
			console.log(loc);
			marker = L.marker(loc);
			console.log(marker);
			marker.addTo(reform.widgets.map);
		} else {
			marker.setLatLng(loc);
		}
		reform.widgets.map.setView(loc, 12);
	})
}

$(document).ready(reform.widgets.timeline);


reform.widgets.stats = function() {

	new Morris.Donut({
		element: 'ui-stats-categories-chart',
		data: reform.data.reportsByCategory,
	});

	new Morris.Donut({
		element: 'ui-stats-features-chart',
		data: reform.data.reportsByFeature,
	});

	new Morris.Donut({
		element: 'ui-stats-victim-gender-chart',
		data: reform.data.reportsByVictimGender,
	});


};

$(document).ready(reform.widgets.stats);
