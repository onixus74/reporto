/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';

angular.module('reformPlatform')

	.controller('ReportsDashboardCtrl', function($scope, $dialog) {

		$scope.reportIncident = function(){
			app.log("creating an incident");
			//$scope.state.showMainView = true;

			var d = $dialog.dialog({
				backdrop: true,
				keyboard: true,
				backdropClick: true,
				dialogFade: true,
				backdropFade: true,
				dialogClass: 'modal report-incident-dialog',
				dialogOpenClass: 'modal-open report-incident-dialog-body',
				templateUrl: 'views/report-incident.html',
				controller: 'ReportIncidentCtrl'
			});

			d.open().then(function(result){
				console.log("dialog closed", arguments);
			});

		};

	})

	.controller('ReportIncidentCtrl', function($scope, dialog) {

		$scope.message = "Hello! from ReportIncidentCtrl";

		$scope.close = function(result){
			console.log(dialog, result);
			dialog.close(result);
		};

	});
