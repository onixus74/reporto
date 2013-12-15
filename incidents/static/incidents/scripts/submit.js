/* jshint strict: true, browser: true, devel: true */
/* global angular, $, L, Dropzone, reform */
'use strict';

if (!reform) {
  window.reform = {
    data: {},
    urls: {},
    widgets: {}
  };
}

reform.widgets.map = {};
reform.widgets.map.init = function() {

  var widget = reform.widgets.map;

  // create a map in the "map" div, set the view to a given place and zoom
  var map = widget.object = L.map('map');

  map.setView([34.161818161230386, 9.3603515625], 5);

  L.control.scale().addTo(map);

  map.setMaxBounds(map.getBounds());

  // add an OpenStreetMap tile layer
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    //attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  var geoSearch = new L.Control.GeoSearch({
    provider: new L.GeoSearch.Provider.Google({
      region: 'tn'
    }),
    //country: "tn",
    zoomLevel: 16
  });
  map.addControl(geoSearch);
  widget.geoSearch = geoSearch;

  //map.scrollWheelZoom.disable();

  var marker;

  var latitude_input = $('#id_latitude');
  var longitude_input = $('#id_longitude');
  var location_input = $('#id_location');

  map.on('click ', function map_click(e) {
    console.log('widget', 'map', 'latlng', e.latlng);
    if (!marker) {
      marker = L.marker(e.latlng, {
        draggable: true
      });
      marker.addTo(map);
      marker.on('dragend', function(e) {
        var value = '' + e.target._latlng.lat + ',' + e.target._latlng.lng;
        latitude_input.val(e.target._latlng.lat);
        longitude_input.val(e.target._latlng.lng);
        location_input.val(value).change();
      });
    } else {
      console.log('widget', 'map', 'marker', marker);
      marker.setLatLng(e.latlng);
    }
    latitude_input.val(e.latlng.lat);
    longitude_input.val(e.latlng.lng);
    location_input.val('' + e.latlng.lat + ',' + e.latlng.lng).change();
  });

};

//$(document).ready(reform.widgets.map.init);

Dropzone.autoDiscover = false;


reform.widgets.dropzone = {};
reform.widgets.dropzone.init = function() {
  var widget = reform.widgets.dropzone;
  var dropzone = widget.object = new Dropzone('#ui-media-file-upload', {
    url: '/',
    paramName: "files", // The name that will be used to transfer the file
    maxFilesize: 10, // MB
    uploadMultiple: true,
    autoProcessQueue: false,
    addRemoveLinks: true,
    acceptedFiles: 'image/*',
    /*

    accept: function(file, done) {
      console.log(file);
      done();
    },
    */
    /*
    removedfile: function(file){
      console.log(file);
      window.file = file;
      return true;
    },
    */
    dictDefaultMessage: "Drop files or click to upload photos"
  });
};

$(document).ready(reform.widgets.dropzone.init);


