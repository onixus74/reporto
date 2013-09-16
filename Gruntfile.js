'use strict';

module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({

		pkg: grunt.file.readJSON('package.json'),

		compass: {

			base: {
				options: {
					basePath: 'base/static/',
					sassDir: 'styles',
					cssDir: 'styles',
					force: true
				}
			},

			reports: {
				options: {
					basePath: 'reports/static/reports',
					sassDir: 'styles',
					cssDir: 'styles',
					force: true
				}
			},

		},

		cssmin: {

			components: {
				expand: true,
				cwd: 'base/static/components',
				src: ['**/*.css', '!*.min.css', '!*.dist.css'],
				dest: 'base/static/components',
				ext: '.min.css'
			},

			base: {
				expand: true,
				cwd: 'base/static/styles',
				src: ['**/*.css', '!*.min.css', '!*.dist.css'],
				dest: 'base/static/styles',
				ext: '.min.css'
			},

			reports: {
				expand: true,
				cwd: 'reports/static/reports/styles',
				src: ['**/*.css', '!*.min.css', '!*.dist.css'],
				dest: 'reports/static/reports/styles',
				ext: '.min.css'
			}

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
				cwd: 'base/static/scripts',
				src: ['**/*.js', '!*.min.js', '!*.dist.js'],
				dest: 'base/static/scripts',
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
				expand: true,
				cwd: 'reprots/static/reports/scripts',
				src: ['**/*.js', '!*.min.js', '!*.dist.js'],
				dest: 'reports/static/reports/scripts',
				ext: '.min.js'
				/*
				files: {
					'reports/static/reports/scripts/reports': ['reports/static/reports/scripts/reports.js'],
					'reports/static/reports/scripts/reports-all.dist.js': [
						'base/static/scripts/app.js',
						'reports/static/reports/scripts/reports.js']
				}
				*/
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
				dest: 'reports/static/reports/scripts/reports-all.dist.js'
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
	grunt.loadNpmTasks('grunt-contrib-compass');

	// Register default task
	grunt.registerTask('static', ['cssmin:static'], 'uglify:static');
	grunt.registerTask('base', ['compass:base', 'cssmin:base', 'uglify:base']);
	grunt.registerTask('reports', ['compass:reports', 'cssmin:reports', 'uglify:reports']);
	grunt.registerTask('default', ['base', 'reports']);

};
