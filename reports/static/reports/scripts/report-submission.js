/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';


!(function() {

	function latlngToText(lat, lng){
		var p = $.getJSON('//maps.googleapis.com/maps/api/geocode/json?latlng=' + lat + ',' + lng + '&sensor=false');
		p.done(function(data){console.log(data);});
		return p;
	}

	function textTolatlng(text){
		var p = $.getJSON('//maps.googleapis.com/maps/api/geocode/json?address=' + text + '&region=tn&sensor=false');
		p.done(function(data){console.log(data);});
		return p;
	}

	var marker = null,
		geocoder = L.mapbox.geocoder('examples.map-vyofok3q'),
		map = L.mapbox.map('map', 'examples.map-vyofok3q', {attributionControl: false})
		//.addControl(L.mapbox.geocoderControl('examples.map-4l7djmvo'));

	L.control.scale().addTo(map);
	map.legendControl.addLegend("Incident location");
	//geocoder.query('TN', showMap);
	//map.setView([36.80006721245233,10.184755325317383], 10);
	map.setView([34.161818161230386,9.3603515625], 5);
	map.setMaxBounds(map.getBounds());

	function showMap(err, data) {
		console.log(data);
		if (data) {
			map.fitBounds(data.lbounds);
		}
	}

	var location_text = $('#id_location_text');
	location_text.on('change', function(e){
		console.log(this, e);
		geocoder.query(location_text.val() + ', Tunisia', showMap);
		textTolatlng(location_text.val()).done(function(data){
			/*
			var southWest = new L.LatLng(40.712, -74.227),
			northEast = new L.LatLng(40.774, -74.125),
			bounds = new L.LatLngBounds(southWest, northEast);
			map.setBounds(bounds());
			*/
		});
	});

	$(function(){
		var location = $('#id_location');
		var loc = location.val();
		console.log(loc);
		if(loc){
			loc = loc.split(',')
			var lat = parseFloat(loc[0]), lng = parseFloat(loc[1]);
			console.log(loc, lat, lng);
			var latlng = new L.LatLng(lat, lng);
			console.log(latlng);
			marker = L.marker(latlng, {
				icon: L.mapbox.marker.icon({
					'marker-color': 'CC0033'
				}),
				draggable: true
			});
			marker.addTo(map);
		}
	})

	function DragPos(e) {
		document.getElementById('id_location').value = '' + e.latlng.lat + ',' + e.latlng.lng;
	}

	function onMapClick(e) {
		console.log(e.latlng);;
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

		document.getElementById('id_location').value = '' + e.latlng.lat + ',' + e.latlng.lng;

		marker.on('dragend', function(e) {
			//window.eee = e;
			var value = '' + e.target._latlng.lat + ',' + e.target._latlng.lng;
			console.log(e.target._latlng, value);
			document.getElementById('id_location').value = value;
		});

	}

	map.on('click ', onMapClick);

})();