reform.widgets.wizard = {};
reform.widgets.wizard.init = function() {

  var widget = reform.widgets.wizard;

  // fix for category input's values list
  $('#id_category option[selected]').removeAttr('selected').html('');

  $('.select2').select2()

  //$('.select2').selectpicker();

  var form = widget.form = $('#report-form');

  var elements = widget.elements = {};
  var inputs = widget.inputs = {};

  elements.reporterState = $('#ui-wizard-reporter-state');

  var sections = widget.sections = {
    'victim-witness': $('#ui-wizard-victim-witness-buttons'),
    'category': $('#ui-wizard-category'),
    'location-datetime': $('#ui-wizard-location-datetime'),
    'victim-aggressor': $('#ui-wizard-victim-aggressor'),
    'description-media': $('#ui-wizard-description-media'),
    'sources-media-links': $('#ui-wizard-sources-media-links'),
    'features': $('#ui-wizard-features'),
    'submit': $('#ui-wizard-submit')
  };
  //var order = widget.order = ['victim-witness', 'category', 'location-datetime', 'victim-aggressor', 'description-media', 'features', 'submit'];
  var order = widget.order = ['victim-witness', 'category', 'location-datetime', ['victim-aggressor', 'description-media', 'sources-media-links', 'features', 'submit']];

  console.log(sections);

  elements.progressBar = $('#ui-wizard-progress');

  function progress(index) {
    var progress = (index + 1) * 100 / (order.length - 1);
    console.log('progress', progress, index, order.length);
    elements.progressBar.css({
      width: progress + "%"
    });
  }

  /* victim-witness section */

  elements.victimButton = $('#ui-wizard-victim-button');
  elements.victimButtonContainer = $('#ui-wizard-victim-button-container');
  elements.witnessButton = $('#ui-wizard-witness-button');
  elements.witnessButtonContainer = $('#ui-wizard-witness-button-container');

  function victimWitnessButtonsAction(e) {
    var el = $(this);
    elements.reporterState.html(el.data('value')).addClass(el.data('class')).addClass('animated pulse');
    sections['victim-witness'].addClass('animated fadeOut').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend webkitAnimationEnd oanimationend msAnimationEnd animationend', function(e) {
      $(this).hide();
      sections['category'].addClass('animated fadeIn').show();
    });
    progress(0);
    elements.victimButton.off('click');
    elements.witnessButton.off('click');
  }

  elements.victimButton.on('click', function(e) {
    //order.splice(order.indexOf('victim'), 1);
    victimWitnessButtonsAction.call(this, e);
    $('#ui-wizard-victim-text').show();
    $('#id_victim').val('user').change();
    //$('#ui-wizard-victim-area').remove();
    //$('#ui-wizard-victim-area').hide();
    //$('#ui-wizard-aggressor-area').removeClass('span6').addClass('span12');
    $('#ui-reporter-victim-fieldset').show().removeAttr('disabled');
    $('#ui-witness-victim-label').show();
    $('#ui-reporter-victim-label').hide();
  });

  elements.witnessButton.on('click', function(e) {
    victimWitnessButtonsAction.call(this, e);
    $('#ui-wizard-witness-text').show();
    $('#id_victim').val('0').change();
    $('#ui-witness-victim-fieldset').show().removeAttr('disabled');
  });

  /*
   *  showNextSection : show sections after all fields changed
   *
   *    @section          String            current section, precedes the one to show
   *    @fields_list      Array             fields to watch
   *    @callback         Function          callback to call after change
   */

  function showNextSection(section, fields_list, callback) {

    function showNextSectionClosure(e) {

      console.log('element', this);
      console.log('target', e.target);
      //console.log(this.name);
      //console.log(e.target.name);

      var fields = showNextSectionClosure.fields;
      console.log('fields', fields);

      fields[this.name] = true;
      console.log('fields', fields);

      var ready = Object.keys(fields).reduce(function(previous, key) {
        return previous && fields[key];
      }, true);

      console.log('ready', ready);

      if (ready) {
        var index = order.indexOf(section);
        var next_index = order[index + 1];
        var next_section;
        if (Array.isArray(next_index)) {
          next_section = next_index.map(function(i) {
            return sections[i];
          });
        } else {
          next_section = sections[next_index];
        }
        console.log('section', section, sections[section]);
        console.log('next section', next_index, next_section);
        if (next_section) {
          if (Array.isArray(next_section)) {
            next_section.forEach(function(e) {
              $(e).addClass('animated fadeIn').show();
            });
          } else {
            next_section.addClass('animated fadeIn').show();
          }
        }
        progress(index);
        if (callback)
          callback();
      }

      $(this).off('change.showNextSection');

    }
    showNextSectionClosure.fields = {};
    fields_list.forEach(function(name) {
      showNextSectionClosure.fields[name] = false;
    });

    return showNextSectionClosure;

  }

  function handleShowNextSection(section, fields_list, callback) {
    var handler = showNextSection(section, fields_list, callback);
    fields_list.forEach(function(field) {
      elements[field].on('change.showNextSection', handler);
    });
  }

  /* */

  Array.prototype.slice.apply(document.querySelector('#report-form').elements).forEach(function(e) {
    elements[e.name] = $(e);
  });

  /* category section */

  elements.category = $('#id_category');

  /*
  var showLocationSection = showNextSection('category-datetime', ['category', 'datetime'], reform.widgets.map.init);
  elements.category.on('change.showNextSection', showLocationSection);
  elements.datetime.on('change.showNextSection', showLocationSection);
  */

  handleShowNextSection('category', ['category'], reform.widgets.map.init);

  /* location-datetime section */

  elements.latitude = $('#id_latitude');
  elements.longitude = $('#id_longitude');
  elements.location = $('#id_location');
  elements.location_text = $('#id_location_text');
  elements.datetime = $('#id_datetime');
  elements.date = $('#id_date');
  elements.time = $('#id_time');

  /*
  var showVictimAggressorSection = showNextSection('location', ['location', 'location_text']);
  elements.location.on('change.showNextSection', showVictimAggressorSection);
  elements.location_text.on('change.showNextSection', showVictimAggressorSection);
  */
  handleShowNextSection('location-datetime', ['location', 'location_text', 'datetime']);

  elements.location.on('change', function(e) {
    var location_text = elements.location_text;
    console.log(this.value);
    var latlng = this.value.split(',');
    console.log(latlng);
    var lat = parseFloat(latlng[0], 10),
      lng = parseFloat(latlng[1], 10);
    var geocoder = new google.maps.Geocoder();
    //var geocoder = L.GeoSearch.Provider.Google.Geocoder;
    geocoder.geocode({
      location: new google.maps.LatLng(lat, lng),
      region: 'tn'
    }, function(data, status) {
      //try { location_text.typeahead('destroy'); } catch(e) {};
      if (status == google.maps.GeocoderStatus.OK) {
        var results = [];
        for (var i = 0; i < data.length; i++)
          results.push(data[i].formatted_address);
        console.log(results);
        if (results.length > 0) {
          /*
          location_text.typeahead({
            //name: 'location_text',
            local: results
          });
          */
          location_text.val(results[0]).change();
        }
      }
    });
  });

  /* victim-aggressor section */

  elements.victim = $('#id_victim');

  elements.aggressor = $('#id_aggressor');

  //handleShowNextSection('victim', ['victim-firstname']);

  /*
  var els = Array.prototype.slice.apply(document.querySelector('#ui-witness-victim-fieldset').elements);
  els.forEach(function(e) {
    elements[e.name] = $(e);
  });
  */

  /*
  var showAggressorSection = showNextSection('victim', ['victim-firstname']);
  elements.victim.on('change.showNextSection', showAggressorSection);
  */
  //handleShowNextSection('victim', ['victim-firstname']);

  /*
  var showDescriptionMediaection = showNextSection('aggressor', ['aggressor']);
  elements.aggressor.on('change.showNextSection', showDescriptionMediaSection);
  */
  //handleShowNextSection('aggressor', ['aggressor']);

  // show on click
  /*
  $('#ui-aggressor-next').on('click', function(){
    aggressorInput.trigger('change');
  });
  */

  /* description-media section */

  elements.description = $('#id_description');

  /* sources-media-links section */

  elements.sourcesList = $('#ui-sources-list');
  elements.sourcesSourceInput = $('#ui-sources-source-input');
  elements.sourcesUrlInput = $('#ui-sources-url-input');
  elements.sourcesAddButton = $('#ui-sources-add-button');

  var sourceItemTemplate = $('#ui-sources-list-item').html();

  elements.sourcesAddButton.on('click', function(e) {
    e.preventDefault();
    var source = elements.sourcesSourceInput.val();
    var url = elements.sourcesUrlInput.val();
    if (!source) {
      elements.sourcesSourceInput.focus();
      return;
    }
    if (!url || !elements.sourcesUrlInput.get(0).checkValidity()) {
      elements.sourcesUrlInput.focus();
      return;
    }
    var element = $(_.template(sourceItemTemplate, {
      source: source,
      url: url,
      value: '[' + source + '](' + url + ')'
    }));
    elements.sourcesList.append(element);
    element.find('.ui-sources-remove-button').on('click', function(e) {
      e.preventDefault();
      element.remove();
    });
    elements.sourcesSourceInput.val(null);
    elements.sourcesUrlInput.val(null);
    elements.sourcesSourceInput.focus();
  });

  elements.linksList = $('#ui-links-list');
  elements.linksUrlInput = $('#ui-links-url-input');
  elements.linksAddButton = $('#ui-links-add-button');

  var linkItemTemplate = $('#ui-links-list-item').html();

  elements.linksAddButton.on('click', function(e) {
    e.preventDefault();
    var url = elements.linksUrlInput.val();
    if (!url || !elements.linksUrlInput.get(0).checkValidity()) {
      elements.linksUrlInput.focus();
      return;
    };
    var element = $(_.template(linkItemTemplate, {
      url: url
    }));
    elements.linksList.append(element);
    element.find('.ui-links-remove-button').on('click', function(e) {
      e.preventDefault();
      element.remove();
    });
    elements.linksUrlInput.val(null);
    elements.linksUrlInput.focus();
  });

  /*
  var showFeaturesSection = showNextSection('description-media', ['description']);
  elements.description.on('change.showNextSection', showFeaturesSection);
  */
  //handleShowNextSection('description-media', ['description']);

  elements.features = $('#id_features');

  /*
  var showSubmitSection = showNextSection('features', ['features']);
  elements.features.on('change.showNextSection', showSubmitSection);
  */
  //handleShowNextSection('features', ['features']);


  $('#report-form').on('submit', function(e) {
    e.preventDefault();
    $('.report-incident-form').block({
      message: '<h3>Processing ...</h3>'
    });

    var data = {};
    var formData = new FormData(this);
    var files = reform.widgets.dropzone.object.files;
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      console.log(file);
      formData.append('files[]', file);
    }
    $.ajax({
      type: "POST",
      url: reform.urls.submit,
      data: formData,
      processData: false,
      contentType: false,
      //dataType: dataType
      headers: {
        "X-CSRFToken": csrf_token
      }
    }).done(function(data) {
      setTimeout(function() {
        //window.location = 'reports/' + data.object.id + '/view';
        //window.location = reform.urls.view.replace('0', data.object.id);
        window.location = data.url;
      }, 500);
      $.pnotify({
        title: data.notification.title,
        text: data.notification.body,
        type: 'success',
        nonblock: true
      });
    }).fail(function(err) {
      console.log(err);
      var data = err.responseJSON;
      $.pnotify({
        title: data.notification.title,
        text: data.errors['__all_'] ? data.errors['__all__'].join("<br>") : data.notification.body,
        type: 'error',
        //nonblock: true
      });
      $('.report-incident-form').unblock();
    });
    return false;
  })

};

