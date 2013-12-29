'use strict';

function makeDjangoAppConfig(config, applicationName){

  config.compass[applicationName] = {
    options: {
      basePath: '{app}/static/{app}'.replace(/{app}/g, applicationName),
      sassDir: 'styles',
      cssDir: 'styles',
      force: true
    }
  };

  config.cssmin[applicationName] = {
    expand: true,
    cwd: '{app}/static/{app}/styles'.replace(/{app}/g, applicationName),
    src: ['**/*.css', '!*.min.css', '!*.dist.css'],
    dest: '{app}/static/{app}/styles'.replace(/{app}/g, applicationName),
    ext: '.min.css'
  };

  config.uglify[applicationName] = {
    options: {
      sourceMap: function(dst) {
        return dst + '.map';
      },
      sourceMappingURL: function(dst) {
        return '/' + dst.substr(dst.indexOf('static')) + '.map';
      },
      sourceMapPrefix: 4
    },
    expand: true,
    cwd: '{app}/static/{app}/scripts'.replace(/{app}/g, applicationName),
    src: ['**/*.js', '!*.min.js', '!*.dist.js'],
    dest: '{app}/static/{app}/scripts'.replace(/{app}/g, applicationName),
    ext: '.min.js'
  };

}

module.exports = function(grunt) {


  var config = {

    pkg: grunt.file.readJSON('package.json'),

    compass: {},

    cssmin: {

      components: {
        expand: true,
        cwd: 'base/static/components',
        src: ['**/*.css', '!*.min.css', '!*.dist.css'],
        dest: 'base/static/components',
        ext: '.min.css'
      },

    },

    uglify: {

      components: {
        options: {
          sourceMap: function(dst) {
            return dst + '.map';
          },
          sourceMappingURL: function(dst) {
            return '/' + dst.substr(dst.indexOf('static')) + '.map';
          },
          sourceMapPrefix: 4
        },
        expand: true,
        cwd: 'base/static/components',
        src: ['**/*.js', '!*.min.js', '!*.dist.js'],
        dest: 'base/static/components',
        ext: '.min.js'
      },

    },

    concat: {},

    watch: {}

  };

  /*
  var config = {
    pkg: grunt.file.readJSON('package.json'),
    compass: {},
    cssmin: {},
    uglify: {},
    contact: {},
    watch: {},
  };
  */

  /* base */

  config.compass.base = {
    options: {
      basePath: 'base/static',
      sassDir: 'styles',
      cssDir: 'styles',
      force: true
    }
  };

  config.cssmin.base = {
    expand: true,
    cwd: 'base/static/styles',
    src: ['**/*.css', '!*.min.css', '!*.dist.css'],
    dest: 'base/static/styles',
    ext: '.min.css'
  };

  config.uglify.base = {
    options: {
      sourceMap: function(dst) {
        return dst + '.map';
      },
      sourceMappingURL: function(dst) {
        return '/' + dst.substr(dst.indexOf('static')) + '.map';
      },
      sourceMapPrefix: 4
    },
    expand: true,
    cwd: 'base/static/scripts',
    src: ['**/*.js', '!*.min.js', '!*.dist.js'],
    dest: 'base/static/scripts',
    ext: '.min.js'
  };


  /* dashboard */

  config.compass.dashboard = {
    options: {
      basePath: 'base/static',
      sassDir: 'dashboard/styles',
      cssDir: 'dashboard/styles',
      force: true
    }
  };

  config.cssmin.dashboard = {
    expand: true,
    cwd: 'base/static/dashboard/styles',
    src: ['**/*.css', '!*.min.css', '!*.dist.css'],
    dest: 'base/static/dashboard/styles',
    ext: '.min.css'
  };

  config.uglify.dashboard = {
    options: {
      sourceMap: function(dst) {
        return dst + '.map';
      },
      sourceMappingURL: function(dst) {
        return '/' + dst.substr(dst.indexOf('static')) + '.map';
      },
      sourceMapPrefix: 4
    },
    expand: true,
    cwd: 'base/static/dashboard/scripts',
    src: ['**/*.js', '!*.min.js', '!*.dist.js'],
    dest: 'base/static/dashboard/scripts',
    ext: '.min.js'
  };

  makeDjangoAppConfig(config, 'users');
  makeDjangoAppConfig(config, 'violations');
  makeDjangoAppConfig(config, 'appreciations');

  grunt.initConfig(config);

  // Load the plugin.
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-compass');

  // Register default task
  //grunt.registerTask('static', ['cssmin:static'], 'uglify:static');
  grunt.registerTask('base', ['compass:base', 'cssmin:base', 'uglify:base']);
  grunt.registerTask('users', ['compass:users', 'cssmin:users', 'uglify:users']);
  grunt.registerTask('dashboard', ['compass:dashboard', 'cssmin:dashboard', 'uglify:dashboard']);
  grunt.registerTask('violations', ['compass:violations', 'cssmin:violations', 'uglify:violations']);
  grunt.registerTask('appreciations', ['compass:appreciations', 'cssmin:appreciations', 'uglify:appreciations']);
  grunt.registerTask('default', ['base', 'users', 'violations', 'appreciations', 'dashboard']);

};
