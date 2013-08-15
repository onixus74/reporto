/* jshint strict: true, browser: true, devel: true */
/* global angular, $, L, Dropzone, reform */
'use strict';


reform.widgets.map = {};
reform.widgets.map.init = function() {

	var widget = reform.widgets.map;

	// create a map in the "map" div, set the view to a given place and zoom
	var map = L.map('map');
	widget.object = map;

	map.setView([34.161818161230386, 9.3603515625], 5);

	//L.control.scale().addTo(map);

	//map.legendControl.addLegend("Incident location");

	map.setMaxBounds(map.getBounds());

	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		//attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	// Popup
	/*
	var popup = L.popup()
		.setLatLng([51.5, -0.09])
		.setContent("I am a standalone popup.")
		.openOn(map);
		*/

	// add a marker in the given location, attach some popup content to it and open the popup
	/*
	L.marker([51.5, -0.09]).addTo(map)
		.bindPopup('A pretty CSS3 popup. <br> Easily customizable.')
		.openPopup();
	*/

	var geoSearch = new L.Control.GeoSearch({
		provider: new L.GeoSearch.Provider.Google({ region: 'tn' }),
		//country: "tn",
		zoomLevel: 16
	});
	map.addControl(geoSearch);
	widget.geoSearch = geoSearch;

	map.scrollWheelZoom.disable();

	var marker;

	var location = $('#id_location');
	var location_text = $('#id_location_text');
	var loc = location.val();
	console.log(loc);
	if (loc) {
		loc = loc.split(',');
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
		console.log(e.latlng);
		if (!marker) {
			marker = L.marker(e.latlng, {
				draggable: true
			});
			marker.addTo(map);
			marker.on('dragend', function(e) {
				var value = '' + e.target._latlng.lat + ',' + e.target._latlng.lng;
				console.log(e.target._latlng, value);
				location.val(value).change();
			});
		} else {
			console.log(marker);
			marker.setLatLng(e.latlng);
		}

		location.val('' + e.latlng.lat + ',' + e.latlng.lng).change();
	});

};

//$(reform.widgets.map.init);

Dropzone.autoDiscover = false;

Dropzone.options.assets = {
	paramName: "files", // The name that will be used to transfer the file
	headers: {
		'X-CSRFToken': csrf_token,
		'X-RSID': report_submit_id
	},
	maxFilesize: 10, // MB
	uploadMultiple: true,
	/*
	addRemoveLinks: true,
	accept: function(file, done) {
		console.log(file);
		done();
	},
	*/
	/*
	removedfile: function(file){
		console.log(file);
		window.file = file;
		return true;
	},
	*/
	dictDefaultMessage: "Drop files or click to upload evidence photos/videos"
};

reform.widgets.dropzone = {};
reform.widgets.dropzone.init = function() {

	var widget = reform.widgets.dropzone;
	var dropzone = new Dropzone("div#assets", { url: reform.urls.upload });
	widget.object = dropzone;

};

$(reform.widgets.dropzone.init);


