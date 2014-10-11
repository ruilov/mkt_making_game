var app = angular.module( "index", ['ui.bootstrap'] );

app.controller( "indexController", function userController($scope,$http,$location) {
  var responsePromise = $http.get("/quizzes_api/?status=active");
  responsePromise.success(function(data, status, headers, config) {
    quizzes = data.quizzes;
    if(quizzes.length>0) {
      quiz = quizzes[0];
      url = quiz_url(quiz.id,true);
      $location.path("/quiz").search("id",quiz.id);
    };
  });
})