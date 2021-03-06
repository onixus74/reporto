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

reform.widgets.map = {};
reform.widgets.map.init = function() {

  var widget = reform.widgets.map;

  var map = widget.object = L.map('map', {
    center: new L.LatLng(reform.data.report.latitude, reform.data.report.longitude),
    zoom: 8
  });

  // add an OpenStreetMap tile layer
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

  L.marker([reform.data.report.latitude, reform.data.report.longitude]).addTo(map);

  L.control.scale().addTo(map);

  //map.setMaxBounds(map.getBounds());

  map.scrollWheelZoom.disable();

}

$(document).ready(reform.widgets.map.init);


reform.widgets.comment = {};
reform.widgets.comment.init = function() {
  var widget = reform.widgets.comment;

  var content = $('#ui-add-comment-content');
  var attachment = $('#ui-add-comment-attachment');
  var attachmentButton = $('#ui-add-comment-attachment-button');
  var attachmentIcon = $('#ui-comment-attachment-icon');
  var attachmentImage = $('#ui-comment-attachment-image');
  var updateButton = $('#ui-add-update-comment-button');
  var correctionButton = $('#ui-add-correction-comment-button');
  var comments = $('#ui-comments');
  var comments_formset = document.getElementById('ui-comments-area');

  attachment.on('change', function(e) {
    var files = e.target.files;
    var f = files[0];
    var reader = new FileReader();

    reader.onload = (function(theFile) {
      return function(e) {
        attachmentImage.attr('src', e.target.result);
        attachmentIcon.hide();
        attachmentImage.show();
      };
    })(f);

    reader.readAsDataURL(f);
  })

  attachmentButton.on('click', function(e) {
    attachment.click();
  });

  function handleClick(e) {

    e.preventDefault();

    var type = 'U';
    console.log(e.target);
    if (e.target.id == 'ui-add-correction-comment-button')
      type = 'C';

    var formdata = new FormData();
    //formdata.append('csrfmiddlewaretoken': csrf_token);
    formdata.append('content', content.val());
    formdata.append('type', type);
    formdata.append('attachment', attachment.get(0).files[0]);
    console.log(attachment.get(0).files[0])

    comments_formset.disabled = true;
    $.ajax({
      type: "POST",
      url: reform.urls.comment,
      data: formdata,
      processData: false,
      contentType: false,
      //dataType: dataType
      headers: {
        "X-CSRFToken": csrf_token
      }
    }).done(function(data) {
      $('#ui-no-comments').remove();
      comments.append(data.html);
      comments.find(".fancybox").fancybox();
      content.val('');
      attachment.val(null);
      $.pnotify({
        title: data.notification.title,
        text: data.notification.body,
        type: 'success',
        nonblock: true
      });
      attachmentImage.attr('src', '');
      attachmentIcon.show();
      attachmentImage.hide();
      comments_formset.disabled = false;
    }).fail(function(err) {
      console.log(err);
      var data = err.responseJSON;
      $.pnotify({
        title: data.notification.title,
        text: data.errors['__all_'] ? data.errors['__all__'].join("<br>") : data.notification.body,
        type: 'error',
        //nonblock: true
      });
      comments_formset.disabled = false;
    });
  }
  updateButton.on('click', handleClick);
  correctionButton.on('click', handleClick);

}

$(document).ready(reform.widgets.comment.init);


$(document).ready(function() {

  //$(".fancybox").fancybox();

  $(".fancybox").fancybox({
    helpers: {
      media: {},
      thumbs: {
        width: 50,
        height: 50
      },
    }
  });

  $(".fancybox-thumb").fancybox({
    prevEffect: 'none',
    nextEffect: 'none',
    helpers: {
      /*title: {
            type: 'outside'
          },*/
      thumbs: {
        width: 50,
        height: 50
      }
    }
  });

  $('.fancybox-media').fancybox({
    /*
        openEffect  : 'none',
        closeEffect : 'none',
        */
    helpers: {
      media: {}
    }
  });
});


$.fn.editable.defaults.mode = 'inline';
$.fn.editable.defaults.anim = 'fast';
$.fn.editable.defaults.ajaxOptions = {
  headers: {
    "X-CSRFToken": csrf_token
  }
};
$(document).ready(function() {
  //$('.ui-editable').editable();
  $('#id_category').editable();
  $('#id_datetime').editable();
  $('#id_location').editable();

  $('#id_description').editable({
    toggle: 'manual',
    /*
    display: function(value) {
      $('#view').text(value);
    }
    */
  });

  $('#ui-description-edit').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $('#ui-description').editable('toggle');
  });


  $('#id_aggressor').editable({
    toggle: 'manual',
  });

  $('#ui-aggressor-edit').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $('#ui-aggressor').editable('toggle');
  });

  $('#id_features').editable({
    toggle: 'manual',
    select2: {
      multiple: true
    }
  });

  $('#ui-features-edit').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $('#ui-features').editable('toggle');
  });

});
