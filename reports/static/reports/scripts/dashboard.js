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

  var incidentMarker = L.AwesomeMarkers.icon({
    icon: 'flag',
    markerColor: 'red'
  });

  var thankMarker = L.AwesomeMarkers.icon({
    icon: 'star',
    markerColor: 'green'
  });

	var markers = new L.MarkerClusterGroup();
	markers.addLayers(reform.data.incidentsLocations.map(function(loc){
		var marker = L.marker(L.latLng(loc.latitude, loc.longitude), { title: loc.category__definition, icon: incidentMarker });
		marker.bindPopup(loc.category__definition);
		return marker;
	}));
  markers.addLayers(reform.data.thanksLocations.map(function(loc){
    var marker = L.marker(L.latLng(loc.latitude, loc.longitude), { title: loc.category__definition, icon: thankMarker });
    marker.bindPopup(loc.category__definition);
    return marker;
  }));
	map.addLayer(markers);

};

$(document).ready(reform.widgets.map);


reform.widgets.geosearch = function() {};

$(document).ready(reform.widgets.geosearch);


reform.widgets.timeline = function() {

	var widget = reform.widgets.timeline;

	var list = widget.list = $('#ui-timeline-list');

	var marker;

	function bindReportItemsToMap() {
		//list.find('.ui-timeline-story').on('mouseover', function(e) {
		list.find('.ui-timeline-story-locator').on('click', function(e) {
			e.stopPropagation();
			e.preventDefault();
			console.log(marker, e.target, e.currentTarget, e.relatedTarget, e.delegateTarget);
			//var loc = $(e.target).closest('li').data('latlng').split(',');
			//loc = new L.LatLng(loc[0], loc[1]);
			var li = $(e.target).closest('li');
			var loc = new L.LatLng(li.data('latitude'), li.data('longitude'));
			/*
			if (!marker) {
				console.log(loc);
				marker = L.marker(loc);
				console.log(marker);
				marker.addTo(reform.widgets.map);
			} else {
				marker.setLatLng(loc);
			}
			*/
			reform.widgets.map.setView(loc, 12);
		});
	}

	$(bindReportItemsToMap);


	var status = reform.data.timeline;

	var paginationIndicator = widget.paginationIndicator = $('#ui-timeline-pagination-indicator');
	var paginationFirst = widget.paginationFirst = $('#ui-timeline-pagination-first');
	var paginationLast = widget.paginationLast = $('#ui-timeline-pagination-last');
	var paginationPrevious = widget.paginationPrevious = $('#ui-timeline-pagination-previous');
	var paginationNext = widget.paginationNext = $('#ui-timeline-pagination-next');

	function updatePagination() {
		paginationIndicator.html(String(status.current) + ' / ' + String(status.pages));
		paginationFirst.off('click');
		paginationLast.off('click');
		paginationPrevious.off('click');
		paginationNext.off('click');
		if (status.current == 1) {
			paginationFirst.closest('li').addClass('disabled');
			paginationFirst.on('click', function(e) {
				e.stopPropagation();
				e.preventDefault();
			});
			paginationPrevious.closest('li').addClass('disabled');
			paginationPrevious.on('click', function(e) {
				e.stopPropagation();
				e.preventDefault();
			});
		} else {
			paginationFirst.closest('li').removeClass('disabled');
			paginationFirst.on('click', function(e) {
				e.stopPropagation();
				e.preventDefault();
				showPage(1);
			});
			paginationPrevious.closest('li').removeClass('disabled');
			paginationPrevious.on('click', function(e) {
				e.stopPropagation();
				e.preventDefault();
				showPage(status.current - 1);
			});
		}
		if (status.current == status.pages) {
			paginationNext.closest('li').addClass('disabled');
			paginationNext.on('click', function(e) {
				e.stopPropagation();
				e.preventDefault();
			});
			paginationLast.closest('li').addClass('disabled');
			paginationLast.on('click', function(e) {
				e.stopPropagation();
				e.preventDefault();
			});
		} else {
			paginationNext.closest('li').removeClass('disabled');
			paginationNext.on('click', function(e) {
				e.stopPropagation();
				e.preventDefault();
				showPage(status.current + 1);
			});
			paginationLast.closest('li').removeClass('disabled');
			paginationLast.on('click', function(e) {
				e.stopPropagation();
				e.preventDefault();
				showPage('last');
			});
		}
	}
	$(updatePagination);

	function showPage(page) {
		$.get('/reports/dashboard.json?page=' + page).done(function(data) {
			console.log(arguments, status);
			status.current = data.current;
			list.html(data.html);
		})
			.done(updatePagination)
			.done(function() {
				list.unblock();
			})
			.done(bindReportItemsToMap);
		//list.html('<li>Loading ...</li>');
		list.block({
			message: 'Loading ...',
			//css: { border: '3px solid #a00' }
		});
	}

	widget.showPage = showPage;

};

