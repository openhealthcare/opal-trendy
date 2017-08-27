var directives = angular.module('opal.directives', []);

directives.directive("pieChart", function () {
  "use strict";
  return {
    restrict: 'A',
    scope: {
      data: "=pieChart",
    },
    link: function (scope, element, attrs) {
      var graphParams = {
        bindto: element[0],
        data: {
          // iris data from R
          columns: scope.data,
          // [
          //   ['data1', 30],
          //   ['data2', 120],
          // ],
          type : 'pie',
          size: {
            height: 25,
            width: 50
          }
        }
      };
      setTimeout(function(){
        c3.generate(graphParams);
      }, 100);
    }
  };
});