$(document).ready(reform.widgets.wizard.init);


reform.widgets.datetime = {};
reform.widgets.datetime.init = function() {
  var widget = reform.widgets.datetime;

  var elements = reform.widgets.wizard.elements;
  var timeInput = elements.time,
    dateInput = elements.date,
    datetimeInput = elements.datetime;

  function handleDateOrTimeChange(e) {
    var time = timeInput.val();
    var date = dateInput.val();

    if (date && time) {
      datetimeInput.val(date + ' ' + time).trigger('change'); //change();
    }
  }

  timeInput.on('change', handleDateOrTimeChange);
  dateInput.on('change', handleDateOrTimeChange);

  var clndr;

  function previousYear(e) {
    //console.log('previousYear', clndr.element.find('.clndr-previous-year-button'), clndr.element.find('.clndr-next-year-button'))
    clndr.previousYear();
  }

  function nextYear(e) {
    //console.log('nextYear', clndr.element.find('.clndr-previous-year-button'), clndr.element.find('.clndr-next-year-button'))
    clndr.nextYear();
  }

  clndr = widget.object = $('#dateinput').clndr({

    template: $('#dateinput-template').html().split(/\n|\r/gi).map(function(s) {
      return s.trim()
    }).join(''),

    adjacentDaysChangeMonth: true,

    clickEvents: {
      click: function(target) {
        console.log(target);
        if (target.date._f) {
          dateInput.val(target.date._i).change();
          $('#dateinput .day.selected').removeClass('selected');
          $(target.element).addClass('selected');
        }
      },
    },

    doneRendering: function() {
      console.log('doneRendering', this);
      if (clndr) {
        clndr.element.find('.clndr-previous-year-button').off('click').on('click', previousYear);
        clndr.element.find('.clndr-next-year-button').off('click').on('click', nextYear);
      }
    }

  });

  clndr.element.find('.clndr-previous-year-button').off('click').on('click', previousYear);
  clndr.element.find('.clndr-next-year-button').off('click').on('click', nextYear);

};

