var app = angular.module( "quizEditor", ['ui.bootstrap'] );

app.controller( "editorController", function userController($scope,$http,$location) {
  var qs = $location.search();
  var quiz_id = qs.id;

  $scope.quiz = {"questions": []};

  var req = $http.get("/quiz_editor_api/?id="+quiz_id);
  req.success(function(quiz, status, headers, config) {
    for(var i in quiz.questions) {
      question = quiz.questions[i];
      $scope.add_question(question.text,question.source,question.answer);
    };
  });

  $scope.add_question = function(text,source,answer,save) {
    if(save==undefined) save = false;

    var question = {
        "text": text,
        "source": source,
        "answer": answer,
    }

    $scope.quiz.questions.push(question);
    if(save) $scope.saveQuiz();
  };

  $scope.remove_question = function(question) {
    for(var i in $scope.quiz.questions) {
      if($scope.quiz.questions[i]==question) {
        $scope.quiz.questions.splice(i,1);
        $scope.saveQuiz();
        return;
      }
    };
  };

  $scope.saveQuiz = function() {
    $http.post("/quiz_editor_api/?id="+quiz_id,$scope.quiz);
  };
})