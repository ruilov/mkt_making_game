var app = angular.module( "quizzes", ['ui.bootstrap'] );

app.controller( "quizzesController", function userController($scope,$http) {
  $scope.quizzes = [];

  $scope.nextID = -1;
  $scope.nextURL = quiz_editor_url($scope.nextID);

  // get the non-old quizzes
  var responsePromise = $http.get("/api/quizzes/?status=editor_active_old");
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

  $scope.quiz_action = function(quiz,action,new_state) {
    for(var i in $scope.quizzes) {
      if($scope.quizzes[i]==quiz) {
        if(!confirm("Do you really want to " + action + " this quiz?")) return;
        var req = $http.post("/api/quizzes/",{"action": action, "id": quiz.id});
        req.success(function(data, status, headers, config) {
          $scope.quizzes[i]["status"] = new_state;
        });
        return;
      }
    };
  }

  $scope.delete = function(quiz) {
    for(var i in $scope.quizzes) {
      if($scope.quizzes[i]==quiz) {
        if(!confirm("Do you really want to delete this quiz?")) return;
        var req = $http.post("/api/quizzes/",{"action": "delete", "id": quiz.id});
        req.success(function(data, status, headers, config) {
          $scope.quizzes.splice(i,1); 
        });
        return;
      }
    };
  };

  $scope.activate = function(quiz) {
    $scope.quiz_action(quiz,"activate","active");
  };

  $scope.deactivate = function(quiz) {
    $scope.quiz_action(quiz,"deactivate","old");
  };
  
  $scope.unold = function(quiz) {
    $scope.quiz_action(quiz,"unold","editor");
  };

  $scope.sendmail = function(quiz) {
    if(!confirm("Do you really want to send the emails?")) return;
    var req = $http.post("/api/send_mail/",{"test": true});
    req.success(function(data, status, headers, config) {
      for(var k in data) {
        $scope.email_answer = k;
        return;
      };
    });
  };

})