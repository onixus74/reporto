/* jshint strict: true, browser: true, devel: true */
/* global $, reform, L, Highcharts */
(function() {
  'use strict';

  if (!reform) {
    window.reform = {
      data: {},
      widgets: {},
      urls: {},
      i18n: {},
      l10n: {},
    };
  }

  reform.widgets.charts = {};

  reform.widgets.charts.reportsByDate = function() {

    var series = [],
      serie, dateMin, dateMax;

    serie = {
      name: gettext("Violations"),
      color: '#c13c2d',
      data: [],
    };
    reform.data.violationsByDate.forEach(function(violation) {
      serie.data.push([new Date(violation.date).getTime(), violation.count]);
    });
    serie.data.push([new Date().getTime(), 0]);
    series.push(serie);

    dateMin = serie.data[0][0];
    dateMax = serie.data[serie.data.length - 1][0];

    serie = {
      name: gettext("Appreciations"),
      color: '#28b262',
      data: []
    };
    reform.data.appreciationsByDate.forEach(function(violation) {
      serie.data.push([new Date(violation.date).getTime(), violation.count]);
    });
    if (!serie.data[0] || serie.data[0][0] > dateMin)
      serie.data.unshift([dateMin, 0]);
    if (!serie.data[serie.data.length - 1] || serie.data[serie.data.length - 1][0] < dateMax)
      serie.data.push([dateMax, 0]);
    series.push(serie);

    $(document).ready(function() {
      //console.log(series);
      $('#ui-stats-reports-by-date-chart').highcharts({
        chart: {
          type: 'line', //'spline',
          zoomType: 'x',
        },
        title: {
          text: gettext("Violations/Appreciations by date")
        },
        subtitle: {
          text: Modernizr.touch ? gettext("Click and drag in the plot area to zoom in") : gettext("Pinch the chart to zoom in"), // document.ontouchstart === undefined
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
            text: gettext("Number of Violations/Appreciations")
          },
          min: 0
        },
        tooltip: {
          formatter: function() {
            /*
            return '<b>' + this.series.name + '</b><br/>' +
              Highcharts.dateFormat('%e. %b', this.x) + ': ' + this.y + ' ' + gettext("violations/appreciations");
            */
            return this.series.name + ': <b>' + this.y + '</b> ' + gettext("reports on") + ' <b>' + moment(this.x).format('LL') + '</b>';
          }
        },
        series: series,
        credits: {
          enabled: false
        }
      });

    });
  };


  reform.widgets.charts.violationsByFeatures = function() {

    var features = reform.data.violationsFeatures.filter(function(e) {
      return e.selectable;
    }).map(function(e) {
      return e.definition;
    });

    var data = [];
    data.length = features.length;

    features.forEach(function(e, i) {
      data[i] = 0;
    });

    reform.data.violationsByFeature.forEach(function(e) {
      var index = features.indexOf(e.label);
      if (index >= 0)
        data[index] = e.count;
    });

    features.unshift("All");
    data.unshift(reform.data.violationsCount);

    $(document).ready(function() {
      $('#ui-stats-violations-by-features-chart').highcharts({
        chart: {
          type: 'bar'
        },
        title: {
          text: gettext("Violations by Features")
        },
        legend: {
          enabled: false,
          rtl: reform.i18n.bidi
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
            text: gettext("Number of Violations"),
            align: 'high'
          },
          labels: {
            overflow: 'justify'
          }
        },
        tooltip: {
          valueSuffix: gettext(" violations")
        },
        plotOptions: {
          bar: {
            dataLabels: {
              enabled: true
            }
          }
        },
        series: [{
          name: gettext("Number of Violations"),
          data: data
        }],
        credits: {
          enabled: false
        },
      });
    });


  };


  reform.widgets.charts.violationsByCategory = function() {

    var data = reform.data.violationsByCategory.map(function(e) {
      return [e.label, e.count]
    });

    $(document).ready(function() {
      $('#ui-stats-violations-by-category-chart').highcharts({
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false
        },
        title: {
          text: gettext("Violation by Category")
        },
        tooltip: {
          pointFormat: '{series.name}: {point.percentage:.1f}%'
        },
        plotOptions: {
          pie: {
            //allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: false,
              color: '#000000',
              connectorColor: '#000000',
              format: '{point.name}: {point.percentage:.1f}%'
            },
            showInLegend: true
          }
        },
        series: [{
          type: 'pie',
          name: gettext("Victim's category share"),
          data: data
        }],
        credits: {
          enabled: false
        },
      });
    });

  };


  reform.widgets.charts.violationsByVictimGender = function() {

    var data = reform.data.violationsByVictimGender.map(function(e) {
      return [e.label, e.count]
    });

    $(document).ready(function() {
      $('#ui-stats-violations-by-victim-gender-chart').highcharts({
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false
        },
        title: {
          text: gettext("Violation by Victim's Gender")
        },
        tooltip: {
          pointFormat: '{series.name}: {point.percentage:.1f}%'
        },
        plotOptions: {
          pie: {
            //allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: false,
              color: '#000000',
              connectorColor: '#000000',
              format: '{point.name}: {point.percentage:.1f}%'
            },
            showInLegend: true
          }
        },
        series: [{
          type: 'pie',
          name: gettext("Victim's gender share"),
          data: data
        }],
        credits: {
          enabled: false
        },
      });
    });

  };

  reform.widgets.charts.violationsByVictimEducation = function() {

    var data = reform.data.violationsByVictimEducation.map(function(e) {
      return [e.label, e.count]
    });

    $(document).ready(function() {
      $('#ui-stats-violations-by-victim-education-chart').highcharts({
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false
        },
        title: {
          text: gettext("Violations by Victim's Education")
        },
        tooltip: {
          pointFormat: '{series.name}: {point.percentage:.1f}%'
        },
        plotOptions: {
          pie: {
            //allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: false,
              color: '#000000',
              connectorColor: '#000000',
              format: '{point.name}: {point.percentage:.1f}%'
            },
            showInLegend: true
          }
        },
        series: [{
          type: 'pie',
          name: gettext("Victim's education share"),
          data: data
        }],
        credits: {
          enabled: false
        },
      });
    });

  };


  reform.widgets.charts.appreciationByCategory = function() {

    var data = reform.data.appreciationsByCategory.map(function(e) {
      return [e.label, e.count]
    });

    $(document).ready(function() {
      $('#ui-stats-appreciations-by-category-chart').highcharts({
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false
        },
        title: {
          text: gettext("Appreciations by Category")
        },
        tooltip: {
          pointFormat: '{series.name}: {point.percentage:.1f}%'
        },
        plotOptions: {
          pie: {
            //allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: false,
              color: '#000000',
              connectorColor: '#000000',
              format: '{point.name}: {point.percentage:.1f}%'
            },
            showInLegend: true
          }
        },
        series: [{
          type: 'pie',
          name: gettext("Appreciation's category share"),
          data: data
        }],
        credits: {
          enabled: false
        },
      });
    });

  };

})();
