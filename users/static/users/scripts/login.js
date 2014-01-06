/* jshint strict: true, browser: true, devel: true */
/* global reform, Highcharts */

$(document).ready(function() {

  $.getJSON(reform.urls.statistics).done(function(statistics) {

    //console.log(statistics);

    reform.data.violationsCount = statistics.violations_count;
    reform.data.violationsCategories = statistics.violations_categories;
    reform.data.violationsFeatures = statistics.violations_features;
    reform.data.violationsByCategory = statistics.violations_by_category;
    reform.data.violationsByFeature = statistics.violations_by_feature;
    reform.data.violationsByVictimGender = statistics.violations_by_victim_gender;
    reform.data.violationsByVictimEducation = statistics.violations_by_victim_education;
    reform.data.violationsByDate = statistics.violations_by_date;
    reform.data.violationsByCategoryByDate = statistics.violations_by_category_by_date;
    reform.data.violationsLocations = statistics.violations_locations;

    reform.data.appreciationsCount = statistics.appreciations_count;
    reform.data.appreciationsByDate = statistics.appreciations_by_date;
    reform.data.appreciationsCategories = statistics.appreciations_categories;
    reform.data.appreciationsByCategory = statistics.appreciations_by_category;
    reform.data.appreciationsLocations = statistics.appreciations_locations;

    reform.widgets.charts.reportsByDate();
    reform.widgets.charts.violationsByCategory();
    reform.widgets.charts.violationsByVictimGender();
    reform.widgets.charts.violationsByVictimEducation();
    reform.widgets.charts.violationsByFeatures();
    //reform.widgets.charts.appreciationByCategory();

  });
});
