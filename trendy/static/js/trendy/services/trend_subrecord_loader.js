angular.module('opal.services').factory('TrendSubrecordLoader', function($q, $http, $location, $window, $log, $routeParams) {
    "use strict";

    var url = '/trend_subrecord_loader/';

    var load = function(subrecordApiName){
      var getArgs $location.url().replace($location.path(), "");
      if(_.size($routeParams)){
        url = url + "&subrecord=" + trend_subrecord_loader
      }
      else{
        url = url + "?subrecord=" + trend_subrecord_loader
      }
      var deferred = $q.defer();
      $http({cache: true, url: url, method: 'GET'}).then(function(response) {
          deferred.resolve(response.data);
      }, function() {
        // handle error better
        $window.alert('TrendSubrecordInfo could not be loaded');
      });
      return deferred.promise;
    };

    return {
      load: load
    };
});
