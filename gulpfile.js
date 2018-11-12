let gulp = require('gulp'),
    pjson = require('./package.json'),
    concat = require('gulp-concat'),
    sass = require('gulp-sass'),
    watch = require('gulp-watch'),
    sourcemaps = require('gulp-sourcemaps'),
    postcss = require('gulp-postcss'),
    babel = require('gulp-babel'),
    autoprefixer = require('autoprefixer'),
    cssnano = require('cssnano'),
    uglify = require('gulp-uglify'),
    spawn = require('child_process').spawn,
    rename = require('gulp-rename'),
    plumber = require('gulp-plumber'),
    imagemin = require('gulp-imagemin'),
    runSequence = require('run-sequence'),
    browserSync = require('browser-sync').create();

let pathsConfig = function (appName) {
    this.app = "./" + (appName || pjson.name);
    return {
        app: this.app,
        templates: `${this.app}/templates`,
        src: `${this.app}/static/src`,
        build: `${this.app}/static/build`,
    }
};

let paths = pathsConfig();

/**
 * CSS assets
 * 
 * The SASS files are run through postcss/autoprefixer and placed into one 
 * single main styles.min.css file (and sourcemap)
 */
gulp.task('styles', function () {
    let styles = gulp.src(`${paths.src}/sass/main.scss`)
        .pipe(sourcemaps.init())
        .pipe(sass({
            includePaths: [
                'node_modules/'
            ]
        }).on('error', sass.logError))
        .pipe(postcss([
            autoprefixer,
            cssnano
        ]))
        .pipe(rename('styles.min.css'))
        .pipe(plumber())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(`${paths.build}/css/`));
    let admin = gulp.src(`${paths.src}/sass/admin.scss`)
        .pipe(sass().on('error', sass.logError))
        .pipe(plumber())
        .pipe(rename('admin.min.css'))
        .pipe(gulp.dest(`${paths.build}/css/`));
    return [styles, admin];
});

/**
 * Javascript assets
 * 
 * All regular .js files are collected, minified and concatonated into one
 * single scripts.min.js file (and sourcemap)
 */
gulp.task('scripts', function () {
    return gulp.src([`${paths.src}/js/scripts.js`])
        .pipe(sourcemaps.init())
        .pipe(babel({
            presets: ['es2015']
        }))
        .pipe(uglify())
        .pipe(concat('scripts.min.js'))
        .pipe(plumber())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(`${paths.build}/js/`));
});

/**
 * External Javascript assets
 * 
 * Any required external libraries are collected, minified and concatonated 
 * into one single vendor.min.js file (and sourcemap)
 */
gulp.task('vendor', function () {
    return gulp.src([
            'node_modules/jquery/dist/jquery.js',
            'node_modules/bootstrap/dist/js/bootstrap.js',
        ])
        .pipe(concat('vendor.min.js'))
        .pipe(uglify())
        .pipe(plumber())
        .pipe(gulp.dest(`${paths.build}/js/`));
});

gulp.task('imgCompression', function () {
    return gulp.src(`${paths.src}/images/**/*`)
        .pipe(imagemin({ optimizationLevel: 5, progressive: true, interlaced: true })) // Compresses PNG, JPEG, GIF and SVG images
        .pipe(gulp.dest(`${paths.build}/images/`));
});

gulp.task('runServer', function (cb) {
    var cmd = spawn('python', ['manage.py', 'runserver'], { stdio: 'inherit' });
    cmd.on('close', function (code) {
        console.log('runServer exited with code ' + code);
        cb(code);
    });
});

gulp.task('browserSync', function () {
    browserSync.init(
        [`${paths.build}/css/*.css`, `${paths.build}/js/*.js`, `${paths.templates}/*.html`], {
            // Proxying the django Docker container
            // https://stackoverflow.com/questions/42456424/browsersync-within-a-docker-container
            proxy: "django:8000",
            open: false
        });
});

/**
 * Watch for changes
 * 
 * Using the default gulp.watch causes issues within Docker where the CPU goes
 * to 100% so we ust gulp-watch instead:
 * 
 * https://forums.docker.com/t/docker-compose-volumes-gulp-watch-100-cpu-usage/10192/14
 */
gulp.task('watch', function () {
    let opts = { usePolling: true, interval: 2000 };
    watch(`${paths.src}/sass/**/*.scss`, opts, () => { gulp.start('styles') });
    watch(`${paths.src}/js/**/*.js`, opts, () => gulp.start('scripts'));
    watch(`${paths.src}/images/**/*`, opts, () => gulp.start('imgCompression'));
});

gulp.task('default', function () {
    runSequence(
        ['styles', 'scripts', 'vendor', 'imgCompression'],
        ['browserSync', 'watch'],
        ['runServer']);
});
