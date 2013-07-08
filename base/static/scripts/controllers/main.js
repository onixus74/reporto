/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';

angular.module('reformPlatform')
  .controller('MainCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
