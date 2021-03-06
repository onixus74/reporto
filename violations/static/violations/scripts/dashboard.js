/* jshint strict: true, browser: true, devel: true */
/* global $, L, Dropzone, reform */
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

  map.scrollWheelZoom.disable();

  // add an OpenStreetMap tile layer
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

  var violationMarker = L.AwesomeMarkers.icon({
    icon: 'flag',
    markerColor: 'red'
  });

  var markers = new L.MarkerClusterGroup();
  markers.addLayers(reform.data.violationsLocations.map(function(loc) {
    var marker = L.marker(L.latLng(loc.latitude, loc.longitude), {
      title: loc['category__definition_' + reform.i18n.language],
      icon: violationMarker
    });
    marker.bindPopup('<a href="' + reform.urls.violationView.replace('0', loc.pk) + '" target="_blank">' + loc['category__definition_' + reform.i18n.language] + '</a>');
    return marker;
  }));
  map.addLayer(markers);

};

$(document).ready(reform.widgets.map);


reform.widgets.geosearch = function() {};

$(document).ready(reform.widgets.geosearch);


$(document).ready(function(){
  reform.widgets.paginate('#ui-timeline-list', reform.data.timeline, reform.urls.violationsDashboard)
});


!(function() {

  var series = [], serie;

  serie = {
    name: 'Violations',
    color: '#c13c2d',
    data: [],
  };
  reform.data.violationsByDate.forEach(function(violation) {
    serie.data.push([new Date(violation.date).getTime(), violation.count]);
  });
  serie.data.push([new Date().getTime(), 0]);
  series.push(serie);

  /*Object.keys(reform.data.violationsByCategoryByDate).forEach(function(category) {
    var serie = {
      name: category,
      data: []
    };
    reform.data.violationsByCategoryByDate[category].forEach(function(violation) {
      serie.data.push([new Date(violation.date).getTime(), violation.count]);
    });
    if (!serie.data[0] || serie.data[0][0] > dateMin)
      serie.data.unshift([dateMin, 0]);
    if (!serie.data[serie.data.length - 1] || serie.data[serie.data.length - 1][0] < dateMax)
      serie.data.push([dateMax, 0]);
    series.push(serie);
  });*/

  $(document).ready(function() {
    console.log(series);

    $('#ui-violations-dates-chart').highcharts({
      chart: {
        type: 'line', //'spline',
        zoomType: 'x',
      },
      title: {
        text: 'Violations by date'
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
          text: 'Violations Number'
        },
        min: 0
      },
      tooltip: {
        formatter: function() {
          return '<b>' + this.series.name + '</b><br/>' +
            Highcharts.dateFormat('%e. %b', this.x) + ': ' + this.y + ' violations';
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

  var data = reform.data.violationsByCategory.map(function(e) {
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
        text: 'Distribution by violation category'
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

  var data = reform.data.violationsByVictimGender.map(function(e) {
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

  var data = reform.data.violationsByVictimEducation.map(function(e) {
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

  var features = reform.data.violationsFeatures.filter(function(e){
    return e.selectable;
  }).map(function(e){
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
  data.unshift(reform.data.timeline.count);

  $(document).ready(function() {
    $('#ui-stats-features-chart').highcharts({
      chart: {
        type: 'bar'
      },
      title: {
        text: 'Violations by Features'
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
          text: 'Number of Violations',
          align: 'high'
        },
        labels: {
          overflow: 'justify'
        }
      },
      tooltip: {
        valueSuffix: ' violations'
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
