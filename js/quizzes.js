var app = angular.module( "quizzes", ['ui.bootstrap'] );

app.controller( "quizzesController", function userController($scope,$http) {
  $scope.quizzes = [];

  $scope.nextID = -1;
  $scope.nextURL = quiz_editor_url($scope.nextID);

  // get the non-old quizzes
  var responsePromise = $http.get("/quizzes_api/?status=editor_active_old");
  responsePromise.success(function(data, status, headers, config) {
    $scope.quizzes = data.quizzes;
    for(var i in $scope.quizzes) {
      id = $scope.quizzes[i].id;
      $scope.quizzes[i].editorUrl = quiz_editor_url(id);
      $scope.quizzes[i].quizUrl = quiz_url(id);
      $scope.quizzes[i].name = quiz_name(id);
      $scope.nextID = Math.max($scope.nextID,parseInt(id));
    };

    $scope.nextID += 1;
    $scope.nextURL = quiz_editor_url($scope.nextID);
  });

  $scope.delete = function(quiz) {
    for(var i in $scope.quizzes) {
      if($scope.quizzes[i]==quiz) {
        if(!confirm("Do you really want to delete this quiz?")) return;
        var req = $http.post("/quizzes_api/",{"action": "delete", "id": quiz.id});
        req.success(function(data, status, headers, config) {
          $scope.quizzes.splice(i,1); 
        });
        return;
      }
    };
  };

  $scope.activate = function(quiz) {
    for(var i in $scope.quizzes) {
      if($scope.quizzes[i]==quiz) {
        if(!confirm("Do you really want to activate this quiz?")) return;
        var req = $http.post("/quizzes_api/",{"action": "activate", "id": quiz.id});
        req.success(function(data, status, headers, config) {
          $scope.quizzes[i]["status"] = "active";
        });
        return;
      }
    };
  };

  $scope.deactivate = function(quiz) {
    for(var i in $scope.quizzes) {
      if($scope.quizzes[i]==quiz) {
        if(!confirm("Do you really want to deactivate this quiz?")) return;
        var req = $http.post("/quizzes_api/",{"action": "deactivate", "id": quiz.id});
        req.success(function(data, status, headers, config) {
          $scope.quizzes.splice(i,1);
        });
        return;
      }
    };
  };
  
  $scope.unold = function(quiz) {
    for(var i in $scope.quizzes) {
      if($scope.quizzes[i]==quiz) {
        if(!confirm("Do you really want to unold this quiz?")) return;
        var req = $http.post("/quizzes_api/",{"action": "unold", "id": quiz.id});
        req.success(function(data, status, headers, config) {
          $scope.quizzes.splice(i,1);
        });
        return;
      }
    };
  };
})