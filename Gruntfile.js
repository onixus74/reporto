'use strict';

module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({

    pkg: grunt.file.readJSON('package.json'),

    cssmin: {

      static: {
        expand: true,
        cwd: 'static',
        src: ['**/*.css', '!*.min.css', '!*.dist.css'],
        dest: 'static',
        ext: '.min.css'
      },

      base: {
        expand: true,
        cwd: 'base',
        src: ['**/*.css', '!*.min.css', '!*.dist.css'],
        dest: 'base',
        ext: '.min.css'
      },

      reports: {
        expand: true,
        cwd: 'reports/static',
        src: ['**/*.css', '!*.min.css', '!*.dist.css'],
        dest: 'reports/static',
        ext: '.min.css'
      }

    },

    uglify: {

      static: {
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
        cwd: 'static',
        src: ['**/*.js', '!*.min.js', '!*.dist.js'],
        dest: 'static',
        ext: '.min.js'
      },

      base: {
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
        cwd: 'base',
        src: ['**/*.js', '!*.min.js', '!*.dist.js'],
        dest: 'base',
        ext: '.min.js'
      },

      reports: {
        options: {
          sourceMap: function(dst) {
            return dst + '.map';
          },
          sourceMappingURL: function(dst) {
            return '/' + dst.substr(dst.indexOf('static')) + '.map';
          },
          sourceMapPrefix: 4
        },
        files: {
          'reports/static/reports/scripts/reports': ['reports/static/reports/scripts/reprots.js'],
          'reports/static/reports/scripts/reprots-all.dist.js': [
            'base/static/scripts/app.js',
            'reports/static/reports/scripts/reports.js']
        }
      }

    },

    concat: {
      options: {
        // define a string to put between each file in the concatenated output
        separator: ';'
      },
      jsdist: {
        // the files to concatenate
        src: ['reports/static/reports/scripts/**/*.min.js'],
        // the location of the resulting JS file
        dest: 'reports/static/reports/scripts/reprots-all.dist.js'
      }
    },

    watch: {
      scripts: {
        files: ['reports/static/reports/scripts/**/*.js', '!*.min.js', '!*.dist.js'],
        tasks: ['uglify:reports'],
        options: {
          nospawn: true
        }
      }
    }

  });

  // Load the plugin.
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');

  // Register default task
  grunt.registerTask('static', ['uglify:static', 'cssmin:static']);
  grunt.registerTask('base', ['uglify:base', 'cssmin:base']);
  grunt.registerTask('reports', ['uglify:reports', 'cssmin:reports']);
  grunt.registerTask('default', ['base', 'reports']);

};