$(document).ready(reform.widgets.timeline);

/*
reform.widgets.stats = function() {

	var dates = reform.data.incidentsByDate.map(function(o) {
		return (new Date(o.date)).getTime()
	})
	var minDate = new Date(Math.min.apply(Math, dates)),
		maxDate = new Date(Math.max.apply(Math, dates));

	var ONE_DAY = 86400000;

	var diff = (maxDate.getTime() - minDate.getTime()) / ONE_DAY;

	var xLabel = "day";

	if (diff > 732) { // 2 * 366
		var xLabel = "year";
	} else if (diff > 62) { // 2 * 31
		var xLabel = "month";
	} else {
		var xLabel = "day";
	}



	new Morris.Line({
		element: 'ui-reports-dates-chart',
		data: reform.data.incidentsByDate,
		xkey: 'date',
		//ykeys: ['total'].concat(reform.data.categories),
		//labels: ['Total Reports'].concat(reform.data.categories),
		ykeys: ['total'],
		labels: ['Total Reports'],
		xLabelFormat: function(x) {
			return x.toLocaleDateString();
		},
		xLabels: xLabel,
		//yLabelFormat: function (y) { return y.toString(); },
		dateFormat: function(x) {
			return new Date(x).toLocaleDateString();
		},
		smooth: false
	});

	new Morris.Bar({
		element: 'ui-stats-features-chart',
		data: reform.data.incidentsByFeature,
		//formatter: function(y, data){ return String(y) + ' (' + String((y / reform.data.incidentsByCategory.length).toFixed(2)) + '%)' }
		xkey: 'label',
		ykeys: ['count'],
		labels: ['Feature'],
		//xLabelFormat: function (x) { return 'F1'; },
		//yLabelFormat: function (y) { return y.toString(); },
		yLabelFormat: function(y) {
			return String(y) + ' (' + String((y * 100 / reform.data.timeline.count).toFixed(2)) + '%)'
		}
	});

	new Morris.Donut({
		element: 'ui-stats-categories-chart',
		data: reform.data.incidentsByCategory,
		//colors: ['#F00', '#0F0', '#00F']
		formatter: function(y) {
			return String(y) + ' (' + String((y * 100 / reform.data.timeline.count).toFixed(2)) + '%)'
		}
		//colors: ['#F00', '#0F0', '#00F']
	});

	new Morris.Donut({
		element: 'ui-stats-victim-gender-chart',
		data: reform.data.incidentsByVictimGender,
		//colors: ['#F00', '#0F0', '#00F']
		formatter: function(y, data) {
			return String(y) + ' (' + String((y * 100 / reform.data.timeline.count).toFixed(2)) + '%)'
		}
	});

	new Morris.Donut({
		element: 'ui-stats-victim-education-chart',
		data: reform.data.incidentsByVictimEducation,
		//colors: ['#F00', '#0F0', '#00F']
		formatter: function(y, data) {
			return String(y) + ' (' + String((y * 100 / reform.data.timeline.count).toFixed(2)) + '%)'
		}
	});
};

$(document).ready(reform.widgets.stats);
*/

!(function() {

	var series = [], serie, dateMin, dateMax;

	serie = {
		name: 'Incidents',
    color: '#c13c2d',
		data: [],
	};
	reform.data.incidentsByDate.forEach(function(report) {
		serie.data.push([new Date(report.date).getTime(), report.count]);
	});
	serie.data.push([new Date().getTime(), 0]);
	series.push(serie);

  dateMin = serie.data[0][0];
  dateMax = serie.data[serie.data.length - 1][0];

  serie = {
    name: 'Thanks',
    color: '#28b262',
    data: []
  };
  reform.data.thanksByDate.forEach(function(report) {
    serie.data.push([new Date(report.date).getTime(), report.count]);
  });
  if (!serie.data[0] || serie.data[0][0] > dateMin)
    serie.data.unshift([dateMin, 0]);
  if (!serie.data[serie.data.length - 1] || serie.data[serie.data.length - 1][0] < dateMax)
    serie.data.push([dateMax, 0]);
  series.push(serie);

	/*Object.keys(reform.data.incidentsByCategoryByDate).forEach(function(category) {
		var serie = {
			name: category,
			data: []
		};
		reform.data.incidentsByCategoryByDate[category].forEach(function(report) {
			serie.data.push([new Date(report.date).getTime(), report.count]);
		});
		if (!serie.data[0] || serie.data[0][0] > dateMin)
			serie.data.unshift([dateMin, 0]);
		if (!serie.data[serie.data.length - 1] || serie.data[serie.data.length - 1][0] < dateMax)
			serie.data.push([dateMax, 0]);
		series.push(serie);
	});*/

	$(document).ready(function() {
		console.log(series);

		$('#ui-reports-dates-chart').highcharts({
			chart: {
				type: 'line', //'spline',
				zoomType: 'x',
			},
			title: {
				text: 'Incidents/Thanks by date'
			},
			subtitle: {
				text: document.ontouchstart === undefined ?
					'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in',
			},
			xAxis: {
				type: 'datetime',
				dateTimeLabelFormats: { // don't display the dummy year
					month: '%e. %b',
					year: '%b'
				}
			},
			yAxis: {
				title: {
					text: 'Incidents/Thanks Number'
				},
				min: 0
			},
			tooltip: {
				formatter: function() {
					return '<b>' + this.series.name + '</b><br/>' +
						Highcharts.dateFormat('%e. %b', this.x) + ': ' + this.y + ' incidents';
				}
			},
			series: series,
			credits: {
				enabled: false
			}
		});
	});
})();



