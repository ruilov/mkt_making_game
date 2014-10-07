var mainApp = angular.module( "main", ['ngRoute','quizzes','quiz','quizEditor'] );

mainApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
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
        redirectTo: '/quizzes'
      });
  }
]);