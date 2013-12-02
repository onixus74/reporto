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
    $.get(reform.urls.thankDashboard + '.json?page=' + page).done(function(data) {
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
