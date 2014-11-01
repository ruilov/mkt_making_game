var app = angular.module( "home", ['ui.bootstrap'] );

app.controller( "homeController", function userController($scope,$http,$location) {
  $scope.has_quiz = "unknown";

  var responsePromise = $http.get("/quizzes_api/?status=active");
  responsePromise.success(function(data, status, headers, config) {
    quizzes = data.quizzes;
    if(quizzes.length>0) {
      $scope.has_quiz = "true";
      $scope.quiz_url = quiz_url(quizzes[0].id,true);
      return;
    };
    $scope.has_quiz = "false";
  });
})