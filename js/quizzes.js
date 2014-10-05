var app = angular.module( "MyApp", ['ui.bootstrap'] );

app.controller( "quizzesController", function userController($scope,$http,$location) {
  $scope.quizzes = [];

  $scope.nextID = -1;
  $scope.nextURL = "/quiz_editor.html/#?id="+$scope.nextID;

  var responsePromise = $http.get("/quizzes/");
  responsePromise.success(function(data, status, headers, config) {
    $scope.quizzes = data.quizzes;
    for(var i in $scope.quizzes) {
      id = $scope.quizzes[i].id;
      $scope.quizzes[i].url = "/quiz_editor.html/#?id="+id;
      $scope.nextID = Math.max($scope.nextID,parseInt(id));
    };

    $scope.nextID += 1;
    $scope.nextURL = "/quiz_editor.html/#?id="+$scope.nextID;
  });

  $scope.delete = function(quiz) {
    for(var i in $scope.quizzes) {
      if($scope.quizzes[i]==quiz) {
        var req = $http.post("/quizzes/",quiz.id);
        req.success(function(data, status, headers, config) {
          $scope.quizzes.splice(i,1); 
        });
        return;
      }
    };
  };
})