!(function() {

	var data = reform.data.incidentsByCategory.map(function(e) {
		return [e.label, e.count]
	});

	$(document).ready(function() {
		$('#ui-stats-categories-chart').highcharts({
			chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false
			},
			title: {
				text: 'Distribution by incident category'
			},
			tooltip: {
				pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
			},
			plotOptions: {
				pie: {
					//allowPointSelect: true,
					cursor: 'pointer',
					dataLabels: {
						enabled: true,
						color: '#000000',
						connectorColor: '#000000',
						format: '<b>{point.name}</b>: {point.percentage:.1f} %'
					}
				}
			},
			series: [{
				type: 'pie',
				name: 'Category share',
				data: data
			}],
			credits: {
				enabled: false
			},
		});
	});

})();



!(function() {

	var data = reform.data.incidentsByVictimGender.map(function(e) {
		return [e.label, e.count]
	});

	$(document).ready(function() {
		$('#ui-stats-victim-gender-chart').highcharts({
			chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false
			},
			title: {
				text: 'Distribution by victim\'s gender'
			},
			tooltip: {
				pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
			},
			plotOptions: {
				pie: {
					//allowPointSelect: true,
					cursor: 'pointer',
					dataLabels: {
						enabled: true,
						color: '#000000',
						connectorColor: '#000000',
						format: '<b>{point.name}</b>: {point.percentage:.1f} %'
					}
				}
			},
			series: [{
				type: 'pie',
				name: 'Victim\'s gender share',
				data: data
			}],
			credits: {
				enabled: false
			},
		});
	});

})();


!(function() {

	var data = reform.data.incidentsByVictimEducation.map(function(e) {
		return [e.label, e.count]
	});

	$(document).ready(function() {
		$('#ui-stats-victim-education-chart').highcharts({
			chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false
			},
			title: {
				text: 'Distribution by victim\'s education'
			},
			tooltip: {
				pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
			},
			plotOptions: {
				pie: {
					//allowPointSelect: true,
					cursor: 'pointer',
					dataLabels: {
						enabled: true,
						color: '#000000',
						connectorColor: '#000000',
						format: '<b>{point.name}</b>: {point.percentage:.1f} %'
					}
				}
			},
			series: [{
				type: 'pie',
				name: 'Victim\'s educqtion share',
				data: data
			}],
			credits: {
				enabled: false
			},
		});
	});

})();


!(function() {

	var features = reform.data.features.slice(0);

	var data = [];
	data.length = features.length;

	features.forEach(function(e, i) {
		data[i] = 0;
	});

	reform.data.incidentsByFeature.forEach(function(e) {
		var index = features.indexOf(e.label);
		if (index >= 0)
			data[index] = e.count;
	});

	features.unshift("All");
	data.unshift(reform.data.timeline.count);

	$(document).ready(function() {
		$('#ui-stats-features-chart').highcharts({
			chart: {
				type: 'bar'
			},
			title: {
				text: 'Incidents by Features'
			},
			legend: {
				enabled: false
			},
			xAxis: {
				categories: features,
				title: {
					text: null
				}
			},
			yAxis: {
				min: 0,
				title: {
					text: 'Number of Incidents',
					align: 'high'
				},
				labels: {
					overflow: 'justify'
				}
			},
			tooltip: {
				valueSuffix: ' incidents'
			},
			plotOptions: {
				bar: {
					dataLabels: {
						enabled: true
					}
				}
			},
			series: [{
				/* name: 'Year 1800', */
				data: data
			}],
			credits: {
				enabled: false
			},
		});
	});


})();
