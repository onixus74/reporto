/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';


!(function() {

	var marker = null,
		geocoder = L.mapbox.geocoder('examples.map-4l7djmvo'),
		map = L.mapbox.map('map', 'examples.map-4l7djmvo')
		.addControl(L.mapbox.geocoderControl('examples.map-4l7djmvo'));

	geocoder.query('Tunisia', showMap);

	function showMap(err, data) {
		map.fitBounds(data.lbounds);
	}

	function DragPos(e) {
		document.getElementById('loc').value = '' + e.latlng.lat + ':' + e.latlng.lng;;
	}

	function onMapClick(e) {
		console.log(e.latlng);
		// alert("You clicked the map at " + e.latlng);
		if (!marker) {
			marker = L.marker(e.latlng, {
				icon: L.mapbox.marker.icon({
					'marker-color': 'CC0033'
				}),
				draggable: true
			});
			marker.addTo(map);
		} else {
			console.log(marker);
			marker.setLatLng(e.latlng);

		}

		document.getElementById('id_location').value = e.latlng;
		marker.on('dragend', function(e) {
			window.eee = e;
			document.getElementById('id_location').value = e.target._latlng;
		});

	}

	map.on('click ', onMapClick);

})();
