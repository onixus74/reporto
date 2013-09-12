/* jshint strict: true, browser: true, devel: true */
/* global angular, $, L, Dropzone, reform */
'use strict';

if(!reform) {
	var reform = {
		data: {},
		urls: {},
		widgets: {}
	};
}


reform.widgets.map = {};
reform.widgets.map.init = function() {

	var widget = reform.widgets.map;

	// create a map in the "map" div, set the view to a given place and zoom
	var map = widget.object = L.map('map');

	map.setView([34.161818161230386, 9.3603515625], 5);

	L.control.scale().addTo(map);

	map.setMaxBounds(map.getBounds());

	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		//attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	var geoSearch = new L.Control.GeoSearch({
		provider: new L.GeoSearch.Provider.Google({
			region: 'tn'
		}),
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
	console.log('widget', 'map', 'location', loc);
	if (loc) {
		loc = loc.split(',');
		var lat = parseFloat(loc[0]),
			lng = parseFloat(loc[1]);
		console.log('widget', 'map', 'latlng', loc, lat, lng);
		var latlng = new L.LatLng(lat, lng);
		console.log('widget', 'map', 'latlng', latlng);
		marker = L.marker(latlng, {
			draggable: true
		});
		marker.addTo(map);
	}

	map.on('click ', function map_click(e) {
		console.log('widget', 'map', 'latlng', e.latlng);
		if (!marker) {
			marker = L.marker(e.latlng, {
				draggable: true
			});
			marker.addTo(map);
			marker.on('dragend', function(e) {
				var value = '' + e.target._latlng.lat + ',' + e.target._latlng.lng;
				console.log('widget', 'map', 'latlng', e.target._latlng, value);
				location.val(value).change();
			});
		} else {
			console.log('widget', 'map', 'marker', marker);
			marker.setLatLng(e.latlng);
		}

		location.val('' + e.latlng.lat + ',' + e.latlng.lng).change();
	});

};

//$(reform.widgets.map.init);

Dropzone.autoDiscover = false;

