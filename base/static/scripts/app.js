/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';

var logger = {
	mode: 0,
	MODES: {
		DEBUG: 0
	},
	info: function(){
		if (this.mode === this.MODES.DEBUG) {
			console.log.apply(console, arguments);
		}
	},
	log: function(){
		console.log.apply(console, arguments);
	}
};

var ReformPlatform = angular.module('reformPlatform', ['ui.router', 'ui.bootstrap', 'google-maps']);

var app = ReformPlatform;

app.log = function(){
	logger.log.apply(logger, arguments);
};

app.config(function ($routeProvider) {
	$routeProvider
		.when('/', {
			templateUrl: 'views/main.html',
			controller: 'MainCtrl'
		})
		.otherwise({
			redirectTo: '/'
		});
});

app.run(function($rootScope){
	$rootScope.state = {
		showMainview: false
	};
});

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('((');
  $interpolateProvider.endSymbol('))');
});
