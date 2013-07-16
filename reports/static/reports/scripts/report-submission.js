/* jshint strict: true, browser: true, devel: true */
/* global angular, $, reform */
'use strict';


reform.widgets.map = function() {

	// create a map in the "map" div, set the view to a given place and zoom
	var map = L.map('map');

	map.setView([34.161818161230386, 9.3603515625], 5);

	//L.control.scale().addTo(map);

	//map.legendControl.addLegend("Incident location");

	map.setMaxBounds(map.getBounds());

	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		//attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	// Popup
	var popup = L.popup()
		.setLatLng([51.5, -0.09])
		.setContent("I am a standalone popup.")
		.openOn(map);

	// add a marker in the given location, attach some popup content to it and open the popup
	/*
	L.marker([51.5, -0.09]).addTo(map)
		.bindPopup('A pretty CSS3 popup. <br> Easily customizable.')
		.openPopup();
	*/

	var marker;

	var location = $('#id_location');
	var loc = location.val();
	console.log(loc);
	if (loc) {
		loc = loc.split(',')
		var lat = parseFloat(loc[0]), lng = parseFloat(loc[1]);
		console.log(loc, lat, lng);
		var latlng = new L.LatLng(lat, lng);
		console.log(latlng);
		marker = L.marker(latlng, {
			draggable: true
		});
		marker.addTo(map);
	}

	map.on('click ', function map_click(e) {
		console.log(e.latlng);;
		if (!marker) {
			marker = L.marker(e.latlng, {
				draggable: true
			});
			marker.addTo(map);
			marker.on('dragend', function(e) {
				//window.eee = e;
				var value = '' + e.target._latlng.lat + ',' + e.target._latlng.lng;
				console.log(e.target._latlng, value);
				document.getElementById('id_location').value = value;
			});
		} else {
			console.log(marker);
			marker.setLatLng(e.latlng);
		}
		document.getElementById('id_location').value = '' + e.latlng.lat + ',' + e.latlng.lng;
	});

};

$(reform.widgets.map);


reform.widgets.geosearch = function() {};

$(reform.widgets.geosearch);
