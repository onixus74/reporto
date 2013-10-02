/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';

reform.widgets.map = function() {

	// create a map in the "map" div, set the view to a given place and zoom
	var map = reform.widgets.map = L.map('ui-timeline-map')

	map.setView([34.161818161230386, 9.3603515625], 5);

	map.setMaxBounds(map.getBounds());

	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

};

$(document).ready(reform.widgets.map);


reform.widgets.geosearch = function() {};

$(document).ready(reform.widgets.geosearch);


reform.widgets.timeline = function() {

	var widget = reform.widgets.timeline;

	var marker;
	$('.ui-timeline-story').on('mouseover', function(e) {
		e.stopPropagation();
		e.preventDefault();
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


	var status = reform.data.timeline;

	var list = widget.list = $('#ui-timeline-list');

	var paginationIndicator = widget.paginationIndicator = $('#ui-timeline-pagination-indicator');
	var paginationFirst = widget.paginationFirst = $('#ui-timeline-pagination-first');
	var paginationLast = widget.paginationLast = $('#ui-timeline-pagination-last');
	var paginationPrevious = widget.paginationPrevious = $('#ui-timeline-pagination-previous');
	var paginationNext = widget.paginationNext = $('#ui-timeline-pagination-next');

	function updatePagination() {
		paginationIndicator.html( String(status.current) + ' / ' + String(status.pages) );
		paginationFirst.off('click');
		paginationLast.off('click');
		paginationPrevious.off('click');
		paginationNext.off('click');
		if (status.current == 1) {
			paginationFirst.closest('li').addClass('disabled');
			paginationPrevious.closest('li').addClass('disabled');
		} else {
			paginationFirst.closest('li').removeClass('disabled');
			paginationFirst.on('click', function(e){
				e.stopPropagation();
				e.preventDefault();
				showPage(1);
			});
			paginationPrevious.closest('li').removeClass('disabled');
			paginationPrevious.on('click', function(e){
				e.stopPropagation();
				e.preventDefault();
				showPage(status.current - 1);
			});
		}
		if (status.current == status.pages) {
			paginationNext.closest('li').addClass('disabled');
			paginationLast.closest('li').addClass('disabled');
		} else {
			paginationNext.closest('li').removeClass('disabled');
			paginationNext.on('click', function(e){
				e.stopPropagation();
				e.preventDefault();
				showPage(status.current + 1);
			});
			paginationLast.closest('li').removeClass('disabled');
			paginationLast.on('click', function(e){
				e.stopPropagation();
				e.preventDefault();
				showPage('last');
			});
		}
	}
	updatePagination();

	function showPage(page){
		$.get('/reports/dashboard.json?page=' + page).done(function(data){
			console.log(arguments, status);
			status.current = data.current;
			list.html(data.html);
		}).done(updatePagination);
		list.html('<li>Loading ...</li>');
	}

	widget.showPage = showPage;

}

$(document).ready(reform.widgets.timeline);


reform.widgets.stats = function() {

	new Morris.Donut({
		element: 'ui-stats-categories-chart',
		data: reform.data.reportsByCategory,
		/*
		formatter: function(y, data){
			console.log(y, data, reform.data.reportsByCategory)
			return String(y) + ' (' + String((y / reform.data.reportsByCategory.length).toFixed(2)) + '%)'
			//return y;
		}
		*/
	});

	new Morris.Bar({
		element: 'ui-stats-features-chart',
		data: reform.data.reportsByFeature,
		//formatter: function(y, data){ return String(y) + ' (' + String((y / reform.data.reportsByCategory.length).toFixed(2)) + '%)' }
		xkey: 'label',
	  ykeys: ['value'],
	  labels: ['Feature'],
		//xLabelFormat: function (x) { return 'F1'; },
		//yLabelFormat: function (y) { return y.toString(); },
	});

	new Morris.Donut({
		element: 'ui-stats-victim-gender-chart',
		data: reform.data.reportsByVictimGender,
	});

	new Morris.Line({
		element: 'ui-reports-dates-chart',
		data: reform.data.reportsByDate,
		/*
		data: [
			{ date: '2006', reports: 100, b: 90 },
			{ date: '2007', reports: 75,  b: 65 },
			{ date: '2008', reports: 50,  b: 40 },
			{ date: '2009', reports: 75,  b: 65 },
			{ date: '2010', reports: 50,  b: 40 },
			{ date: '2011', reports: 75,  b: 65 },
			{ date: '2012', reports: 100, b: 90 }
		],
		*/
		xkey: 'date',
		ykeys: ['reports'],
		labels: ['Reports'],
		xLabelFormat: function (x) { return x.toLocaleDateString(); },
		//yLabelFormat: function (y) { return y.toString(); },
		dateFormat: function (x) { return new Date(x).toLocaleDateString(); },
	});
};

$(document).ready(reform.widgets.stats);
