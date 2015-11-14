'use strict';

module.exports = function(grunt) {

  require('load-grunt-tasks')(grunt);
  require('time-grunt')(grunt);

  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.initConfig({

    sass: {
      dist: {
        options: {
          style: "compressed"
        },
        files: {
          'static/styles/styles.css': 'static/styles/styles.scss'
        }
      }
    },

    watch: {
      sass: {
        files: ['static/styles/*.scss'],
        tasks: ['sass']
      }
    }

  });

  grunt.registerTask('default', ['sass']);
  grunt.registerTask('dev', ['watch']);

};
