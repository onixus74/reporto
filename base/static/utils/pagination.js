reform.widgets.pagination = function(id, status, url , refreshCallback) {

  var list = $(id);

  var pagination = list.parent().find('.pagination');

  var widget = {};

  var paginationControls = widget.paginationControls = pagination.find('.ui-pagination-control');
  var paginationIndicator = widget.paginationIndicator = pagination.find('.ui-pagination-indicator');
  var paginationFirst = widget.paginationFirst = pagination.find('.ui-pagination-first');
  var paginationLast = widget.paginationLast = pagination.find('.ui-pagination-last');
  var paginationPrevious = widget.paginationPrevious = pagination.find('.ui-pagination-previous');
  var paginationNext = widget.paginationNext = pagination.find('.ui-pagination-next');

  //console.log(pagination, widget);

  function updatePagination() {
    paginationIndicator.html(String(status.current) + ' / ' + String(status.pages));
    paginationFirst.off('click');
    paginationLast.off('click');
    paginationPrevious.off('click');
    paginationNext.off('click');
    if (status.current == 1) {
      paginationFirst.closest('li').addClass('disabled');
      paginationFirst.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
      });
      paginationPrevious.closest('li').addClass('disabled');
      paginationPrevious.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
      });
    } else {
      paginationFirst.closest('li').removeClass('disabled');
      paginationFirst.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        showPage(1);
      });
      paginationPrevious.closest('li').removeClass('disabled');
      paginationPrevious.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        showPage(status.current - 1);
      });
    }
    if (status.current == status.pages) {
      paginationNext.closest('li').addClass('disabled');
      paginationNext.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
      });
      paginationLast.closest('li').addClass('disabled');
      paginationLast.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
      });
    } else {
      paginationNext.closest('li').removeClass('disabled');
      paginationNext.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        showPage(status.current + 1);
      });
      paginationLast.closest('li').removeClass('disabled');
      paginationLast.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        showPage('last');
      });
    }
  }

  updatePagination();

  var marker;

  function callback(){
    if(refreshCallback)
      refreshCallback(list);
  }

  function showPage(page) {
    $.get(url + '.json?page=' + page).done(function(data) {
      console.log(arguments, status);
      status.current = data.current;
      list.html(data.html);
    })
      .done(updatePagination)
      .done(function() {
        list.unblock();
      })
      .done(callback);
    //list.html('<li>Loading ...</li>');
    list.block({
      message: 'Loading ...',
      //css: { border: '3px solid #a00' }
    });
  }

  callback();

};
/*
$(document).ready(function() {
  function refreshCallback(list) {
    list.find('.ui-timeline-story-locator').on('click', function(e) {
      e.stopPropagation();
      e.preventDefault();
      var li = $(e.target).closest('li');
      var loc = new L.LatLng(li.data('latitude'), li.data('longitude'));
      reform.widgets.map.setView(loc, 12);
      $.scrollTo(reform.widgets.map._container, 500);
    });
  }
  reform.widgets.pagination('#ui-violations-list', reform.data.violationsPagination, reform.urls.violationsDashboard, refreshCallback);
  reform.widgets.pagination('#ui-thanks-list', reform.data.thanksPagination, reform.urls.thanksDashboard, refreshCallback);
});

*/
