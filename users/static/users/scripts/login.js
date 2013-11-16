$(document).ready(function() {

	$.getJSON(reform.urls.statistics).done(function(statistics) {

		console.log(statistics);

		!(function() {

			var reports_by_category_by_date = statistics.reports_by_category_by_date;

			var series = [];

			var serie = {
				name: 'All Incidents',
				data: [],
				lineWidth: 4,
			};

			statistics.reports_by_date.forEach(function(report) {
				serie.data.push([new Date(report.date).getTime(), report.count]);
			});
			serie.data.push([new Date().getTime(), 0]);
			series.push(serie);

			var dateMin = serie.data[0][0],
				dateMax = serie.data[serie.data.length - 1][0];

			Object.keys(reports_by_category_by_date).forEach(function(category) {
				var serie = {
					name: category,
					data: []
				};
				reports_by_category_by_date[category].forEach(function(report) {
					serie.data.push([new Date(report.date).getTime(), report.count]);
				});
				if (!serie.data[0] || serie.data[0][0] != dateMin)
					serie.data.unshift([dateMin, 0]);
				if (!serie.data[serie.data.length - 1] || serie.data[serie.data.length - 1][0] != dateMax)
					serie.data.push([dateMax, 0]);
				series.push(serie);
			});

			console.log(series);

			$('#ui-reports-dates-chart-highcharts').highcharts({
				chart: {
					type: 'line', //'spline',
					zoomType: 'x',
				},
				title: {
					text: 'Incidents by date'
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
						text: 'Incidents Number'
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

		})();

		!(function() {

			var data = statistics.reports_by_category.map(function(e) {
				return [e.label, e.count]
			});

			$(document).ready(function() {
				$('#ui-stats-categories-chart-highcharts').highcharts({
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

			var data = statistics.reports_by_victim_gender.map(function(e) {
				return [e.label, e.count]
			});

			$(document).ready(function() {
				$('#ui-stats-victim-gender-chart-highcharts').highcharts({
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

			var data = statistics.reports_by_victim_education.map(function(e) {
				return [e.label, e.count]
			});

			$(document).ready(function() {
				$('#ui-stats-victim-education-chart-highcharts').highcharts({
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

			var features = statistics.features.slice(0);

			var data = [];
			data.length = features.length;

			features.forEach(function(e, i) {
				data[i] = 0;
			});

			statistics.reports_by_feature.forEach(function(e) {
				var index = features.indexOf(e.label);
				if (index >= 0)
					data[index] = e.count;
			});

			features.unshift("All");
			data.unshift(statistics.reports_count);

			$(document).ready(function() {
				$('#ui-stats-features-chart-highcharts').highcharts({
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
