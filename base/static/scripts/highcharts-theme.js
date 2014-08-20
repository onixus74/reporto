/* jshint strict: true, browser: true, devel: true */
/* global reform, Highcharts */
(function() {
  'use strict';

  var theme = {
    //colors: ['#484D59', '#aaaaaa', '#4295F3'],
    //colors: ['#484D59', '#8E8DFF', '#aaaaaa', '#7270CC', '#47467F', '#53527F'],
    colors: ['#484D59', '#7270CC', '#aaaaaa', '#7276FF', '#6D6C7F'],
    plotOptions: {
      line: {
        marker: {
          enabled: true,
          lineWidth: 2,
          radius: 5,
          fillColor: '#FFFFFF',
          lineColor: null,
          symbol: 'circle',
          states: {
            hover: {
              lineWidth: 3,
              radius: 6
            }
          }
        },
      },
      bar: {
        pointWidth: 1
      },
      column: {
        pointWidth: 1
      }
    },
    chart: {
      style: {
        fontFamily: ['Droid Arabic Kufi', 'Open Sans', 'sans-serif'], //'Open Sans',
        fontWeight: 'lighter'
      }
    }
  };
  Highcharts.setOptions(theme);
})();
