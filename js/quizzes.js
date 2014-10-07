var app = angular.module( "quizzes", ['ui.bootstrap'] );

app.controller( "quizzesController", function userController($scope,$http,$location) {
  $scope.quizzes = [];

  $scope.nextID = -1;
  $scope.nextURL = "/#/quiz_editor?id="+$scope.nextID;

  var responsePromise = $http.get("/quizzes_api/");
  responsePromise.success(function(data, status, headers, config) {
    $scope.quizzes = data.quizzes;
    for(var i in $scope.quizzes) {
      id = $scope.quizzes[i].id;
      $scope.quizzes[i].editorUrl = "/#/quiz_editor?id="+id;
      $scope.quizzes[i].quizUrl = "/#/quiz?id="+id;
      $scope.nextID = Math.max($scope.nextID,parseInt(id));
    };

    $scope.nextID += 1;
    $scope.nextURL = "/#/quiz_editor?id="+$scope.nextID;
  });

  $scope.delete = function(quiz) {
    for(var i in $scope.quizzes) {
      if($scope.quizzes[i]==quiz) {
        var req = $http.post("/quizzes_api/",quiz.id);
        req.success(function(data, status, headers, config) {
          $scope.quizzes.splice(i,1); 
        });
        return;
      }
    };
  };
})