module.exports = function(config){
  var opalPath = process.env.OPAL_LOCATION;
  var karmaDefaults = require(opalPath + '/config/karma_defaults.js');
  var baseDir = __dirname + '/..';
  var coverageFiles = [
    __dirname+'/../trendy/static/js/trendy/**/*.js',
  ];
    var includedFiles = [
      __dirname+'/../trendy/static/js/trendy/**/*.js',
      __dirname+'/../trendy/static/js/test/*.js',
  ];

  var defaultConfig = karmaDefaults(includedFiles, baseDir, coverageFiles);
  config.set(defaultConfig);
};