// call this from the developer console and you can control both instances
var calendars = {};

$(document).ready( function() {

  // assuming you've got the appropriate language files,
  // clndr will respect whatever moment's language is set to.
  // moment.lang('ru');

  // here's some magic to make sure the dates are happening this month.
  var thisMonth = moment().format('YYYY-MM');

  // Here's our events array. We could grab this via AJAX as well.
  var eventArray = [
    { date: thisMonth + "-24 07:52", title: "This is an event title", url: "http://google.com", time: "7:15PM" },
    { date: thisMonth + "-28", title: "the 28th, Part 1", url: "http://www.google.com" },
    { date: thisMonth + "-28", title: "the 28th, Part 2", arbitraryObject: 42 },
    { date: thisMonth + "-16", title: "Another title", anotherObject: "clndr exposes whatever is in your event object" },
    { date: moment().add('months', 1).format('YYYY-MM') + "-02", title: "Next Month Party", anotherObject: "This is always happening next month." }
  ];

  calendars.clndr1 = $('.cal1').clndr({
    events: eventArray,
    clickEvents: {
      click: function(target) {
        console.log(target);
      }
    },
    showAdjacentMonths: false,
    adjacentDaysChangeMonth: true
  });

  calendars.clndr2 = $('.cal2').clndr({
    template: $('#template-calendar').html(),
    events: eventArray,
    startWithMonth: moment().add('month', 1),
    clickEvents: {
      click: function(target) {
        console.log(target);
      }
    }
  });

  // bind both clndrs to the left and right arrow keys
  $(document).keydown( function(e) {
    if(e.keyCode == 37) {
      // left arrow
      calendars.clndr1.back();
      calendars.clndr2.back();
    }
    if(e.keyCode == 39) {
      // right arrow
      calendars.clndr1.forward();
      calendars.clndr2.forward();
    }
  });

});