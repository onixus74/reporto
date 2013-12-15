/* jshint strict: true, browser: true, devel: true */
/* global angular, $, L, Dropzone, reform */
'use strict';

if (!reform) {
  window.reform = {
    data: {},
    urls: {},
    widgets: {}
  };
}

reform.widgets.map = {};
reform.widgets.map.init = function() {

  var widget = reform.widgets.map;

  var map = widget.object = L.map('map', {
    center: new L.LatLng(reform.data.thank.latitude, reform.data.thank.longitude),
    zoom: 8
  });

  // add an OpenStreetMap tile layer
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

  L.marker([reform.data.thank.latitude, reform.data.thank.longitude]).addTo(map);

  L.control.scale().addTo(map);

  //map.setMaxBounds(map.getBounds());

  map.scrollWheelZoom.disable();

}

$(document).ready(reform.widgets.map.init);
