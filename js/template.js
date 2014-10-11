// this is the controler for the template of all the HTML pages

var templateApp = angular.module( "template", ['ngRoute','index','quizzes','quiz','quizEditor'] );

templateApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'index.html',
        controller: 'indexController'
      }).
      when('/quizzes', {
        templateUrl: 'quizzes.html',
        controller: 'quizzesController'
      }).
      when('/quiz', {
        templateUrl: 'quiz.html',
        controller: 'quizController'
      }).
      when('/quiz_editor', {
        templateUrl: 'quiz_editor.html',
        controller: 'editorController'
      }).
      otherwise({
        redirectTo: '/'
      });
  }
]);

templateApp.controller( "templateController", function mainController($scope,$http) {
  $scope.old_quizzes = [];

  var responsePromise = $http.get("/quizzes_api/?status=old");
  responsePromise.success(function(data, status, headers, config) {
    $scope.old_quizzes = data.quizzes;
    for(var i in $scope.old_quizzes) {
      id = $scope.old_quizzes[i].id;
      $scope.old_quizzes[i].url = quiz_url(id);
      $scope.old_quizzes[i].name = quiz_name(id);
      $scope.old_quizzes[i].date = new Date($scope.old_quizzes[i].releaseDate).toDateString();
    };
  });
});