$(document).ready(reform.widgets.datetime.init);


reform.widgets.similarReports = {};
reform.widgets.similarReports.init = function() {
  var widget = reform.widgets.similarReports;
  /*
  var similarReports =
  widget.object = similarReports;
  widget.element = similarReports;
  */

  var similar = false,
    latestReportsLabel = $('#ui-latest-reports-label'),
    similarReportsLabel = $('#ui-similar-reports-label'),
    noSimilarReportsNotification = $('#ui-no-similar-reports'),
    noReportsNotification = $('#ui-no-reports'),
    reportsList = $('#ui-reports-list'),
    reportsItems = reportsList.find('.ui-similar-report-candidate');

  //noSimilarReportsNotification.addClass('animated');

  noReportsNotification.addClass('animated fadeInUp').show();

  window.similarReports = widget;

  widget.reportsList = reportsList;
  widget.reportsItems = reportsItems;

  var elements = reform.widgets.wizard.elements;

  function showSimilarReports(e) {

    if (!similar) {
      latestReportsLabel.hide();
      similarReportsLabel.css({
        'display': 'inline-block'
      }).addClass('animated pulse').show();
      similar = true;
    }

    var formData = new FormData(document.querySelector('#report-form'));

    $('#ui-reports-list').block({
      message: 'Loading ...',
    });
    $.ajax({
      type: "POST",
      url: reform.urls.similar,
      data: formData,
      processData: false,
      contentType: false,
      dataType: 'json',
      headers: {
        "X-CSRFToken": csrf_token
      }
    }).done(function(data) {
      reportsList.html(data.html).find('#ui-no-similar-reports').addClass('animated fadeInUp').show();;
      $('#ui-reports-list').unblock();
    }).fail(function(err) {
      console.log(err);
      /*
      var data = err.responseJSON;
      $.pnotify({
        title: data.notification.title,
        text: data.errors['__all_'] ? data.errors['__all__'].join("<br>") : data.notification.body,
        type: 'error',
        //nonblock: true
      });
      */
    });
    //reportsList.html('<li><div class="text-center">Loading ...</div></li>')

    return;


    var any = false;
    reportsItems.each(function(index, el) {
      el = $(el);
      el.addClass('animated');

      //if(widget.isSimilarToInput(e, el)) {
      //var similarities = widget.checkSimilarity(e, el);
      //if(similarities.length > 0) {
      if (true) {
        any = true;
        //el.removeClass().addClass('ui-similar-report-candidate ui-similar').addClass(similarities.map(function(field){ return 'ui-similar-' + field;}).join(' ')); //.show();
        /*
        el.removeClass('fadeOutRight')
        if(!el.hasClass('fadeInRight')) {
          el.addClass('fadeInRight').show();
        }
        */
      } else {
        //el.removeClass().addClass('ui-similar-report-candidate'); //.hide();
        /*
        el.removeClass('fadeInRight');
        if(!el.hasClass('fadeOutRight')) {
          el.addClass('fadeOutRight').hide();
          //.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend webkitAnimationEnd oanimationend msAnimationEnd animationend', function(e) { $(this).hide(); });
        }
        */
      }
    });
    if (any) {
      //noSimilarReportsNotification.hide();
      /*
      noSimilarReportsNotification.removeClass('fadeInUp');
      if(!noSimilarReportsNotification.hasClass('fadeOutDown')) {
        noSimilarReportsNotification.addClass('fadeOutDown').hide();
        //.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend webkitAnimationEnd oanimationend msAnimationEnd animationend', function(e) { $(this).hide(); });
      }
      */
    } else {
      //noSimilarReportsNotification.show();
      /*
      noSimilarReportsNotification.removeClass('fadeOutDown');
      if(!noSimilarReportsNotification.hasClass('fadeInUp')) {
        noSimilarReportsNotification.addClass('fadeInUp').show();
      }
      */
    }

  }

  var elements = reform.widgets.wizard.elements;

  elements.category.on('change', showSimilarReports);

  elements.location.on('change', showSimilarReports);

  //elements.datetime.on('change', showSimilarReports);
  elements.date.on('change', showSimilarReports);

  elements['victim-firstname'].on('change', showSimilarReports);

  elements['victim-lastname'].on('change', showSimilarReports);

};

$(document).ready(reform.widgets.similarReports.init);


/*
reform.widgets.xxx = {};
reform.widgets.xxx.init = function() {
  var widget = reform.widgets.xxx;
  var xxx =
  widget.object = xxx;
  widget.element = xxx;
};

$(document).ready(reform.widgets.xxx.init);
*/
