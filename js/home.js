var app = angular.module( "home", ['ui.bootstrap'] );

app.controller( "homeController", function userController($scope,$http,$location) {
  $scope.quiz_url = false;
  var responsePromise = $http.get("/quizzes_api/?status=active");
  responsePromise.success(function(data, status, headers, config) {
    console.log(data);
    quizzes = data.quizzes;
    if(quizzes.length>0) {
      quiz = quizzes[0];
      $scope.quiz_url = quiz_url(quiz.id,true);
      return;
    };
  });
})