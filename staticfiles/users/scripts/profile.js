/* jshint strict: true, browser: true, devel: true */
/* global angular, $ */
'use strict';

$.fn.editable.defaults.mode = 'inline';
$.fn.editable.defaults.anim = 'fast';
$.fn.editable.defaults.ajaxOptions = {
	headers: {
		"X-CSRFToken": csrf_token
	}
};
$(document).ready(function() {
	$('.ui-editable').editable();
});

