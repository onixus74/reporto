/* jshint strict: true, browser: true, devel: true */
/* global reform, Highcharts, gettext */
(function() {
  'use strict';

  var i18n = {
    lang: {
      loading: gettext("Loading..."),
      months: [
        gettext("January"),
        gettext("February"),
        gettext("March"),
        gettext("April"),
        gettext("May"),
        gettext("June"),
        gettext("July"),
        gettext("August"),
        gettext("September"),
        gettext("October"),
        gettext("November"),
        gettext("December")
      ],
      shortMonths: [
        gettext("Jan"),
        gettext("Feb"),
        gettext("Mar"),
        gettext("Apr"),
        gettext("May"),
        gettext("Jun"),
        gettext("Jul"),
        gettext("Aug"),
        gettext("Sep"),
        gettext("Oct"),
        gettext("Nov"),
        gettext("Dec")
      ],
      weekdays: [
        gettext("Sunday"),
        gettext("Monday"),
        gettext("Tuesday"),
        gettext("Wednesday"),
        gettext("Thursday"),
        gettext("Friday"),
        gettext("Saturday")
      ],
      decimalPoint: '.',
      numericSymbols: ['k', 'M', 'G', 'T', 'P', 'E'], // SI prefixes used in axis labels
      resetZoom: gettext("Reset zoom"),
      resetZoomTitle: gettext("Reset zoom level 1:1"),
      thousandsSep: gettext(","),
      printChart: gettext("Print chart"),
      downloadPNG: gettext("Download PNG image"),
      downloadJPEG: gettext("Download JPEG image"),
      downloadPDF: gettext("Download PDF document"),
      downloadSVG: gettext("Download SVG vector image"),
      contextButtonTitle: gettext("Chart context menu")
    }
  };

  Highcharts.setOptions(i18n);
})();