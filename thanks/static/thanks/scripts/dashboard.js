/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';

if (!reform) {
  window.reform = {
    data: {},
    urls: {},
    widgets: {}
  };
}

reform.widgets.map = function() {

  // create a map in the "map" div, set the view to a given place and zoom
  var map = reform.widgets.map = L.map('ui-timeline-map')

  map.setView([34.161818161230386, 9.3603515625], 5);

  map.setMaxBounds(map.getBounds());

  // add an OpenStreetMap tile layer
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

  var thankMarker = L.AwesomeMarkers.icon({
    icon: 'star',
    markerColor: 'green'
  });

  var markers = new L.MarkerClusterGroup();
  markers.addLayers(reform.data.thanksLocations.map(function(loc) {
    var marker = L.marker(L.latLng(loc.latitude, loc.longitude), {
      title: loc.category__definition,
      icon: thankMarker
    });
    marker.bindPopup('<a href="' + reform.urls.thankView.replace('0', loc.pk) + '" target="_blank">' + loc.category__definition + '</a>');
    return marker;
  }));
  map.addLayer(markers);

};

$(document).ready(reform.widgets.map);


reform.widgets.geosearch = function() {};

$(document).ready(reform.widgets.geosearch);


$(document).ready(function(){
  reform.widgets.pagination('#ui-timeline-list', reform.data.timeline, reform.urls.thanksDashboard)
});


!(function() {

  var series = [], serie;

  serie = {
    name: 'Thanks',
    color: '#28b262',
    data: []
  };
  reform.data.thanksByDate.forEach(function(report) {
    serie.data.push([new Date(report.date).getTime(), report.count]);
  });
  serie.data.push([new Date().getTime(), 0]);
  series.push(serie);

  $(document).ready(function() {
    console.log(series);

    $('#ui-reports-dates-chart').highcharts({
      chart: {
        type: 'line', //'spline',
        zoomType: 'x',
      },
      title: {
        text: 'Thanks by date'
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
          text: 'Thanks Number'
        },
        min: 0
      },
      tooltip: {
        formatter: function() {
          return '<b>' + this.series.name + '</b><br/>' +
            Highcharts.dateFormat('%e. %b', this.x) + ': ' + this.y + ' thanks';
        }
      },
      series: series,
      credits: {
        enabled: false
      }
    });
  });
})();
