// Generated on 2014-05-15 using generator-django-webapp 0.4.8-0.1.0
'use strict';

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'
/*jshint indent: false */
/*jshint undef: false */

module.exports = function (grunt) {

    // Load grunt tasks automatically

    require('load-grunt-tasks')(grunt);

    // Time how long tasks take. Can help when optimizing build times
    require('time-grunt')(grunt);

    // ReuireJS configuration sample for distribution
    var requirejsDistModules = [
    ];

    // Define the configuration for all the tasks
    grunt.initConfig({

                         // Configurable paths
                         config: {
                             assets: 'static',
                             templates: 'templates',
                             collectedAssets: 'static_collected',
                             collectedTemplates: 'templates_collected',
                             dist: 'dist',
                             distAssets: 'dist/static',
                             distTemplates: 'dist/templates'
                         },

                         // Optimize RequireJS projects using r.js
                         requirejs: {
                             dist: {
                                 // https://github.com/jrburke/r.js/blob/master/build/example.build.js
                                 options: {
                                     baseUrl: '<%= config.collectedAssets %>/scripts',
                                     dir: '<%= config.distAssets %>/scripts',
                                     paths: {
                                         jquery: '../bower_components/jquery/dist/jquery',
                                         bootstrap: '../bower_components/bootstrap/dist/js/bootstrap'
                                     },
                                     shim: {
                                         bootstrap: ['jquery'],
                                     },
                                     modules: requirejsDistModules,
                                     optimize: 'uglify',
                                     preserveLicenseComments: false,
                                     useStrict: true,
                                     wrap: true,
                                     removeCombined: true,
                                     findNestedDependencies: true
                                 }
                             }
                         },

                         // Custom task to collect information of revved files of RequireJS modules,
                         // then write a temporary file for inserting into html body for paths config
                         requirejspaths: {
                             dist: {
                                 options: {
                                     baseRoot: '<%= config.distAssets %>/scripts',
                                     baseUrl: '{{ STATIC_URL }}scripts',
                                     modules: requirejsDistModules.map(function (m) {
                                         return m.name;
                                     }),
                                     outputFile: '.tmp/requirejspaths.html'
                                 }
                             }
                         },

                         // Process html files at build time to modify them depending on the release environment
                         processhtml: {
                             options: {
                                 commentMarker: 'process',
                                 includeBase: '.tmp',
                             },
                             dist: {
                                 files: [
                                     {
                                         expand: true,
                                         cwd: '<%= config.collectedTemplates %>',
                                         src: '**/*.html',
                                         dest: '<%= config.distTemplates %>'
                                     }
                                 ]
                             }
                         },

                         // Watches files for changes and runs tasks based on the changed files
                         watch: {
                             // bower: {
                             //     files: ['bower.json'],
                             //     tasks: ['bowerInstall']
                             // },

                             js: {
                                 files: ['<%= config.assets %>/scripts/**/*.js'],
                                 tasks: ['jshint'],
                                 options: {
                                     livereload: true
                                 }
                             },
                              jsTest: {
                                files: ['test/spec/{,*/}*.js'],
                                tasks: ['test:watch', 'karma']
                              },
                             gruntfile: {
                                 files: ['Gruntfile.js']
                             },
                             compass: {
                                 files: ['<%= config.assets %>/styles/**/*.{scss,sass}'],
                                 tasks: ['compass:server', 'autoprefixer']
                             },
                             less: {
                                 files: ['<%= config.assets %>/less/**/*.less'],
                                 tasks: ['less:server']
                             },
                             styles: {
                                 files: ['<%= config.assets %>/styles/**/*.css'],
                                 tasks: ['newer:copy:styles', 'autoprefixer']
                             },
                             livereload: {
                                 options: {
                                     livereload: '<%= connect.options.livereload %>'
                                 },
                                 files: [
                                     '<%= config.templates %>/**/*.html',
                                     '.tmp/styles/**/*.css',
                                     '<%= config.assets %>/images/**/*'
                                 ]
                             }
                         },

                         // The actual grunt server settings
                         connect: {
                             options: {
                                 port: 9000,
                                 open: true,
                                 livereload: 35729,
                                 // Change this to '0.0.0.0' to access the server from outside
                                 hostname: 'localhost'
                             },
                             livereload: {
                                 options: {
                                     middleware: function (connect) {
                                         return [
                                             connect.static('.tmp'),
                                             connect().use('/bower_components', connect.static('<%= config.assets %>/bower_components')),
                                             connect.static('<%= config.assets %>')
                                         ];
                                     }
                                 }
                             },
                             test: {
                                 options: {
                                     open: false,
                                     port: 9001,
                                     middleware: function (connect) {
                                         return [
                                             connect.static('.tmp'),
                                             connect.static('test'),
                                             connect().use('/bower_components', connect.static('<%= config.assets %>/bower_components')),
                                             connect.static('<%= config.assets %>')
                                         ];
                                     }
                                 }
                             },
                             dist: {
                                 options: {
                                     base: [
                                         '<%= config.distAssets %>',
                                         '<%= config.distTemplates %>'
                                     ],
                                     livereload: false
                                 }
                             }
                         },

                         // Empties folders to start fresh
                         clean: {
                             dist: {
                                 files: [
                                     {
                                         dot: true,
                                         src: [
                                             '.tmp',
                                             '<%= config.dist %>/*',
                                             '!<%= config.dist %>/.git*'
                                         ]
                                     }
                                 ]
                             },
                             server: '.tmp',
                             requirejs: '<%= config.distAssets %>/scripts/build.txt',
                             collected: [
                                 '<%= config.collectedAssets %>',
                                 '<%= config.collectedTemplates %>'
                             ]
                         },

                         // Make sure code styles are up to par and there are no obvious mistakes
                         jshint: {
                             options: {
                                 jshintrc: '.jshintrc',
                                 reporter: require('jshint-stylish')
                             },
                             all: [
                                 'Gruntfile.js',
                                 '<%= config.assets %>/scripts/**/*.js',
                                 '!<%= config.assets %>/scripts/vendor/*',
                                 '<%= config.collectedAssets %>/scripts/**/*.js',
                                 '!<%= config.collectedAssets %>/scripts/vendor/*',
                                 'test/spec/**/*.js'
                             ]
                         },

                         karma: {
                              unit: {
                                  configFile: 'karma.conf.js',
                                  singleRun: true
                              }
                         },

                         // Compiles Sass to CSS and generates necessary files if requested
                         compass: {
                             options: {
                                 cssDir: '.tmp/styles',
                                 generatedImagesDir: '.tmp/images/generated',
                                 httpImagesPath: '/images',
                                 httpGeneratedImagesPath: '/images/generated',
                                 httpFontsPath: '/fonts',
                                 relativeAssets: false,
                                 assetCacheBuster: false
                             },
                             dist: {
                                 options: {
                                     sassDir: '<%= config.collectedAssets %>/styles',
                                     imagesDir: '<%= config.collectedAssets %>/images',
                                     javascriptsDir: '<%= config.collectedAssets %>/scripts',
                                     fontsDir: '<%= config.collectedAssets %>/fonts',
                                     importPath: '<%= config.collectedAssets %>/bower_components',
                                     generatedImagesDir: '<%= config.distAssets %>/images/generated'
                                 }
                             },
                             server: {
                                 options: {
                                     sassDir: '<%= config.assets %>/styles',
                                     imagesDir: '<%= config.assets %>/images',
                                     javascriptsDir: '<%= config.assets %>/scripts',
                                     fontsDir: '<%= config.assets %>/fonts',
                                     importPath: '<%= config.assets %>/bower_components',
                                     debugInfo: true
                                 }
                             }
                         },

                         // Compile LESS files to CSS.
                         less: {
                             dist: {
                                 options: {
                                     strictMath: true,
                                 },
                                 files: [
                                     {
                                         // Dynamic expansion:
                                         // http://gruntjs.com/configuring-tasks#building-the-files-object-dynamically
                                         expand: true,
                                         cwd: '<%= config.collectedAssets %>/less',
                                         src: ['**/*.less'],
                                         dest: '.tmp/styles',
                                         ext: '.css'
                                     }
                                 ]
                             },
                             server: {
                                 options: {
                                     strictMath: true,
                                 },
                                 files: [
                                     {
                                         // Dynamic expansion:
                                         // http://gruntjs.com/configuring-tasks#building-the-files-object-dynamically
                                         expand: true,
                                         cwd: '<%= config.assets %>/less',
                                         src: ['**/*.less'],
                                         dest: '.tmp/styles',
                                         ext: '.css'
                                     }
                                 ]
                             }
                         },

                         // Add vendor prefixed styles
                         autoprefixer: {
                             options: {
                                 browsers: ['> 1%', 'last 2 versions']
                             },
                             dist: {
                                 files: [
                                     {
                                         expand: true,
                                         cwd: '.tmp',
                                         src: '{,*/}{styles,css}/**/*.css',
                                         dest: '.tmp'
                                     }
                                 ]
                             }
                         },

                         // Automatically inject Bower components into the HTML file
                         // bowerInstall: {
                         //     app: {
                         //         src: ['<%= config.templates %>/index.html'],
                         //         ignorePath: '<%= config.assets %>',
                         //         exclude: ['<%= config.assets %>/bower_components/bootstrap-sass-official/vendor/assets/javascripts/bootstrap.js']
                         //     },
                         //     sass: {
                         //         src: ['<%= config.assets %>/styles/**/*.{scss,sass}'],
                         //         ignorePath: '<%= config.assets %>/bower_components'
                         //     }
                         // },

                         // Renames files for browser caching purposes
                         filerev: {
                             files: {
                                 src: [
                                     '<%= config.distAssets %>/{,*/}{scripts,js}/**/*.js',
                                     '<%= config.distAssets %>/{,*/}{styles,css}/**/*.css',
                                     '<%= config.distAssets %>/{,*/}{images,img}/**/*.*',
                                     '<%= config.distAssets %>/{,*/}{fonts,font}/**/*.*'
                                 ]
                             }
                         },

                         // Reads HTML for usemin blocks to enable smart builds that automatically
                         // concat, minify and revision files. Creates configurations in memory so
                         // additional tasks can operate on them
                         useminPrepare: {
                             options: {
                                 root: '<%= config.collectedAssets %>',
                                 dest: '<%= config.distAssets %>',
                                 useDjangoFlow: true
                             },
                             html: '<%= config.collectedTemplates %>/**/*.html'
                         },

                         // Performs rewrites based on rev and the useminPrepare configuration
                         usemin: {
                             options: {
                                 useDjangoPatterns: true
                             },
                             html: {
                                 src: ['<%= config.distTemplates %>/**/*.html'],
                                 options: {
                                     assetsDirs: ['<%= config.distAssets %>']
                                 }
                             },
                             css: {
                                 src: ['<%= config.distAssets %>/{,*/}{styles,css}/**/*.css'],
                                 options: {
                                     assetsDirs: [
                                         '',  // Search from directory of current file first
                                         '<%= config.distAssets %>'
                                     ]
                                 }
                             }
                         },

                         // The following *-min tasks produce minified files in the dist folder
//                         imagemin: {
//                             dist: {
//                                 files: [
//                                     {
//                                         expand: true,
//                                         cwd: '<%= config.collectedAssets %>',
//                                         src: '{,*/}{images,img}/**/*.{gif,jpeg,jpg,png}',
//                                         dest: '<%= config.distAssets %>'
//                                     }
//                                 ]
//                             }
//                         },

                         svgmin: {
                             dist: {
                                 files: [
                                     {
                                         expand: true,
                                         cwd: '<%= config.collectedAssets %>',
                                         src: '{,*/}{images,img}/**/*.svg',
                                         dest: '<%= config.distAssets %>'
                                     }
                                 ]
                             }
                         },

                         // grunt-htmlcompressor is Java-based and Django-friendly. (grunt-contrib-htmlmin crashes
                         // sometimes when minifying Django templates.) However, it runs HORRIBLY SLOW if
                         // mis-configured. See performance hints below.
                         htmlcompressor: {
                             compress: {
                                 options: {
                                     // Options can be whatever htmlcompressor accepts.
                                     // https://code.google.com/p/htmlcompressor/
                                     type: 'html',
                                     removeSurroundingSpaces: 'all',
                                     compressCss: true,
                                     compressJs: true,
                                     jsCompressor: 'closure',

                                     // *** 10x PERFORMANCE BOOST HERE ***

                                     // Hint: Put the output directory here. DO NOT USE "dest" of a file mapping.
                                     output: '<%= config.distTemplates %>',

                                     // Hint: Compress files inside sub-directories of the input directory.
                                     recursive: true,

                                     // Hint: This is IMPORTANT. By default, grunt-htmlcompressor grabs the
                                     // minified content from stdout of the Java process and writes it to a file
                                     // specified by "dest" (which is `undefined` in this case). By specifying
                                     // "processName" option as the following function, it will be call at
                                     // runtime and generate a "black hole" for writing, so Grunt won't crash.
                                     // This function is consumed by grunt-htmlcompressor only.
                                     processName: function () {
                                         return '/dev/null';
                                     }
                                 },
                                 // Hint: Put your input directory here. DO NOT specify files using globbing
                                 // or dynamic patterns. Otherwise, grunt-htmlcompressor will spawn a Java process
                                 // for EACH FILE, which is INSANE. Also, "dest" is useless. You should instead
                                 // put the output directory in the "output" option above. If you need multiple
                                 // input directories, a multi-target configuration for this task is preferred.
                                 src: '<%= config.distTemplates %>'
                             }
                         },

                         // By default, your `index.html`'s <!-- Usemin block --> will take care of
                         // minification. These next options are pre-configured if you do not wish
                         // to use the Usemin blocks.
                         // concat: {
                         //     dist: {}
                         // },

                         // Only put CSS files here which are not referenced by <!-- Usemin block -->
                         // e.g. Those of Django Admin app (whose templates are certainly not Usemin-aware)
                         cssmin: {
                             dist: {
                                 files: [
                                     {
                                         // CSS minification for admin app
                                         expand: true,
                                         cwd: '<%= config.collectedAssets %>',
                                         src: 'admin/css/**/*.css',
                                         dest: '<%= config.distAssets %>'
                                     }
                                 ]
                             }
                         },

                         // Only put JavaScript files here which are not referenced by <!-- Usemin block -->
                         // e.g. Those of Django Admin app (whose templates are certainly not Usemin-aware)
                         uglify: {
                             dist: {
                                 files: [
                                     {
                                         // JavaScript uglification for admin app
                                         expand: true,
                                         cwd: '<%= config.collectedAssets %>',
                                         src: 'admin/js/**/*.js',
                                         dest: '<%= config.distAssets %>'
                                     }
                                 ]
                             }
                         },

                         // Copies remaining files to places other tasks can use
                         copy: {
                             dist: {
                                 files: [
                                     {
                                         // Static assets
                                         expand: true,
                                         dot: true,
                                         cwd: '<%= config.collectedAssets %>',
                                         src: [
                                             '*.{ico,png,txt}',
                                             '.htaccess',
                                             '{,*/}{images,img}/**/*.webp',
                                             '{,*/}fonts/**/*.*'
                                         ],
                                         dest: '<%= config.distAssets %>'
                                     },
                                     {
                                         // Template files
                                         expand: true,
                                         dot: true,
                                         cwd: '<%= config.collectedTemplates %>',
                                         src: '**/*.html',
                                         dest: '<%= config.distTemplates %>'
                                     },
                                     {
                                         // Bootstrap
                                         expand: true,
                                         dot: true,
                                         cwd: '.',
                                         src: '<%= config.collectedAssets %>/bower_components/bootstrap-sass-official/vendor/assets/fonts/bootstrap/*.*',
                                         dest: '<%= config.distAssets %>'
                                     }
                                 ]
                             },
                             // Copy all CSS files for concat task
                             diststyles: {
                                 expand: true,
                                 dot: true,
                                 cwd: '<%= config.collectedAssets %>',
                                 src: '{,*/}{styles,css}/**/*.css',
                                 dest: '.tmp'
                             },
                             styles: {
                                 expand: true,
                                 dot: true,
                                 cwd: '<%= config.assets %>',
                                 src: '{,*/}{styles,css}/**/*.css',
                                 dest: '.tmp'
                             },
                             // Simulate the collection process
                             simcollected: {
                                 files: [
                                     {
                                         // Static assets
                                         expand: true,
                                         dot: true,
                                         cwd: '<%= config.assets %>',
                                         src: '**',
                                         dest: '<%= config.collectedAssets %>'
                                     },
                                     {
                                         // Templates
                                         expand: true,
                                         dot: true,
                                         cwd: '<%= config.templates %>',
                                         src: '**',
                                         dest: '<%= config.collectedTemplates %>'
                                     }
                                 ]
                             }
                         },

                         // Generates a custom Modernizr build that includes only the tests you
                         // reference in your app
                         modernizr: {
                             devFile: '<%= config.collectedAssets %>/bower_components/modernizr/modernizr.js',
                             outputFile: '<%= config.distAssets %>/scripts/vendor/modernizr.js',
                             files: [
                                 '<%= config.distAssets %>/{,*/}{scripts,js}/**/*.js',
                                 '<%= config.distAssets %>/{,*/}{styles,css}/**/*.css',
                                 '!<%= config.distAssets %>/{,*/}{scripts,js}/vendor/*'
                             ],
                             uglify: true
                         },


                         // Run some tasks in parallel to speed up build process
                     });


    grunt.registerTask('serve', function (target) {
        if (target === 'dist') {
            return grunt.task.run(['build', 'connect:dist:keepalive']);
        }

        grunt.task.run([
                           'clean:server',
                           'autoprefixer',
                           'connect:livereload',
                           'watch'
                       ]);
    });

    grunt.registerTask('serve', function (target) {
        if (target === 'dist') {
            return grunt.task.run(['build', 'connect:dist:keepalive']);
        }

        grunt.task.run([
                           'clean:server',
                           'autoprefixer',
                           'connect:livereload',
                           'watch'
                       ]);
    });

    grunt.registerTask('server', function (target) {
        grunt.log.warn('The `server` task has been deprecated. Use `grunt serve` to start a server.');
        grunt.task.run([target ? ('serve:' + target) : 'serve']);
    });

    grunt.registerTask('test', [
        'clean:server',
        'autoprefixer',
        'connect:test',
        'karma'
    ]);
//    grunt.registerTask('test', function (target) {
//        if (target !== 'watch') {
//            grunt.task.run([
//                               'clean:server',
//                               'autoprefixer'
//                           ]);
//        }
//
//        grunt.task.run([
//                           'connect:test',
//                           'jasmine'
//                       ]);
//    });

    grunt.registerTask('checkcollected', function () {
        var fs = require('fs');
        var config = grunt.config.get('config');
        if (!fs.existsSync(config.collectedAssets)) {
            /*jshint multistr:true */
            grunt.fail.fatal(grunt.template.process('\
Collect assets and templates into the following directories first:\n\
  * <%= config.collectedAssets %>\n\
  * <%= config.collectedTemplates %>\n\n\
Hints: You might need to run `../manage.py collectstatic` to collect \
static assets, and some custom Fabric tasks to collect templates. \n\n\
If you want to try out the `build` task, run `grunt copy:simcollected` \
to simulate the collection process, then try again.'));
        }
    });

    grunt.registerTask('build', [
        'checkcollected',
        'clean:dist',
        'useminPrepare',
        'requirejs',
        'clean:requirejs',
        'autoprefixer',
        'cssmin',
        'uglify',
        'copy:dist',
        'modernizr',
        'filerev',
        'requirejspaths',
        'processhtml',
        'usemin',
        'htmlcompressor',
//        'clean:collected'
    ]);

    grunt.registerTask('default', [
        'newer:jshint',
        'test',
        'build'
    ]);
};
