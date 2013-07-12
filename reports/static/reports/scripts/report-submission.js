/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';

//var app = angular.module('reformPlatform')

app.controller('ReportIncidentCtrl', function($scope) {

	$scope.message = "Hello! from ReportIncidentCtrl";

});

app.controller('ReportsMapCtrl', function($scope, $timeout) {

	// Enable the new Google Maps visuals until it gets enabled by default.
	// See http://googlegeodevelopers.blogspot.ca/2013/05/a-fresh-new-look-for-maps-api-for-all.html
	google.maps.visualRefresh = true;

	angular.extend($scope, {

		position: {
			coords: {
				latitude: 36.799,
				longitude: 10.185441970825194
			}
		},

		/** the initial center of the map */
		centerProperty: {
			latitude: 45,
			longitude: -73
		},

		/** the initial zoom level of the map */
		zoomProperty: 9,

		/** list of markers to put in the map */
		markersProperty: [{
			latitude: 45,
			longitude: -74
		}],

		// These 2 properties will be set when clicking on the map
		clickedLatitudeProperty: null,
		clickedLongitudeProperty: null,

		eventsProperty: {
			click: function(mapModel, eventName, originalEventArgs) {
				// 'this' is the directive's scope
				console.log("user defined event on map directive with scope", this);
				console.log("user defined event: " + eventName, mapModel, originalEventArgs);
			}
		}
	});
});


!(function() {

	var marker = null,
		geocoder = L.mapbox.geocoder('examples.map-4l7djmvo'),
		map = L.mapbox.map('map', 'examples.map-4l7djmvo')
		.addControl(L.mapbox.geocoderControl('examples.map-4l7djmvo')); geocoder.query('Tunisia', showMap);

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
		// document.getElementById('loc').value = '' + e.latlng.lat + ':' + e.latlng.lng;
		document.getElementById('id_location').value = e.latlng;
		marker.on('dragend', function(e) {
			window.eee = e;
			document.getElementById('id_location').value = e.target._latlng;
		});
		//document.getElementById('loc').value = e.latlng;


	}

	map.on('click ', onMapClick);

})();