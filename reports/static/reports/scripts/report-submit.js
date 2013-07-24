/* jshint strict: true, browser: true, devel: true */
/* global angular, $, reform */
'use strict';


reform.widgets.map = {};
reform.widgets.map.init = function() {

	var widget = reform.widgets.map;

	// create a map in the "map" div, set the view to a given place and zoom
	var map = L.map('map');
	widget.e = map;

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

	new L.Control.GeoSearch({
		provider: new L.GeoSearch.Provider.Google({
			region: 'tn'
		})
	}).addTo(map);

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
	addRemoveLinks: true,
	accept: function(file, done) {
		/*
		if (file.name == "justinbieber.jpg") {
			done("Naha, you don't.");
		}
		else { done(); }
		*/
		done();
	},
	dictDefaultMessage: "Drop files or click to upload evidence photos/videos"
};

reform.widgets.dropzone = {};
reform.widgets.dropzone.init = function() {

	var widget = reform.widgets.dropzone;
	var dropzone = new Dropzone("div#assets", { url: "/reports/submit/upload"});
	widget.e = dropzone;

};

$(reform.widgets.dropzone.init);


reform.widgets.wizard = {};
reform.widgets.wizard.init = function() {
	var widget = reform.widgets.wizard;
	//var wizard =
	//widget.e = wizard;

	widget.reporterState = $('#ui-wizard-reporter-state');
	console.log(widget.reporterState);

	widget.sections = {};

	widget.sections.victimWitnessButtons = $('#ui-wizard-victim-witness-buttons');
	widget.sections.categoryDatetime = $('#ui-wizard-category-datetime');
	widget.sections.location = $('#ui-wizard-location');
	widget.sections.victimAggressor = $('#ui-wizard-victim-aggressor');
	widget.sections.descriptionEvidence = $('#ui-wizard-description-evidence');
	widget.sections.features = $('#ui-wizard-features');
	widget.sections.submit = $('#ui-wizard-submit');
	console.log(widget.sections);

	widget.progressBar = $('#ui-wizard-progress');


	widget.victimButton = $('#ui-wizard-victim-button');
	console.log(widget.victimButton);
	widget.victimButtonContainer = $('#ui-wizard-victim-button-container');
	console.log(widget.victimButtonContainer);
	widget.witnessButton = $('#ui-wizard-witness-button');
	console.log(widget.witnessButton);
	widget.witnessButtonContainer = $('#ui-wizard-witness-button-container');
	console.log(widget.witnessButtonContainer);

	function victimWitnessButtonsAction(e){
		var el = $(this);
		widget.reporterState.html(el.data('value')).addClass(el.data('class')).addClass('animated pulse');
		widget.sections.categoryDatetime.addClass('animated fadeIn').show();
		widget.sections.victimWitnessButtons.addClass('animated fadeOut');
		widget.progressBar.css({width: "10%"});
		widget.victimButton.off('click');
		widget.witnessButton.off('click');
	}

	widget.victimButton.on('click', function(e){
		/*
		var el = $(this);
		widget.reporterState.html(el.data('value')).addClass(el.data('class')).addClass('animated pulse');
		widget.sections.categoryDatetime.addClass('animated fadeIn').show();
		widget.sections.victimWitnessButtons.addClass('animated fadeOut');
		widget.progressBar.css({width: "10%"});
		el.off('click');
		*/
		victimWitnessButtonsAction.call(this, e)
	});

	widget.witnessButton.on('click', function(e){
		/*
		var el = $(this);
		widget.reporterState.html(el.data('value')).addClass(el.data('class')).addClass('animated pulse');
		widget.sections.categoryDatetime.addClass('animated fadeIn').show();
		widget.sections.victimWitnessButtons.addClass('animated fadeOut');
		widget.progressBar.css({width: "10%"});
		el.off('click');
		*/
		victimWitnessButtonsAction.call(this, e)
	});

	widget.category = $('#id_category');
	console.log(widget.category);

	widget.category.on('change', function(e){
		widget.sections.location.addClass('animated fadeIn').show();
		reform.widgets.map.init();
		widget.progressBar.css({width: "20%"});
		widget.category.off('change');
	});

	widget.location = $('#id_location');
	console.log(widget.location);

	widget.location.on('change', function(e){
		console.log('changed', e);
		widget.sections.victimAggressor.addClass('animated fadeIn').show();
		widget.progressBar.css({width: "30%"});
		widget.location.off('change');
	});

	widget.victim = $('#id_victim');
	console.log(widget.victim);

	widget.victim.on('change', function(e){
		widget.sections.descriptionEvidence.addClass('animated fadeIn').show();
		widget.progressBar.css({width: "40%"});
		widget.victim.off('change');
	});

	widget.description = $('#id_description');
	console.log(widget.description);

	widget.description.on('change', function(e){
		widget.sections.features.addClass('animated fadeIn').show();
		widget.progressBar.css({width: "50%"});
		widget.description.off('change');
	});

	widget.features = $('#id_features');
	console.log(widget.features);

	widget.features.on('change', function(e){
		widget.sections.submit.addClass('animated fadeIn').show();
		widget.progressBar.css({width: "100%"});
		widget.features.off('change');
	});


	/*
	var el = $(this);	widget.location = $('#id_location');
	widget.reporterState.html(el.data('value'));
	widget.location.on('change', function(e){
		console.log(e);
	});
	*/

/*
$('#report-form').on('submit', function(e){
  return false;
})
*/

};

$(reform.widgets.wizard.init);

/*
reform.widgets.xxx = {};
reform.widgets.xxx.init = function() {
	var widget = reform.widgets.xxx;
	var xxx =
	widget.e = xxx;
};

$(reform.widgets.xxx.init);
*/
