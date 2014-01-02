
$(document).ready(function() {

  $.getJSON(reform.urls.statistics).done(function(statistics) {

    !(function() {

      var series = [],
        serie, dateMin, dateMax;

      serie = {
        name: 'Violations',
        color: '#c13c2d',
        data: [],
      };
      statistics.violations_by_date.forEach(function(report) {
        serie.data.push([new Date(report.date).getTime(), report.count]);
      });
      serie.data.push([new Date().getTime(), 0]);
      series.push(serie);

      dateMin = serie.data[0][0];
      dateMax = serie.data[serie.data.length - 1][0];

      serie = {
        name: 'Appreciations',
        color: '#28b262',
        data: []
      };
      statistics.appreciations_by_date.forEach(function(report) {
        serie.data.push([new Date(report.date).getTime(), report.count]);
      });
      if (!serie.data[0] || serie.data[0][0] > dateMin)
        serie.data.unshift([dateMin, 0]);
      if (!serie.data[serie.data.length - 1] || serie.data[serie.data.length - 1][0] < dateMax)
        serie.data.push([dateMax, 0]);
      series.push(serie);

      //console.log(series);

      $('#ui-reports-dates-chart').highcharts({
        chart: {
          type: 'line', //'spline',
          zoomType: 'x',
        },
        title: {
          text: 'Violations/Appreciations by date'
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
            text: 'Violations/Appreciations Number'
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

    })();

    !(function() {

      var data = statistics.violations_by_category.map(function(e) {
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

      var data = statistics.violations_by_victim_gender.map(function(e) {
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

      var data = statistics.violations_by_victim_education.map(function(e) {
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

      var features = statistics.violations_features.filter(function(e){
        return e.selectable;
      }).map(function(e){
        return e.definition;
      });

      var data = [];
      data.length = features.length;

      features.forEach(function(e, i) {
        data[i] = 0;
      });

      statistics.violations_by_feature.forEach(function(e) {
        var index = features.indexOf(e.label);
        if (index >= 0)
          data[index] = e.count;
      });

      features.unshift("All");
      data.unshift(statistics.violations_count);

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
            data: data
          }],
          credits: {
            enabled: false
          },
        });
      });

    })();

  });
});
