var app = angular.module( "QuizEditor", ['ui.bootstrap'] );

app.controller( "editorController", function userController($scope,$http,$modal,$log,$location) {
  var qs = $location.search();
  $scope.quiz_id = qs.id;

  var question = {
      "question": "",
      "source": "",
      "answer": "",
  }
  $scope.questions = [question]

  $scope.add_question = function() {
    var question = {
        "question": "",
        "source": "",
        "answer": "",
    }

    $scope.questions.push(question);
  }

  $scope.remove_question = function(question) {
    $log.info("hi");
    for(var i in $scope.questions) {
      if($scope.questions[i]==question) {

        $scope.questions.splice(i,1);
        return;
      }
    }
  }
})