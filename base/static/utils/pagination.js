
reform.widgets.pagination = function(id, status, url, refreshCallback){

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

  function bindReportItemsToMap() {
    //list.find('.ui-timeline-story').on('mouseover', function(e) {
    list.find('.ui-timeline-story-locator').on('click', function(e) {
      e.stopPropagation();
      e.preventDefault();
      console.log(marker, e.target, e.currentTarget, e.relatedTarget, e.delegateTarget);
      //var loc = $(e.target).closest('li').data('latlng').split(',');
      //loc = new L.LatLng(loc[0], loc[1]);
      var li = $(e.target).closest('li');
      var loc = new L.LatLng(li.data('latitude'), li.data('longitude'));
      /*
      if (!marker) {
        console.log(loc);
        marker = L.marker(loc);
        console.log(marker);
        marker.addTo(reform.widgets.map);
      } else {
        marker.setLatLng(loc);
      }
      */
      reform.widgets.map.setView(loc, 12);
    });
  }

  bindReportItemsToMap();

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
      .done(bindReportItemsToMap);
    //list.html('<li>Loading ...</li>');
    list.block({
      message: 'Loading ...',
      //css: { border: '3px solid #a00' }
    });
  }

};
/*
$(document).ready(function(){
  reform.widgets.pagination('#ui-incidents-list', reform.data.incidentsPagination, reform.urls.incidentsDashboard)
  reform.widgets.pagination('#ui-thanks-list', reform.data.thanksPagination, reform.urls.thanksDashboard)
});
*/