Dropzone.options.assets = {
	paramName: "files", // The name that will be used to transfer the file
	/*
	headers: {
		'X-CSRFToken': csrf_token,
		'X-RSID': report_submit_id
	},
	*/
	maxFilesize: 10, // MB
	uploadMultiple: true,
	autoProcessQueue: false,
	addRemoveLinks: true,
	/*

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
	//var dropzone = new Dropzone("#assets", { url: reform.urls.upload });
	var dropzone = new Dropzone("#assets", {
		url: '/'
	});
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
		'category': $('#ui-wizard-category'),
		'location-datetime': $('#ui-wizard-location-datetime'),
		//'victim-aggressor' : $('#ui-wizard-victim-aggressor'),
		'victim': $('#ui-wizard-victim'),
		'aggressor': $('#ui-wizard-aggressor'),
		'description-evidence': $('#ui-wizard-description-evidence'),
		'features': $('#ui-wizard-features'),
		'submit': $('#ui-wizard-submit')
	}
	var order = widget.order = ['victim-witness', 'category', 'location-datetime', 'victim', 'aggressor', 'description-evidence', 'features', 'submit'];

	console.log(sections);

	elements.progressBar = $('#ui-wizard-progress');

	function progress(index) {
		var progress = (index + 1) * 100 / (order.length - 1);
		console.log('progress', progress, index, order.length);
		elements.progressBar.css({
			width: progress + "%"
		});
	}

	/* victim-witness section */

	elements.victimButton = $('#ui-wizard-victim-button');
	console.log(elements.victimButton);
	elements.victimButtonContainer = $('#ui-wizard-victim-button-container');
	console.log(elements.victimButtonContainer);
	elements.witnessButton = $('#ui-wizard-witness-button');
	console.log(elements.witnessButton);
	elements.witnessButtonContainer = $('#ui-wizard-witness-button-container');
	console.log(elements.witnessButtonContainer);

	function victimWitnessButtonsAction(e) {
		var el = $(this);
		elements.reporterState.html(el.data('value')).addClass(el.data('class')).addClass('animated pulse');
		sections['category'].addClass('animated fadeIn').show();
		sections['victim-witness'].addClass('animated fadeOut');
		progress(0);
		elements.victimButton.off('click');
		elements.witnessButton.off('click');
	}

	elements.victimButton.on('click', function(e) {
		order.splice(order.indexOf('victim'), 1);
		victimWitnessButtonsAction.call(this, e);
		$('#ui-wizard-victim-text').show();
		$('#id_victim').val('user').change();
		//$('#ui-wizard-victim-area').remove();
		//$('#ui-wizard-victim-area').hide();
		//$('#ui-wizard-aggressor-area').removeClass('span6').addClass('span12');
	});

	elements.witnessButton.on('click', function(e) {
		victimWitnessButtonsAction.call(this, e);
		$('#ui-wizard-witness-text').show();
		$('#id_victim').val('0').change();
	});

	/*
	 *  showNextSection	: show sections after all fields changed
	 *
	 *		@section					String						current section, precedes the one to show
	 *		@fields_list			Array							fields to watch
	 *		@callback					Function					callback to call after change
	 */

	function showNextSection(section, fields_list, callback) {

		function showNextSectionClosure(e) {

			console.log('element', this);
			console.log('target', e.target);
			//console.log(this.name);
			//console.log(e.target.name);

			var fields = showNextSectionClosure.fields;
			console.log('fields', fields);

			fields[this.name] = true;
			console.log('fields', fields);

			var ready = Object.keys(fields).reduce(function(previous, key) {
				return previous && fields[key];
			}, true);

			console.log('ready', ready);

			if (ready) {
				var index = order.indexOf(section);
				var next_index = order[index + 1];
				var next_section = sections[next_index];
				console.log('section', section, sections[section]);
				console.log('next section', next_index, next_section);
				if (next_section)
					next_section.addClass('animated fadeIn').show();
				progress(index);
				if (callback)
					callback();
			}

			$(this).off('change.showNextSection');

		}
		showNextSectionClosure.fields = {};
		fields_list.forEach(function(name) {
			showNextSectionClosure.fields[name] = false;
		})

		return showNextSectionClosure;

	}

	function handleShowNextSection(section, fields_list, callback) {
		var handler = showNextSection(section, fields_list, callback);
		fields_list.forEach(function(field) {
			elements[field].on('change.showNextSection', handler);
		})
	}


	/* category section */

	elements.category = $('#id_category');
	console.log(elements.category);

	/*
	var showLocationSection = showNextSection('category-datetime', ['category', 'datetime'], reform.widgets.map.init);
	elements.category.on('change.showNextSection', showLocationSection);
	elements.datetime.on('change.showNextSection', showLocationSection);
	*/
	handleShowNextSection('category', ['category'], reform.widgets.map.init);

	/* location-datetime section */

	elements.location = $('#id_location');
	console.log(elements.location);

	elements.location_text = $('#id_location_text');
	console.log(elements.location_text);

	elements.datetime = $('#id_datetime');
	console.log(elements.datetime);

	/*
	var showVictimAggressorSection = showNextSection('location', ['location', 'location_text']);
	elements.location.on('change.showNextSection', showVictimAggressorSection);
	elements.location_text.on('change.showNextSection', showVictimAggressorSection);
	*/
	handleShowNextSection('location-datetime', ['location', 'location_text', 'datetime']);

	elements.location.on('change', function(e) {
		var location_text = elements.location_text;
		console.log(this.value);
		var latlng = this.value.split(',');
		console.log(latlng);
		var lat = parseFloat(latlng[0], 10),
			lng = parseFloat(latlng[1], 10);
		var geocoder = new google.maps.Geocoder();
		//var geocoder = L.GeoSearch.Provider.Google.Geocoder;
		geocoder.geocode({
			location: new google.maps.LatLng(lat, lng),
			region: 'tn'
		}, function(data, status) {
			//try { location_text.typeahead('destroy'); } catch(e) {};
			if (status == google.maps.GeocoderStatus.OK) {
				var results = [];
				for (var i = 0; i < data.length; i++)
					results.push(data[i].formatted_address);
				console.log(results);
				if (results.length > 0) {
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

	var els = Array.prototype.slice.apply(document.getElementById('ui-victim-fieldset').elements);
	els.forEach(function(e) {
		elements[e.name] = $(e);
	});

	elements.aggressor = $('#id_aggressor');
	console.log(elements.aggressor);

	/*
	var showAggressorSection = showNextSection('victim', ['victim-firstname']);
	elements.victim.on('change.showNextSection', showAggressorSection);
	*/
	handleShowNextSection('victim', ['victim-firstname']);

	/*
	var showDescriptionEvidenceSection = showNextSection('aggressor', ['aggressor']);
	elements.aggressor.on('change.showNextSection', showDescriptionEvidenceSection);
	*/
	handleShowNextSection('aggressor', ['aggressor']);

	/* description-evidence section */

	elements.description = $('#id_description');
	console.log(elements.description);

	/*
	var showFeaturesSection = showNextSection('description-evidence', ['description']);
	elements.description.on('change.showNextSection', showFeaturesSection);
	*/
	handleShowNextSection('description-evidence', ['description']);

	elements.features = $('#id_features');
	console.log(elements.features);

	/*
	var showSubmitSection = showNextSection('features', ['features']);
	elements.features.on('change.showNextSection', showSubmitSection);
	*/
	handleShowNextSection('features', ['features']);


	$('#report-form').on('submit', function(e) {
		e.preventDefault();
		var data = {};
		var formdata = new FormData();
		$(this).serializeArray().forEach(function(e) {
			if (e.name != 'csrfmiddlewaretoken') {
				console.log(e.name, e.value);
				data[e.name] = e.value;
				formdata.append(e.name, e.value);
			}
		});
		var files = reform.widgets.dropzone.object.files;
		for (var i = 0; i < files.length; i++) {
			var file = files[i];
			console.log(file);
			formdata.append('files[]', file);
		}
		$.ajax({
			type: "POST",
			url: reform.urls.submit,
			data: formdata,
			processData: false,
			contentType: false,
			//dataType: dataType
			headers: {
				"X-CSRFToken": csrf_token
			}
		}).done(function(data) {
			//window.location = 'reports/' + data.object.id + '/view';
			//window.location = reform.urls.view.replace('0', data.object.id);
			window.location = data.url;
		}).fail(function() {
			//...
		});
		return false;
	})

};

$(reform.widgets.wizard.init);


reform.widgets.similarReports = {};
reform.widgets.similarReports.init = function() {
	var widget = reform.widgets.similarReports;
	/*
	var similarReports =
	widget.object = similarReports;
	widget.element = similarReports;
	*/

	var similar = false,
			latestReportsLabel = $('#ui-latest-reports-label'),
			similarReportsLabel = $('#ui-similar-reports-label'),
			noSimilarReportsNotification = $('#ui-no-similar-reports'),
			reportsList = $('#ui-reports-list'),
			reportsItems = reportsList.find('.ui-timeline-story');

	noSimilarReportsNotification.addClass('animated');

	window.similarReports = widget;

	widget.reportsList = reportsList;
	widget.reportsItems = reportsItems;

	widget.isSimilarToInput = function(el){
		console.log('widget', 'similarReports', 'report record', el);
		return true;
	};

	function showSimilarReports(e) {
		if(!similar) {
			latestReportsLabel.hide();
			similarReportsLabel.css({'display': 'inline-block'}).addClass('animated pulse').show();
			similar = true;
		}
		var any = false;
		reportsItems.each(function(index, el){
			el = $(el);
			el.addClass('animated');
			if(widget.isSimilarToInput(e)) {
				any = true;
				el.removeClass('fadeOutRight').addClass('fadeInRight').show();
			} else {
				el.removeClass('fadeInRight').addClass('fadeOutRight').hide();
			}
		});
		if (any){
			noSimilarReportsNotification.removeClass('fadeInUp').addClass('fadeOutDown').hide();
		} else {
			noSimilarReportsNotification.removeClass('fadeOutDown').addClass('fadeInUp').show();
		}
	}

	var datetime = reform.widgets.wizard.elements.datetime;
	datetime.on('change', showSimilarReports);

};

$(reform.widgets.similarReports.init);


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
