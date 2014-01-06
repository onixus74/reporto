/* jshint strict: true, browser: true, devel: true */
/* global $, reform, L, Highcharts */
(function() {
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
    var map = reform.widgets.map = L.map('ui-timeline-map');

    map.setView([34.161818161230386, 9.3603515625], 5);

    map.setMaxBounds(map.getBounds());

    map.scrollWheelZoom.disable();

    // add an OpenStreetMap tile layer
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

    var violationMarker = L.AwesomeMarkers.icon({
      icon: 'flag',
      markerColor: 'red'
    });

    var appreciationMarker = L.AwesomeMarkers.icon({
      icon: 'star',
      markerColor: 'green'
    });

    var markers = new L.MarkerClusterGroup();
    markers.addLayers(reform.data.violationsLocations.map(function(loc) {
      var marker = L.marker(L.latLng(loc.latitude, loc.longitude), {
        title: loc.category__definition,
        icon: violationMarker
      });
      marker.bindPopup('<a href="' + reform.urls.violationView.replace('0', loc.pk) + '" target="_blank">' + loc.category__definition + '</a>');
      return marker;
    }));
    markers.addLayers(reform.data.appreciationsLocations.map(function(loc) {
      var marker = L.marker(L.latLng(loc.latitude, loc.longitude), {
        title: loc.category__definition,
        icon: appreciationMarker
      });
      marker.bindPopup('<a href="' + reform.urls.appreciationView.replace('0', loc.pk) + '" target="_blank">' + loc.category__definition + '</a>');
      return marker;
    }));
    map.addLayer(markers);

  };


  reform.widgets.geosearch = function() {};


  reform.widgets.paginators = function() {

    function updateMarkers(list) {

      list.find('.ui-timeline-story-locator').on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        //console.log(marker, e.target, e.currentTarget, e.relatedTarget, e.delegateTarget);
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
        reform.widgets.map.setView(loc, 20);
        $.scrollTo(reform.widgets.map._container, 500, {
          axis: 'y',
          offset: {
            top: -100
          }
        });
      });


      list.tooltip({
        selector: '[data-toggle=tooltip]',
        container: 'body'
      });

    }

    function updateReportLinks(list, modal) {

      list.find('.ui-timeline-story-link').on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        var target = $(e.target).closest('a');
        var url = target.attr('href');
        modal.find('.modal-footer .ui-more').attr('href', url);
        $.get(url + '/partial').done(function(html) {
          modal.find('.modal-body').html(html);
          modal.modal('show');
        });

      });

    }

    function ListUpdateHandlerFactory($list, $modal) {
      return function(status, url) {
        reform.widgets.paginate($list, status, url, function(list) {
          updateMarkers(list);
          updateReportLinks(list, $modal);
        });
      };
    }

    function ListResetHandlerFactory($list, updateHandler, url) {
      return function() {
        $list.block();
        $.getJSON(url + '.json').done(function(response) {
          console.log(response);
          $list.html(response.html);
          updateHandler(response, url);
          $list.unblock();
        });
      };
    }

    var $violationsTimeline = $('#ui-violations-timeline-list');
    var $violationsList = $violationsTimeline.find('.ui-list');

    var violationsUpdateHandler = ListUpdateHandlerFactory($violationsList, $('#ui-violation-view-modal'));
    var violationsResetHandler = ListResetHandlerFactory($violationsList, violationsUpdateHandler, reform.urls.violationsDashboard);
    violationsUpdateHandler(reform.data.violationsPagination, reform.urls.violationsDashboard);
    reform.widgets.paginateSearch($violationsTimeline, reform.urls.violationsSearch, violationsUpdateHandler, violationsResetHandler);

    var $appreciationsTimeline = $('#ui-appreciations-timeline-list');
    var $appreciationsList = $appreciationsTimeline.find('.ui-list');

    var appreciationsUpdateHandler = ListUpdateHandlerFactory($appreciationsList, $('#ui-appreciation-view-modal'));
    var appreciationsResetHandler = ListResetHandlerFactory($appreciationsList, appreciationsUpdateHandler, reform.urls.appreciationsDashboard);
    appreciationsUpdateHandler(reform.data.appreciationsPagination, reform.urls.appreciationsDashboard);
    reform.widgets.paginateSearch($appreciationsTimeline, reform.urls.appreciationsSearch, appreciationsUpdateHandler, appreciationsResetHandler);

  }

  function main() {
    $(document).ready(reform.widgets.map);
    //$(document).ready(reform.widgets.geosearch);
    $(document).ready(reform.widgets.paginators);
    $(document).ready(reform.widgets.search);
    reform.widgets.charts.reportsByDate();
    reform.widgets.charts.violationsByCategory();
    reform.widgets.charts.violationsByVictimGender();
    reform.widgets.charts.violationsByVictimEducation();
    reform.widgets.charts.violationsByFeatures();
    reform.widgets.charts.appreciationByCategory();
  }

  main();
})();
