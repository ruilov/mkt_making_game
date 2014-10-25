// this is the controler for the template of all the HTML pages
var templateApp = angular.module( "template", ['ngRoute','index','quizzes','quiz','quizEditor','rankings','rankingDetailed'] );

templateApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'index.html',
        controller: 'indexController',
      }).
      when('/login', {
        templateUrl: 'login.html',
      }).
      when('/rankings', {
        templateUrl: 'rankings.html',
        controller: 'rankingsController',
      }).
      when('/ranking_detailed', {
        templateUrl: 'ranking_detailed.html',
        controller: 'rankingDetailedController',
        resolve: {
          message: function($http,$location,quizOldService) {
            var qs = $location.search();
            var req = $http.get("/quiz_api/?id="+qs.id);
            return req.success(quizOldService.isAllowed);
          }
        }
      }).
      when('/quizzes', {
        templateUrl: 'quizzes.html',
        controller: 'quizzesController'
      }).
      when('/quiz', {
        templateUrl: 'quiz.html',
        controller: 'quizController',
        resolve: {
          message: function($http,$location,quizAllowedService) {
            var qs = $location.search();
            var req = $http.get("/quiz_api/?id="+qs.id);
            return req.success(quizAllowedService.isAllowed);
          }
        }
      }).
      when('/quiz_editor', {
        templateUrl: 'quiz_editor.html',
        controller: 'editorController'
      }).
      when('/not_allowed', {
        templateUrl: 'not_allowed.html',
      }).
      otherwise({
        redirectTo: '/'
      });
  }
]);

templateApp.factory("quizAllowedService", function ($rootScope, $location) {
  return {
    isAllowed: function(quiz, status, headers, config) {
      $rootScope.quiz_data = quiz;
      if(typeof(quiz)=="string" || ("not_allowed" in quiz)) {
        $location.path("/not_allowed");
      }
      return;
    }
  };
});

templateApp.factory("quizOldService", function ($rootScope, $location) {
  return {
    isAllowed: function(quiz, status, headers, config) {
      $rootScope.quiz_data = quiz;
      if(typeof(quiz)=="string" || ("quiz_not_old" in quiz)) {
        $location.path("/not_allowed");
      }
      return;
    }
  };
});

templateApp.controller( "templateController", function ($scope,$http) {
  $scope.old_quizzes = [];

  var responsePromise = $http.get("/quizzes_api/?status=old");
  responsePromise.success(function(data, status, headers, config) {
    $scope.old_quizzes = data.quizzes;
    for(var i in $scope.old_quizzes) {
      id = $scope.old_quizzes[i].id;
      $scope.old_quizzes[i].url = quiz_url(id);
      $scope.old_quizzes[i].name = quiz_name(id);
      $scope.old_quizzes[i].date = new Date($scope.old_quizzes[i].releaseDate);
    };
    $scope.old_quizzes.sort(function(a,b) {
      if(a.date<b.date) return -1;
      else if(a.date>b.date) return 1;
      return 0;
    });
    for(var i in $scope.old_quizzes) 
      $scope.old_quizzes[i].date = $scope.old_quizzes[i].date.toLocaleDateString("en-US");
  });
});