reform.widgets.wizard = {};
reform.widgets.wizard.init = function() {

	//$('.select2').select2()
	$('.select2').selectpicker();
	/*
	$('.datetimepicker').datetimepicker({
		//language: 'en',
		pick12HourFormat: true
	});
	*/

	var widget = reform.widgets.wizard;
	//var wizard =
	//widget.object = wizard;

	var elements = widget.elements = {};

	elements.reporterState = $('#ui-wizard-reporter-state');
	console.log(elements.reporterState);

	var sections = widget.sections = {
		'victim-witness': $('#ui-wizard-victim-witness-buttons'),
		'category-datetime': $('#ui-wizard-category-datetime'),
		'location' : $('#ui-wizard-location'),
		'victim-aggressor' : $('#ui-wizard-victim-aggressor'),
		'description-evidence' : $('#ui-wizard-description-evidence'),
		'features' : $('#ui-wizard-features'),
		'submit' : $('#ui-wizard-submit')
	}

	console.log(sections);

	elements.progressBar = $('#ui-wizard-progress');

	/* victim-witness section */

	elements.victimButton = $('#ui-wizard-victim-button');
	console.log(elements.victimButton);
	elements.victimButtonContainer = $('#ui-wizard-victim-button-container');
	console.log(elements.victimButtonContainer);
	elements.witnessButton = $('#ui-wizard-witness-button');
	console.log(elements.witnessButton);
	elements.witnessButtonContainer = $('#ui-wizard-witness-button-container');
	console.log(elements.witnessButtonContainer);

	function victimWitnessButtonsAction(e){
		var el = $(this);
		elements.reporterState.html(el.data('value')).addClass(el.data('class')).addClass('animated pulse');
		sections['category-datetime'].addClass('animated fadeIn').show();
		sections['victim-witness'].addClass('animated fadeOut');
		elements.progressBar.css({width: "10%"});
		elements.victimButton.off('click');
		elements.witnessButton.off('click');
	}

	elements.victimButton.on('click', function(e){
		victimWitnessButtonsAction.call(this, e);
		$('#ui-wizard-victim').show();
	});

	elements.witnessButton.on('click', function(e){
		victimWitnessButtonsAction.call(this, e);
		$('#ui-wizard-witness').show();
	});

	function showSection(section, fields, callback, progress){

		function showSectionClosure(e){

			console.log(this);
			console.log(e.target);
			//console.log(this.name);
			//console.log(e.target.name);

			var fields = showSectionClosure.fields;
			console.log(fields);

			fields[this.name] = true;
			console.log(fields);

			var ready = Object.keys(fields).reduce(function (previous, key) {
				return previous && fields[key];
			}, true);

			console.log(ready);

			if(ready){
				sections[section].addClass('animated fadeIn').show();
				if(callback)
					callback();
				if(progress)
					elements.progressBar.css({width: progress + "%"});
			}

			$(this).off('change.showSection');

		}
		showSectionClosure.fields = {};
		fields.forEach(function(name){
			showSectionClosure.fields[name] = false;
		})

		return showSectionClosure;

	}


	/* category-datetime section */

	elements.category = $('#id_category');
	console.log(elements.category);

	elements.datetime = $('#id_datetime');
	console.log(elements.datetime);

	var showLocationSection = showSection('location', ['category', 'datetime'], reform.widgets.map.init, 20);
	elements.category.on('change.showSection', showLocationSection);
	elements.datetime.on('change.showSection', showLocationSection);

	/* location section */

	elements.location = $('#id_location');
	console.log(elements.location);

	elements.location_text = $('#id_location_text');
	console.log(elements.location_text);

	var showVictimAggressorSection = showSection('victim-aggressor', ['location', 'location_text'], null, 30);
	elements.location.on('change.showSection', showVictimAggressorSection);
	elements.location_text.on('change.showSection', showVictimAggressorSection);

	elements.location.on('change', function(e){
		var location_text = elements.location_text;
		console.log(this.value);
		var latlng = this.value.split(',');
		console.log(latlng);
		var lat = parseFloat(latlng[0], 10), lng = parseFloat(latlng[1], 10);
		var geocoder = new google.maps.Geocoder();
		//var geocoder = L.GeoSearch.Provider.Google.Geocoder;
		geocoder.geocode({location: new google.maps.LatLng(lat, lng), region: 'tn'}, function(data, status){
			//try { location_text.typeahead('destroy'); } catch(e) {};
			if (status == google.maps.GeocoderStatus.OK) {
				var results = [];
				for (var i = 0; i < data.length; i++)
					results.push(data[i].formatted_address);
				console.log(results);
				if(results.length > 0){
					/*
					location_text.typeahead({
						//name: 'location_text',
						local: results
					});
					*/
					location_text.val(results[0]).change();
				}
			}
		});
	});

	/* victim-aggressor section */

	elements.victim = $('#id_victim');
	console.log(elements.victim);

	elements.aggressor = $('#id_aggressor');
	console.log(elements.aggressor);

	var showDescriptionEvidenceSection = showSection('description-evidence', ['victim', 'aggressor'], null, 40);
	elements.victim.on('change.showSection', showDescriptionEvidenceSection);
	elements.aggressor.on('change.showSection', showDescriptionEvidenceSection);

	/* description-evidence section */

	elements.description = $('#id_description');
	console.log(elements.description);

	var showFeaturesSection = showSection('features', ['description'], null, 50);
	elements.description.on('change.showSection', showFeaturesSection);

	/*
	elements.description.on('change.showSection', function(e){
		sections['features'].addClass('animated fadeIn').show();
		elements.progressBar.css({width: "50%"});
		elements.description.off('change.showSection');
	});
	*/

	elements.features = $('#id_features');
	console.log(elements.features);

	var showSubmitSection = showSection('submit', ['features'], null, 100);
	elements.features.on('change.showSection', showSubmitSection);

	/*
	elements.features.on('change.showSection', function(e){
		sections['submit'].addClass('animated fadeIn').show();
		elements.progressBar.css({width: "100%"});
		elements.features.off('change.showSection');
	});
	*/


	/*
	var el = $(this);	widget.location = $('#id_location');
	widget.reporterState.html(el.data('value'));
	widget.location.on('change', function(e){
		console.log(e);
	});
	*/


$('#report-form').on('submit', function(e){
	var data = {};
	$(this).serializeArray().forEach(function(e){
		if(e.name != 'csrfmiddlewaretoken')
			data[e.name] = e.value;
	})
	console.log(data);

	$.ajax({
		type: "POST",
		url: reform.urls.submit,
		data: data,
		//success: success,
		//dataType: dataType
		headers: {"X-CSRFToken": csrf_token}
	}).done(function(){
	//$.post('/reports/submit/ajax', data).done(function(){
		console.log(arguments);
	});
  return false;
})

};

$(reform.widgets.wizard.init);

/*
reform.widgets.xxx = {};
reform.widgets.xxx.init = function() {
	var widget = reform.widgets.xxx;
	var xxx =
	widget.object = xxx;
	widget.element = xxx;
};

$(reform.widgets.xxx.init);
*/
