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

$(function() {
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
});



new Morris.Donut({
	// ID of the element in which to drawPthe chart.
	element: 'categoryDonutChart',
	// Chart data records -- each entry in this array corresponds to a point on
	// the chart.
	/*
	data: [
		{ label: 'Verbal Violence', value: 20 },
		{ label: 'Violence', value: 10 },
		{ label: 'Rape', value: 20 },
		{ label: 'Lack of Investigation and Prosecution', value: 50 },

	],
	*/
	data: reform.data.categoryDonut,

});

new Morris.Donut({
	// ID of the element in which to draw the chart.
	element: 'featureDonutChart',
	// Chart data records -- each entry in this array corresponds to a point on
	// the chart.
	data: reform.data.featureDonut,

});



new Morris.Donut({
	// ID of the element in which to draw the chart.
	element: 'myfirstchart3',
	// Chart data records -- each entry in this array corresponds to a point on
	// the chart.
	data: [{
		label: '2008',
		value: 20
	}, {
		label: '2009',
		value: 10
	}, {
		label: '2010',
		value: 5
	}, {
		label: '2011',
		value: 5
	}, {
		label: '2012',
		value: 20
	}],

});

